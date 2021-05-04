#include "scout/arc/mips.h"

#ifdef SCOUT_ARCH_MIPS

void flush_cache(uint8_t * buffer, uint32_t size)
{
#if defined(SCOUT_HIGH_PRIVILEGES)
    #error "Not supported yet. Had no way to check if it works :("
#else
    /* No permissions to perform these operations :( */
#endif
}

#endif /* SCOUT_ARCH_MIPS */
