#include "scout/arc/arm.h"

#ifdef SCOUT_ARCH_ARM

void flush_cache(uint8_t * buffer, uint32_t size)
{
#if defined(SCOUT_HIGH_PRIVILEGES)
    asm("    MOV             R2, R0                                                       ");
    asm("    ADR             R0, flush_cache_inner                                        ");
    asm("    BX              R0                                                           ");
    /* Flush the D-cache */
#ifdef SCOUT_ARM_THUMB
    asm(".arm");
#endif /* SCOUT_ARM_THUMB */
    asm(" flush_cache_inner:                                                              ");
    asm("    MOV             R0, #0xFFFFFFE0                                              ");
    asm("    AND             R0, R0, R2              ;# R0 := aligned buffer              ");
    asm("    ADD             R1, R2                  ;# R1 := buffer's end                ");
    asm("dcache_loop:                                                                     ");
    asm("    MCR             p15, 0, R0, c7, c14, 1  ;# Clean and Flush the line (DCache) ");
    asm("    ADD             R0, R0, #0x20           ;# Rd = Op1 + Op2                    ");
    asm("    CMP             R0, R1                  ;# Set cond. codes on Op1 - Op2      ");
    asm("    BLT             dcache_loop             ;# Branch                            ");

    /* Flush the (entire) I-cache */
    asm("    MOV             R0, #0                                                       ");
    asm("    MCR             p15, 0, R0, c7, c5, 0   ;# Flush entire ICache               ");

    /* return */
    asm("    BX              LR                                                           ");
#else
    /* No permissions to perform these operations :( */
#endif
}

#endif /* SCOUT_ARCH_ARM */
