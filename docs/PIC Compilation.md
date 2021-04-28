Position Independent Code (PIC) Mode
====================================
In PIC mode Scout is no longer loaded using the native loader of the operating system, since it is injected into a running executable. This means that Scout is compiled to be fully independent, enabling it to work no matter where it was injected to.

Entry Point
-----------
The entry point to our executable blob is at offset 0, meaning that we can literally jump into our buffer's start.

**IMPORATNT:** This can only be achieved if the ```*_pic_wrapper.c``` file will be linked as the FIRST file in the list of files. In case there are any errors it is always recommended to check if the compiled files were compiled in a different order.

From the project's point of view, the main function is called ```main``` (as usual), since this is the function that will be executed by the start stub at offset 0.

The Context
-----------
The PIC Context consists of 4 parts:
* Base scout "PLT"
* Project "PLT"
* Base scout "Globals"
* Project "Globals"

The code is compiled so that any call to an external function (library call) will pass through an indirection layer (named after the ELF's "PLT"). This "PLT" will locate Scout's context object, and will lookup the wanted address in the context's "GOT".

In a similar fashion, the code is compiled (and developed) so that any access to a global variable will pass through an indirection layer. This layer will locate the scout's context object, and will find the offset of the global variable inside the PIC context.

Locating the Context
--------------------
Our code can be compiled so that it will access the PIC context instead of being linked as an ordinary ELF. Now we only need to tell our code how to be able to locate the context's address in runtime, using a PIC way. The context itself will be embedded INSIDE the full executed binary blob, so that it will be stored in a known relative offset from our code. The final step of deriving the absolute address of the context will be solved using an assembly layer: ```*_pic_wrapper.c```.

**Important Note:** Locating the context is done in assembly, hence this is the only part that depends on the architecture on which we will be executed.

Expanding the Context
---------------------
In order to be able to use additional symbols (functions) or globals (global variables), we need to add them to the respective ```project_plt.c``` and ```project_globals.c``` files, accordingly. Please make sure that the compilation script will be notified of these additions, so that the GOT will contain the needed addresses and the globals section will be of the correct size.

Testing - exploit_me
--------------------
The ```exploit_me.c``` module in the testing folder lets you test your PIC scout (with / without a loader). As you can see in the "Known Gaps" section (point 2), it is recommended that the test will be done on a setup that contains RWX environments (Linux VMs without the NX bit exposed, for instance).

Known Gaps
----------
1) In PIC mode our globals will need to be initialized manually as we will have no "init" methods that will be executed before our main function.
2) RWX flags: Since the context is embedded inside the compiled binary, that has executable (X) permissions, it means that the PIC Scout assumes it is loaded into a memory area with RWX permissions so to be able to update global variables.