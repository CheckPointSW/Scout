#include "scout/arc/intel.h"
#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_ARCH_INTEL

void flush_cache(uint8_t * buffer, uint32_t size)
{
    (void)buffer;
    (void)size;

    /* Intel has no caches that we need to flush :) */
}

#endif /* SCOUT_ARCH_INTEL */
