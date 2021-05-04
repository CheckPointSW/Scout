Scout Instructions
==================
Scout is an instruction-based debugger, that commonly uses a TCP network session on which the instructions are received and their output is being sent.

Default Instructions
--------------------
* **NOP** - Used as a Ping (or Keep-Alive) instruction to make sure the debugger is active and responds to commands
* **Memory Read** - Reads (virtual) memory from the given address, and sends it back
* **Memory Write** - Writes a given binary content to a (virtual) memory in the debuggee's address space

Each supported instruction must be pre-registered by the debugger before it enters his server loop, usually by calling ``register_all_instructions()``.

Network API
-----------
Each instruction is sent together with a network header that includes the following:

* Instruction ID - 2 Bytes
* Length field - 4 Bytes

The length field specifies the length, in bytes, of the serialized instruction.

**Note:** All instructions should be serialized to NETWORK order.
See ``manager\scout_api.py`` for a python sample that prepares the instructions for network transmission.
