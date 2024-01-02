import os
from cffi import FFI


OTP_PATH = os.getenv('PYEI_OTP_PATH')
CDEF_PATH = os.getenv('PYEI_CDEF_PATH') or os.path.join(os.path.dirname(__file__), 'pyei.cdef')

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