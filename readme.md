# py-erl-interface
This is a utility for generating a Python C extension for [erl_interface](https://www.erlang.org/doc/apps/erl_interface/) for an Erlang/OTP install. Once you've generated the extension, you can use the erl_interface functions to connect python and erlang code.

[python-cffi](https://github.com/python-cffi/cffi) does most of the heavy lifting here and is a fantastic library, and I'd also highly recommend using it for working with the generated extension functions (see the example in this repository).

This was written for and tested on Linux. It will not work on Windows out of the box for two reasons:
1. I had to strip several Windows-specific definitions in ei.h out of the cdef that I produced from it since python-cffi does not support ifdef and other directives. Only what will work on linux is present in the bundled cdef.
2. I configured the extension builder with pthreads as a library, following the examples of compiling plain C code to interop with Erlang in the docs.

If someone finds this and wants to use it on Windows, it may not be too hard to produce a windows variant of the cdef file and use whatever erl_interface uses for threading on Windows instead. Hopefully those should be the only changes needed in that case.


## Use as a script
You must point this at the erl_interface directory of an Erlang/OTP installation by setting the PYEI_PATH environment variable. For example:

```export PYEI_OTP_PATH=/usr/lib/erlang/lib/erl_interface-X.Y/```

where X and Y will vary according to your Erlang/OTP version. The path to your install may differ significantly from mine, so don't just copy the snippit above. 

Please note that I used OTP 26 (version 5.5 of erl_interface) to create the included cdef file. If you have a version that differs significantly then the generated extension may not work, or may not even compile at all. A more complete tool may attempt to generate the cdef from ei.h, but this does not do that. If you run into this and want to create your own cdef for your version, you can point the script at it by setting the `PYEI_CDEF_PATH` environment variable to its absolute path.

To generate the extension you can just run the script (after setting at least PYEI_PATH): `python erl_interface_ext_build.py`

If you pip install (this is not on pypi, so you'd have to do so from git or checkout the repo and do a local install) then you can also run `python -m py_erl_interface`

See the example directory for a simple example that shows how to write a basic Python entry point for interfacing with Erlang and how to call some of erl_interface's encoding/decoding functions.