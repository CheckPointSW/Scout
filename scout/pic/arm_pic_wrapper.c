#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_PIC_CODE
#ifdef SCOUT_ARCH_ARM

/*
 * Thumb mode (SCOUT_ARM_THUMB) has limitations
 * and it mandates the order of the functions in this file.
 */

/* Compilation on an intel ubuntu machine, with arm-gcc */
//#define ELF_START           (0x00008000)
/* Compilation on a raspberry pi */
//#define ELF_START           (0x00010074)

#ifndef ELF_START
    #error "\"ELF_START\" symbol is missing! Should be defined to the address of the \"_start\ function in the ELF."
#endif /* ELF_START */

#ifdef SCOUT_ARM_THUMB
#define STATIC_FUNC_ADDR    (ELF_START + 0x10)  // It sounds wierd, but with +0xC it had an offset of 4 bytes...
#else
#define STATIC_FUNC_ADDR    (ELF_START + 0x10)
#endif /* SCOUT_ARM_THUMB */

void _start()
{
    scout_main();
}

void * get_live_address(const void * address)
{
#ifdef SCOUT_ARM_THUMB
#ifdef SCOUT_BITS_32
    asm("mov    r1, pc              ");
    asm("mov    r0, %0              " : : "r" (address));
    asm("sub    r0, %0              " : : "r" (STATIC_FUNC_ADDR));
    asm("add    r0, r1              ");
#else  /* SCOUT_BITS_64 */
    #error "Currently ARM 64bit is not supported :("
#endif /* SCOUT_BITS_32 */
#else
#ifdef SCOUT_BITS_32
    asm("adr    r1, _start          ");
    asm("mov    r0, %0              " : : "r" (address));
    asm("sub    r0, %0              " : : "r" (ELF_START));
    asm("add    r0, r1              ");
#else  /* SCOUT_BITS_64 */
    #error "Currently ARM 64bit is not supported :("
#endif /* SCOUT_BITS_32 */
#endif /* SCOUT_ARM_THUMB */
}

pic_context_t * get_context()
{
#ifdef SCOUT_BITS_32
    asm("adr    r0, CONTEXT_LABEL   ");
#else  /* SCOUT_BITS_64 */
    #error "Currently ARM 64bit is not supported :("
#endif /* SCOUT_BITS_32 */
}

void dummy_context()
{
    asm("CONTEXT_LABEL:  ");
    asm(".int  0x11222211"); /* Start marker */
    asm(".space %0, 0    " : : "n"(sizeof(pic_context_t) - 2 * 4));
    asm(".int  0x33444433"); /* End marker   */
}

#endif /* SCOUT_ARCH_ARM */
#endif /* SCOUT_PIC_CODE */
