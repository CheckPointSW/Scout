Compilation Modes
=================
Scout is a configurable debugger, that could bedeployed in several different environments:

* Linux User-Mode Process - "User Mode"
* Linux Kernel Driver - "Kernel Mode"
* Linux In-Process Debugging - "User Mode" + "PIC Mode"
* Embedded "In-Process" Debugging - "PIC Mode" + "Embedded Mode"

To decide what will be the suitable compilation mode / architecture flags, one should check the following parameters.
Each of the defined parameters is a C MACRO (define) that controls the behavior (and compilation) of the resulting binary.

Target Endianness
-----------------
* SCOUT_BIG_ENDIAN - Scout is executed on a Big Endian architecture
* SCOUT_LITTLE_ENDIAN - Scout is executed on a Little Endian architecture

Only one of above flags can be defined.
If none are defined the base library will define "SCOUT_LITTLE_ENDIAN" on it's own.

Target Bitness
--------------
* SCOUT_BITS_32 - Scout is executed on a 32 bit machine
* SCOUT_BITS_64 - Scout is executed on a 64 bit machine

Only one of above flags can be defined.
If none are defined the base library will define "SCOUT_BITS_32" on it's own.

Target CPU Architecture
-----------------------
* SCOUT_ARCH_INTEL - Scout is executed on an Intel (x86 \ x64) CPU
* SCOUT_ARCH_ARM   - Scout is executed on an ARM (maybe thumb mode) CPU
* SCOUT_ARCH_MIPS  - Scout is executed on a  MIPS (*not* mips16 mode) CPU

Only one of above flags can be defined.
If none are defined the base library will define "SCOUT_ARCH_INTEL" on it's own.

**Additional Flags:**
* SCOUT_ARM_THUMB - Scout will be executed on an ARM cpu in Thumb mode. Can only be used together with the "SCOUT_ARCH_ARM" flag.

The flags is needed only in PIC mode, in which we use inline assembly.

Target Permission Level
-----------------------
* SCOUT_MODE_USER - Scout is executed in User-Mode
* SCOUT_MODE_KERNEL - Scout is executed in Kernel-Mode

Only one of above flags can be defined.
If none are defined the base library will define "SCOUT_MODE_USER" on it's own.

**Note:** These flags are used only in a Linux PC Environment, and are not used in an Embedded Environment.

Target Loading Environment
--------------------------
* SCOUT_PC_ENV - Scout is executed as a standard process (user) or driver (kernel) on a Linux machine
* SCOUT_EMBEDDED_ENV - Scout is injected to the address space of a given executable

Only one of above flags can be defined.
If none are defined the base library will define "SCOUT_PC_ENV" on it's own.

**Note:** SCOUT_EMBEDDED_ENV has many use cases, including:
1. Injecting a debugger into a debuggee Linux process
2. Injecting a debugger into a debuggee firmware (if the executable's API matches the basic POSIX based API of Scout)

**Note:** At the current moment, "SCOUT_EMBEDDED_ENV" must be used with "SCOUT_PIC_CODE", although in the future a linker script could help an embedded scout access external functions without the PIC context.

Position Independent Mode - SCOUT_PIC_CODE
------------------------------------------
Scout will be compiled for full Position Independent Code (PIC) mode. Any access to an external function / global variable will pass through a unique "Context" object. Read the section about "PIC Compilation" for more information.
**Note:** Can only be used with "SCOUT_EMBEDDED_ENV".

Loader Flags
------------
* SCOUT_LOADER - We are now compiling a loader (that might be using it's own pic plt / globals).
* SCOUT_LOADING_THUMB_CODE - The loader will load a Scout that was compiled to be executed on an ARM cpu in Thumb mode.
* SCOUT_RESTORE_FLOW - The default loaders (```tcp_client_server.c```, ```tcp_loader_server.c```) will clean-up after themselves if the loaded scout will finish his endless loop.

Additional Flags:
-----------------
* SCOUT_INSTRUCTIONS - Scout is going to use the instructions api (using the TCP server for instance)
* SCOUT_DYNAMIC_BUFFERS - Scout will dynamically malloc() buffers to be used by the tcp server. Otherwise static buffers will be used.
* SCOUT_PROXY - Scout is going to act as a proxy (user scout passing instructions to a kernel driver for instance)
* SCOUT_MMAP - Should scout's loaders use mmap() and mprotect() when loading (if defined) or should they simply use malloc (if undefined)
