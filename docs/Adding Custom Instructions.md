Adding Custom Instructions
==========================
Being an instruction-based debugger, Scout supports project extensions.

Registration - C Code
---------------------
* Each of the instructions that are added by the project, should be registerred by calling ```register_instruction()```.
* The registration should take place inside the function ```register_specific_instructions()```.
* This design makes sure that when invoking ```register_all_instructions()```, all of the default instructions, and extension instruction, will be registerred correctly.

Implementation - C Code
-----------------------
In order to implement a new instruction, one should define each of the required parts:

* Instruction ID - must be unique, but not necessarily consecutive
* Minimal Length - minimal amount of bytes needed for a valid instruction (robustness checks)
* Maximal Length - maximal amount of bytes needed for a valid instruction (robustness checks)
* Instruction handler - a handler function with a fixed signature of: ```int32_t (*instrHandler)(void * ctx, uint8_t * instruction, uint32_t length)```

**Note:** The instructions are stored in a global array with a **fixed** capacity. When adding new instructions, one should make sure to adjust this capacity accordingly.
The capacity is defined in ```scout_api.h``` and is set by default to ```#define SCOUT_MAX_INSTRS   (10)```.

Examples - C Code
-----------------
* Embedded mode (```embedded_scout```) - files ```project_instructions``` (*.c and *.h)
* Linux Kernel mode (```kernel_scout```) - files ```driver\scout_kernel_instructions``` (*.c and *.h)

Client Side - Python Code
-------------------------
In the client side, adding a new instructions is even easier, and requires only 2 definitions:

* Defining the Instruction ID (as was defined in the C code)
* Implementing a serializer for the instruction

Examples - Python Code
----------------------
* Linux Kernel example (```manager```) - file ```kernel_scout_api.py```