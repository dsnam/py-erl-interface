This example is adapted from the [C example](https://www.erlang.org/doc/tutorial/erl_interface#c-program) in the Erlang docs and does a lot of things that are unusual in python (deals mostly in C types via cffi, handles unbuffered input/output). There may be better ways to write this glue code, but this is certainly an approach that works. On the bright side all the weirdness can be hidden away in the entry point that interfaces with Erlang, leaving whatever code you want to call into alone.

The gist of it is that you must write a python entry point that will handle decoding messages sent to it by the process in the Erlang VM and encoding the results from your python library to send back. Like the C example in the docs the python functions I expose are extremely simple, so the decoding/encoding boilerplate is about as easy on the eyes as that kind of code can be.


To run this example:
1. Set PYEI_OTP_PATH to point at your OTP install's erl_interface and then build the extension with `make`. Note that this step will do a local editable install of the package.

2. launch an interactive erlang session with `erl`.

3. Compile the erlang module that wraps the communication with the external process: `c(external_wrapper)`

4. Start the process: `external_wrapper:start("python example.py")`

5. Call the python code! `external_wrapper:increment(3)`

You should see something like this in your interactive session:

```
Erlang/OTP 26 [erts-14.2] [source] [64-bit] [smp:4:4] [ds:4:4:10] [async-threads:1] [jit:ns]

Eshell V14.2 (press Ctrl+G to abort, type help(). for help)
1> c(external_wrapper).
external_wrapper.erl:32:24: Warning: variable 'Reason' is unused
%   32|         {'EXIT', Port, Reason} ->
%     |                        ^

{ok,external_wrapper}
2> external_wrapper:start("python example.py").
<0.93.0>
3> external_wrapper:increment(5).
6
4> external_wrapper:decrement(11).
10
5> external_wrapper:stop().
stop
```