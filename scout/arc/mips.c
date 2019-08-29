#include "scout/arc/mips.h"
#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_ARCH_MIPS

void flush_cache(uint8_t * buffer, uint32_t size)
{
#if defined(SCOUT_MODE_KERNEL) || defined(SCOUT_EMBEDDED_ENV)
    #error "Not supported yet. Had no way to check if it works :("
#else
    /* No permissions to perform these operations :( */
#endif
}

#endif /* SCOUT_ARCH_MIPS */
