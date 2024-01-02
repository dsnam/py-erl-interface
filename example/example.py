import sys
import logging
from typing import Tuple, Any

from _erl_interface import ffi, lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('example.log', mode='w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def crash(reason):
    logger.error(reason)
    exit(1)
    
def increment(number):
    return number + 1
    
def decrement(number):
    return number - 1

def main():
    lib.ei_init()
    
    # most of the erl_interface functions expect a pointer to a buffer and an index into it.
    # they will operate on a section of the buffer and then bump the index to the end of the section
    in_buff = ffi.new('unsigned char[100]')
        
    with open(0, 'rb', buffering=0) as raw_in, open(1, 'wb', buffering=0) as raw_out:
        while read_from_erl(raw_in, in_buff) > 0:
            atom_str, args = decode_input_in_buffer(in_buff)
            if atom_str == b'increment':
                res = increment(*args)
            elif atom_str == b'decrement':
                res = decrement(*args)
            else:
                crash('unknown command')
                
            res_buff = encode_result_in_buffer(res)
                
            write_to_erl(raw_out, res_buff.buff, res_buff.index)
            
            if lib.ei_x_free(res_buff) != 0:
                crash('failed to free result buffer')
                        
    
def encode_result_in_buffer(result: int):
    res_buff = ffi.new('ei_x_buff *')
    if lib.ei_x_new_with_version(res_buff) != 0:
        crash('failed to set up new ei_x_buff')
        
    if lib.ei_x_encode_long(res_buff, ffi.cast('long', result)) != 0:
        crash('failed to encode result')
        
    return res_buff
    
    
def decode_input_in_buffer(buffer) -> Tuple[str, Tuple[Any]]:
    idx = ffi.new('int *')
    version = ffi.new('int *')
    arity = ffi.new('int *')
    long = ffi.new('long *')
    atom = ffi.new('char[128]')

    if lib.ei_decode_version(buffer, idx, version) != 0:
        crash('failed decoding version')
    if lib.ei_decode_tuple_header(buffer, idx, arity) != 0:
        crash('failed decoding tuple header')
    if arity[0] != 2:
        crash(f'incorrect arity')
    if lib.ei_decode_atom(buffer, idx, atom) != 0:
        crash('failed decoding atom')
    # can just immediately assume there's a long to decode since both functions have the same arg
    if lib.ei_decode_long(buffer, idx, long) != 0:
        crash('failed decoding long')
        
    atom_str = ffi.string(atom)
        
    return atom_str, (long[0],)
    
    
def write_to_erl(raw_out, buff, length):
    raw_out.write(length.to_bytes(2))
    ffi_buffer = ffi.buffer(buff, length)
    raw_out.write(ffi_buffer[0:length])
    

def read_from_erl(raw_in, buff) -> int:
    # the first two bytes describe the packet size, as per the args to open_port in external_wrapper.erl
    p_size = raw_in.read(2)
    if not p_size or len(p_size) != 2:
        return -1
    length = (p_size[0] << 8) | p_size[1]
    data = raw_in.read(length)
    ffi.memmove(buff, data, length)
    return length
    

if __name__ == '__main__':
    main()