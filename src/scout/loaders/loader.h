#ifndef __SCOUT__LOADER__H__
#define __SCOUT__LOADER__H__

#include "scout/scout.h"

#ifdef SCOUT_LOADER

/***************/
/**  Defines  **/
/***************/

#if defined(SCOUT_LOADING_THUMB_CODE)
#define PAYLOAD_START(_X_)  ((_X_) + 1)
#else
#define PAYLOAD_START(_X_)  (_X_)
#endif /* SCOUT_LOADING_THUMB_CODE */

#define INVOKE_PAYLOAD(_X_) ((void (*)(void))PAYLOAD_START(_X_))()

#endif /* SCOUT_LOADER */
#endif /* __SCOUT__LOADER__H__ */
