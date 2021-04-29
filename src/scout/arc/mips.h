#ifndef __SCOUT__ARC__MIPS__H__
#define __SCOUT__ARC__MIPS__H__

#include "scout/scout.h"

#ifdef SCOUT_ARCH_MIPS

/*****************/
/**  Functions  **/
/*****************/

/**
 * Flushes the caches (D-Cache and I-Cache) for the given buffer
 *
 * @author eyalit (29/08/2019)
 *
 * @param buffer - pointer to flushed buffer
 * @param size - size in bytes of the given buffer
 *
 */
void flush_cache(uint8_t * buffer, uint32_t size);

#endif /* SCOUT_ARCH_MIPS */
#endif /* __SCOUT__ARC__MIPS__H__ */