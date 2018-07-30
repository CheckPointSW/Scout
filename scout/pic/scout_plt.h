#ifndef __SCOUT__PIC__PLT__H__
#define __SCOUT__PIC__PLT__H__

#include "scout/scout.h"

#ifdef SCOUT_PIC_CODE

/***************/
/**  Structs  **/
/***************/

#pragma pack(1)
typedef struct __pic_got
{
    /* LibC */
    addr_t      memcpy;
    addr_t      memset;
    addr_t      malloc;
    addr_t      free;
    /* Sockets */
    addr_t      socket;
    addr_t      bind;
    addr_t      listen;
    addr_t      accept;
    addr_t      connect;
    addr_t      recv;
    addr_t      send;
    addr_t      close;
} pic_got_t;

#endif /* SCOUT_PIC_CODE */

#endif // __SCOUT__PIC__PLT__H__
