#ifndef __SCOUT__ARC__INTEL__H__
#define __SCOUT__ARC__INTEL__H__

#include "scout/scout.h"

#ifdef SCOUT_ARCH_INTEL

/*****************/
/**  Functions  **/
/*****************/

/**
 * Flushes the caches (D-Cache and I-Cache) for the given buffer
 * 
 * @author eyalit (01/04/2018)
 * 
 * @param buffer - pointer to flushed buffer
 * @param size - size in bytes of the given buffer
 * 
 */
void flush_cache(uint8_t * buffer, uint32_t size);

#endif /* SCOUT_ARCH_INTEL */
#endif /* __SCOUT__ARC__INTEL__H__ */
