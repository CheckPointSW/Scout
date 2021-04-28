#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_PIC_CODE
#ifdef SCOUT_ARCH_INTEL

void _start()
{
    asm("jmp   code_start");
    asm("CONTEXT_LABEL:  ");
    asm(".int  0x11222211"); /* Start marker */
    asm(".space %0, 0"    : : "n"(sizeof(pic_context_t) - 2 * 4));
    asm(".int  0x33444433"); /* End marker   */
}

addr_t get_pc()
{
#ifdef SCOUT_BITS_32
    asm("movl    4(%esp), %eax"); /* GCC Adds "push %ebp" to the start of our function */
#else  /* SCOUT_BITS_64 */
    asm("movq    (%rsp), %rax");
#endif /* SCOUT_BITS_32 */
}

pic_context_t * get_context()
{
#ifdef SCOUT_BITS_32
    asm("push   %ebx                 ");
    asm("push   %ecx                 ");
    asm("lea    CONTEXT_LABEL, %ebx  ");
    asm("call   get_pc               ");
    asm("MEASURE_LABEL1:             ");
    asm("lea    MEASURE_LABEL1, %ecx ");
    asm("sub    %ecx, %ebx           ");
    asm("add    %ebx, %eax           ");
    asm("pop    %ecx                 ");
    asm("pop    %ebx                 ");
#else  /* SCOUT_BITS_64 */
    /* Function pointers are stored in a PIC fashion by default in 64 bits */
    asm("movq   %0, %%rax            " : : "r" ((addr_t)address));
#endif /* SCOUT_BITS_32 */
}

void * get_live_address(const void * address)
{
#ifdef SCOUT_BITS_32
    asm("push   %ebx                 ");
    asm("push   %ecx                 ");
    asm("movl   %0, %%ebx            " : : "r" ((addr_t)address));
    asm("call   get_pc               ");
    asm("MEASURE_LABEL2:             ");
    asm("lea    MEASURE_LABEL2, %ecx ");
    asm("sub    %ecx, %ebx           ");
    asm("add    %ebx, %eax           ");
    asm("pop    %ecx                 ");
    asm("pop    %ebx                 ");
#else  /* SCOUT_BITS_64 */
    asm("push   %rbx                 ");
    asm("push   %rcx                 ");
    asm("movq   %0, %%rbx            " : : "r" ((addr_t)address));
    asm("call   get_pc               ");
    asm("MEASURE_LABEL2:             ");
    asm("lea    MEASURE_LABEL2, %rcx ");
    asm("sub    %rcx, %rbx           ");
    asm("add    %rbx, %rax           ");
    asm("pop    %rcx                 ");
    asm("pop    %rbx                 ");
#endif /* SCOUT_BITS_32 */
}

void code_start()
{
    main();
}

#endif /* SCOUT_ARCH_INTEL */
#endif /* SCOUT_PIC_CODE */