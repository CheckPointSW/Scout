#ifndef __SCOUT__H__
#define __SCOUT__H__

#include "flags.h"                /* Project defined, must come first */
#include "scout/architecture.h"   /* Important architecture defines */
#include "scout/errors.h"         /* Error statuses */

#ifdef SCOUT_PIC_CODE
#include "scout/pic/pic_wrapper.h"
#else
#define GLOBAL(_V_)     g##_V_
#endif /* SCOUT_PIC_CODE */

#ifdef SCOUT_ISOLATED_ENV

#include "scout/external_deps.h"  /* All external dependencies that should be found in libraries on a PC */

#else /* !SCOUT_ISOLATED_ENV */

#ifdef SCOUT_USER_MODE
#include <stdlib.h>
#include <string.h>
#else
#include <linux/string.h>
#endif /* SCOUT_USER_MODE */

#endif /* SCOUT_ISOLATED_ENV */

#endif // __SCOUT__H__