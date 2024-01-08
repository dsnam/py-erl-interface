# py-erl-interface
This is a utility for generating a Python C extension for [erl_interface](https://www.erlang.org/doc/apps/erl_interface/) for an Erlang/OTP install. Once you've generated the extension, you can use the erl_interface functions to connect python and erlang code.

[python-cffi](https://github.com/python-cffi/cffi) does most of the heavy lifting here and is a fantastic library, and I'd also highly recommend using it for working with the generated extension functions (see the example in this repository).

## tl;dr
1. set `PYEI_OTP_PATH` to your OTP install's erl_interface directory
2. run `python erl_interface_ext_build.py`
3. drop the `.so` file whereever you want to use it
4. import it in your python code with `from _erl_interface import ffi, lib`
5. `lib` will have all of the functions from the cdef, while `ffi` is a special object from cffi that can help create custom types from the cdef in addition to a ton of useful Python/C interop utilities, which will be needed to interact with the wrapped functions.

## Use as a script
You must point this at the erl_interface directory of an Erlang/OTP installation by setting the `PYEI_OTP_PATH` environment variable. For example:

```export PYEI_OTP_PATH=/usr/lib/erlang/lib/erl_interface-X.Y/```

where X and Y will vary according to your Erlang/OTP version. The path to your install may differ significantly from mine.

This script will attempt to parse and process the ei.h file in your Erlang install first. For this to work you must have cpp installed. If it is not on your path, set the `PYEI_CPP_PATH` variable to point at the binary.

If this processing fails, it will use a bundled cdef file created from erl_interface in OTP 26. If you would like to create the cdef yourself, you can point the script at it by setting `PYEI_CDEF_PATH` to its absolute path.

To generate the extension you can just run the script after setting the relevant environment variables: `python erl_interface_ext_build.py`

If you pip install (this is not on pypi, so you'd have to do so from git or checkout the repo and do a local install) then you can also run `python -m py_erl_interface`

See the example directory for a simple example that shows how to write a basic Python entry point for interfacing with Erlang and how to call some of erl_interface's encoding/decoding functions. 