#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_PIC_CODE
#ifdef SCOUT_ARCH_MIPS

/* Compilation on an intel ubuntu machine, with mips-gcc */
#define ELF_START           (0x004000D0)

#ifndef ELF_START
    #error "\"ELF_START\" symbol is missing! Should be defined to the address of the \"__start\ function in the ELF."
#endif /* ELF_START */

void __start()
{
    scout_main();
}

addr_t get_pc()
{
    asm("move   $v0, $ra              ");
}

void * get_live_address(const void * address)
{
#ifdef SCOUT_BITS_32
    asm("sw     $ra, -0x4($sp)        ");
    asm("\tjal\tget_pc                ");
    asm("move   $v1, $v0              ");
    asm("subu   $v1, 0x1C             ");
    asm("move   $v0, %0               " : : "r" (ELF_START));
    asm("subu   $v0, $a0, $v0         ");
    asm("addu   $v0, $v1              ");
    asm("lw     $ra, -0x4($sp)        ");
    asm("nop                          ");
#else  /* SCOUT_BITS_64 */
    #error "Currently MIPS 64bit is not supported :("
#endif /* SCOUT_BITS_32 */
}

pic_context_t * get_context()
{
#ifdef SCOUT_BITS_32
    asm("sw     $ra, -0x4($sp)        ");
    asm("\tjal\tget_pc                ");
    asm("addu   $v0, 0x10             ");
    asm("lw     $ra, -0x4($sp)        ");
    asm("jr     $ra                   ");
#else  /* SCOUT_BITS_64 */
    #error "Currently MIPS 64bit is not supported :("
#endif /* SCOUT_BITS_32 */
    asm("CONTEXT_LABEL:  ");
    asm(".int  0x11222211"); /* Start marker */
    asm(".space %0, 0    " : : "n"(sizeof(pic_context_t) - 2 * 4));
    asm(".int  0x33444433"); /* End marker   */
}

#endif /* SCOUT_ARCH_MIPS */
#endif /* SCOUT_PIC_CODE */
