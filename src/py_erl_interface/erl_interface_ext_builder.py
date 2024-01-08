import os
import logging
from cffi import FFI
from pycparser import parse_file
from pycparserext.ext_c_generator import GnuCGenerator
from pycparserext.ext_c_parser import GnuCParser

logger = logging.getLogger(__name__)

OTP_PATH = os.getenv('PYEI_OTP_PATH')
CPP_PATH = os.getenv('PYEI_CPP_PATH') or 'cpp'


def _should_filter_ast_node(node) -> bool:
    def from_eih_file(n):
        return n.coord and 'ei.h' in n.coord.file
    
    def is_erl_errno(n):
        # this one is a hack because I didn't see a clear way to distinguish 
        # plain var decls from other decls in the AST. The cdef only needs to
        # have the typedefs and functions in it, just drop this node entirely.
        # If other versions of erl_interface have other such declarations then
        # this will need to become less of a hack.
        return n.name == '__erl_errno'
        
    return from_eih_file(node) and not is_erl_errno(node)
    
def try_generate_cdef():
    eih_path = os.path.join(OTP_PATH, 'include', 'ei.h')
    ast = parse_file(eih_path, use_cpp=True, cpp_path=CPP_PATH, parser=GnuCParser())
    filtered_children = [child for child in ast.ext if _should_filter_ast_node(child)]
    ast.ext = filtered_children
    c_gen = GnuCGenerator()
    pyei_path = os.path.join(os.path.dirname(__file__), 'pyei.h')
    with open(pyei_path, 'w') as cdef_f:
        cdef_f.write(c_gen.visit(ast))
    return pyei_path

CDEF_PATH = os.getenv('PYEI_CDEF_PATH')

if not CDEF_PATH:
    try:
        CDEF_PATH = try_generate_cdef()
    except Exception as e:
        logger.error('Failed to process ei.h automatically, falling back to bundled cdef', exc_info=True)
        CDEF_PATH = os.path.join(os.path.dirname(__file__), 'pyei.cdef')

builder = FFI()

with open(CDEF_PATH) as cdef_file:
    cdef_content = cdef_file.read()
    builder.cdef(cdef_content)
    

builder.set_source(
    module_name="_erl_interface",
    source="""
        #include "ei.h"
    """,
    include_dirs=[f'{OTP_PATH}/include'],
    library_dirs=[f'{OTP_PATH}/lib'],
    libraries=['ei', 'pthread'],
)
            
if __name__ == '__main__':
    builder.compile(verbose=True)