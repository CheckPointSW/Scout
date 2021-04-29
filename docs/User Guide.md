User Guide
==========
Scout consists of two main parts:

1. Server Side - C code
2. Client Side - Python code

The server is the debugger that is being sent / injected into the debugee, and the client is the user API that issues the instructions.

Folder Structure
----------------
* docs - This documentation
* examples
  * embedded_scout - Use case example for an "Embedded Mode" compilation
  * kernel_scout - Use case example for a Linux "Kernel Mode" compilation
* src
  * scout - Source code for the debugger (core of the server side)
  * utils - Python compilation scripts and network API for the client/server
* tests - A simple exploit_me.c for checking PIC compiled binaries


**Note:** More information on the different compilation modes can be found under the "Compilation Modes" section.

Beginner's Guide
----------------
When deploying Scout for a new research project, we recommend to pick the suitable use case out of the two examples. Both the "Embedded Mode" and the Linux "Kernel Mode" use case examples are supplied so that they will serve as templates for new projects.

The project part of the server side consists of the following parts:

* Main (Init) code - Only needed in the Embedded Mode
* Project Instructions - When adding custom instructions
* Loader PIC - globals / plt for the loader in an Embedded Mode
* Project PIC - globals / plt for the project's extensions in an Embedded Mode
* Compilation Script - ```compile_scout.py``` with the compile instructions