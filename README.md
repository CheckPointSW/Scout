
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
                                             
## Purpose
"Scout" is an extendable basic debugger that was designed for use in those cases that there is no built-in debugger / gdb-stub in the debugee process / firmware. The debugger is intended to be used by security researchers in various scenarios, such as:
1. Collecting information on the address space of the debuggee - recon phase and exploit development
2. Exploring functionality of the original executable by accessing and executing selected code snippets
3. Adding and testing new functionality using custom debugger instructions

We have successfully used "Scout" as a debugger in a Linux Kernel setup, and in several embedded firmware research projects, and so we believe that it's extendable API could prove handy for other security researchers in their research projects.

## Read The Docs
https://scout-debugger.readthedocs.io/

### Supported Architectures
* x86 - Intel 32 bit
* x64 - Intel 64 bit
* ARM  32 bit - Little & Big endian (Including Thumb mode)
* MIPS 32 bit - Little & Big endian (Without Mips16 mode)

##### Future Architectures
* ARM  64 bit - Little & Big endian
* MIPS 16 bit - Little & Big endian
* MIPS 64 bit - Little & Big endian
* ...

### Supported Operating Systems
* Linux - User-mode (PC Mode)
* Linux - Kernel-mode (PC Mode)
* Any Posix-like operating system (Embedded Mode)

## Folder Structure
* **docs:** Useful tutorials regarding each unique module of the debugger, including documentation of the API used for custom extensions
* **embedded_scout:** Example project for an embedded debugger scenario, i.e. a debugger that is injected into the address space of a debuggee firmware
* **kernel_scout:** Linux kernel driver-based debugger, including a proxy user mode process used for transparent network access
* **manager:** Python layer for communicating with the debuggee (usually over a TCP connection)
* **scout:** C code of the basic scout debugger
* **tests:** A testing utility for PIC based debuggers
* **utils:** Useful python compilation scripts

## Credits
This projects combines together design and compilation tricks that I learned from many fellow researchers during the years.

## Links
Scout was developed and used in our following research projects:
* [Check Point Research - RCE over the FAX protocol](https://research.checkpoint.com/sending-fax-back-to-the-dark-ages)
* [Check Point Research - Say Cheese - Ransomware-ing A DSLR Camera](https://research.checkpoint.com/say-cheese-ransomware-ing-a-dslr-camera)
* [Check Point Research - Don't be Silly - It's Only a Lightbulb](https://research.checkpoint.com/2020/dont-be-silly-its-only-a-lightbulb/)
* [Check Point Research - Would you like some RCE with your Guacamole?](https://research.checkpoint.com/2020/apache-guacamole-rce/)
* [Check Point Research - Linux Kernel MMap vulnerabilities](https://research.checkpoint.com/mmap-vulnerabilities-linux-kernel)

## Contact
Eyal Itkin (eyalit at checkpoint dot com)

[@EyalItkin](https://twitter.com/EyalItkin)
