-module(external_wrapper).
-export([start/1, stop/0, init/1]).
-export([increment/1, decrement/1]).

% This is taken from the Erlang docs with some very minor modifications (mostly function names to fit the example I set up here better).
% You can find the original code for the C FFI example here: https://www.erlang.org/doc/tutorial/erl_interface#erlang-program

start(ExternalProgram) ->
    spawn(?MODULE, init, [ExternalProgram]).

stop() ->
    ext ! stop.

init(ExternalProgram) ->
    register(ext, self()),
    process_flag(trap_exit, true),
    Port = open_port({spawn, ExternalProgram}, [{packet, 2}, binary]),
    loop(Port).

loop(Port) ->
    receive
        {call, Caller, Msg} ->
            Port ! {self(), {command, term_to_binary(Msg)}},
            receive
                {Port, {data, Data}} ->
                    Caller ! {ext, binary_to_term(Data)}
            end,
            loop(Port);
        stop ->
            Port ! {self(), close},
            receive
                {Port, closed} ->
                    exit(normal)
            end;
        {'EXIT', Port, Reason} ->
            exit(port_terminated)
    end.

increment(X) ->
    call_port({increment, X}).

decrement(X) ->
    call_port({decrement, X}).

call_port(Msg) ->
    ext ! {call, self(), Msg},
    receive
        {ext, Result} ->
            Result
    end.
