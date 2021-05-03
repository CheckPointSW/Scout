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
    asm("lea    CONTEXT_LABEL, %eax  ");
    asm("call   get_live_address     ");
#else  /* SCOUT_BITS_64 */
    asm("lea    CONTEXT_LABEL, %rdi  ");
    asm("call   get_live_address     ");
#endif /* SCOUT_BITS_32 */
}

void * get_live_address(const void * address)
{
#ifdef SCOUT_BITS_32
    asm("movl   %0, %%edx            " : : "r" ((addr_t)address));
    asm("call   get_pc               ");
    asm("MEASURE_LABEL1:             ");
    asm("lea    MEASURE_LABEL1, %ecx ");
    asm("sub    %ecx, %edx           ");
    asm("add    %edx, %eax           ");
#else  /* SCOUT_BITS_64 */
    asm("movq   %0, %%rdx            " : : "r" ((addr_t)address));
    asm("call   get_pc               ");
    asm("MEASURE_LABEL1:             ");
    asm("lea    MEASURE_LABEL1, %rcx ");
    asm("sub    %rcx, %rdx           ");
    asm("add    %rdx, %rax           ");
#endif /* SCOUT_BITS_32 */
}

void code_start()
{
    main();
}

#endif /* SCOUT_ARCH_INTEL */
#endif /* SCOUT_PIC_CODE */
