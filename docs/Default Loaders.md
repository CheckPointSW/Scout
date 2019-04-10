Scout's Loader
==============
Embedded debuggers often require an initial code execution vulnerability, that will load up the debugger (instead of using a normal "shellcode"). Exploits for such vulnerabilities are often limited:
1. Size limits on the controlled input
2. Forbidden chars that must not be used

To overcome these limitations, the scout debugger comes with a list of supported default loaders. These loaders are self-contained and are compiled to a smaller memory footprint that the entire scout debugger (especially in case there are project specific extensions to the debugger).

The defualt loaders are:

1. ```tcp_client_loader.c``` - Connects to a predefined TCP server
2. ```tcp_server_loader.c``` - Waits for an incoming TCP client

Both of the loaders use the same network protocol:

* header - 4 bytes of length field (in network order, i.e. Big Endian)
* data - X bytes of data (X is the value that was sent in the header)

After a TCP connection was established, the loader will follow these steps:

1. The loader will receive the header and malloc() a memory buffer of appropriate size.
2. The data will be received and stored in this memory buffer.
3. The loader will flush the D-cache and I-cache of the buffer (only in architectures were this is needed)
4. The loader will mprotect() the memory to use the correct permissions (only in architectures were this is needed)
5. The loader will jump into the buffer's start (offset 0, as mentioned in the "PIC Compilation" section)
6. In the flow restore case, once the loaded executable finishes the loader will free the memory and close the used sockets.

The functions ```remoteLoadServer()``` and ```remoteLoadClient()``` in ```scout_network.py```, implement the required protocol for communicating with the loader, and loading up the full Scout.

**Note:** In case there are any W^X style limitations in your environment, it is recommended to make sure that the allocated memory for the full debugger will have both Write and eXcutable permissions (should probably use the SCOUT_MMAP flag in this case).
