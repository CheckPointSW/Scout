.. Scout documentation master file, created by
   sphinx-quickstart on Wed Apr 10 10:04:29 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: User Guide:
   :hidden:

   User Guide
   
.. toctree::
   :maxdepth: 2
   :caption: Compilation Modes:
   :hidden:

   Compilation Modes
   PIC Compilation
   
.. toctree::
   :maxdepth: 2
   :caption: Scout Instructions:
   :hidden:

   Default Instructions
   Adding Custom Instructions
   
.. toctree::
   :maxdepth: 2
   :caption: Loaders:
   :hidden:

   Default Loaders
   
..
   
::

      ______                                   __
     /      \                                 /  |                                  
    /$$$$$$  |  _______   ______   __    __  _$$ |_                                 
    $$ \__$$/  /       | /      \ /  |  /  |/ $$   |                                
    $$      \ /$$$$$$$/ /$$$$$$  |$$ |  $$ |$$$$$$/                                 
     $$$$$$  |$$ |      $$ |  $$ |$$ |  $$ |  $$ | __                               
    /  \__$$ |$$ \_____ $$ \__$$ |$$ \__$$ |  $$ |/  |                              
    $$    $$/ $$       |$$    $$/ $$    $$/   $$  $$/                               
     $$$$$$/   $$$$$$$/  $$$$$$/   $$$$$$/     $$$$/                                
                                               
     _______             __                                                         
    /       \           /  |                                                        
    $$$$$$$  |  ______  $$ |____   __    __   ______    ______    ______    ______  
    $$ |  $$ | /      \ $$      \ /  |  /  | /      \  /      \  /      \  /      \ 
    $$ |  $$ |/$$$$$$  |$$$$$$$  |$$ |  $$ |/$$$$$$  |/$$$$$$  |/$$$$$$  |/$$$$$$  |
    $$ |  $$ |$$    $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
    $$ |__$$ |$$$$$$$$/ $$ |__$$ |$$ \__$$ |$$ \__$$ |$$ \__$$ |$$$$$$$$/ $$ |      
    $$    $$/ $$       |$$    $$/ $$    $$/ $$    $$ |$$    $$ |$$       |$$ |      
    $$$$$$$/   $$$$$$$/ $$$$$$$/   $$$$$$/   $$$$$$$ | $$$$$$$ | $$$$$$$/ $$/       
                                            /  \__$$ |/  \__$$ |                    
                                            $$    $$/ $$    $$/                     
                                             $$$$$$/   $$$$$$/
                                             

Brief
=====
"Scout" is an extendable basic debugger that was designed for use in those cases that there is no built-in debugger / gdb-stub in the debugee process / firmware. The debugger is intended to be used by security researchers in various scenarios, such as:

1. Collecting information on the address space of the debuggee - recon phase and exploit development
2. Exploring functionality of the original executable by accessing and executing selected code snippets
3. Adding and testing new functionality using custom debugger instructions

We have successfully used "Scout" as a debugger in a Linux Kernel setup, and in an several embedded firmware research projects, and so we believe that it's extendable API could prove handy for other security researchers in their research projects.

Supported Architectures
-----------------------
* x86 - Intel 32 bit
* x64 - Intel 64 bit
* ARM  32 bit - Little & Big endian (Including Thumb mode)
* MIPS 32 bit - Little & Big endian (Without Mips16 mode)

**Future Architectures**

* ARM  64 bit - Little & Big endian
* MIPS 16 bit - Little & Big endian
* MIPS 64 bit - Little & Big endian
* ...

Supported Operating Systems
---------------------------
* Linux - User-mode (PC Mode)
* Linux - Kernel-mode (PC Mode)
* Any Posix-like operating system (Embedded Mode)

Credits
-------
This projects combines together design and compilation tricks that I learned from many fellow researchers during the years.

Links
-----
* Original   repository - https://github.com/CheckPointSW/Scout
* Maintained repository - https://github.com/eyalitki/Scout

Scout was used in our following research projects:

* https://research.checkpoint.com/sending-fax-back-to-the-dark-ages
* https://research.checkpoint.com/say-cheese-ransomware-ing-a-dslr-camera
* https://research.checkpoint.com/2020/dont-be-silly-its-only-a-lightbulb/
* https://research.checkpoint.com/2020/apache-guacamole-rce/
* https://research.checkpoint.com/mmap-vulnerabilities-linux-kernel

Contact
-------
* `@EyalItkin <https://twitter.com/EyalItkin>`_ 
