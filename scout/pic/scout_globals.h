#ifndef __SCOUT__PIC__GLOBALS__H__
#define __SCOUT__PIC__GLOBALS__H__

#include "scout/scout.h"

#ifdef SCOUT_PIC_CODE

#include "scout/scout_api.h"
#include "scout/tcp_server.h"

/**************/
/**  MACROS  **/
/**************/

#define GLOBAL(_V_)     global_##_V_()

/***************/
/**  Structs  **/
/***************/

typedef struct __pic_globals
{
#ifdef SCOUT_INSTRUCTIONS
    /* Scout API */
    uint32_t            numInstructions;
    scout_instruction_t instructions[SCOUT_MAX_INSTRS];
#ifndef SCOUT_DYNAMIC_BUFFERS
    /* TCP Server */
    uint8_t             recvBuffer[SCOUT_HEADER_SIZE + SCOUT_TCP_MAX_MESSAGE];
    uint8_t             sendBuffer[SCOUT_TCP_MAX_MESSAGE];
#endif /* ! SCOUT_DYNAMIC_BUFFERS */
#endif /* SCOUT_INSTRUCTIONS */
} pic_vars_t;

#ifdef SCOUT_INSTRUCTIONS
/* Scout API */
extern uint32_t * global_pNumInstructions();
extern scout_instruction_t * global_Instructions();

#ifndef SCOUT_DYNAMIC_BUFFERS
/* TCP server */
extern uint8_t * global_RecvBuffer();
extern uint8_t * global_SendBuffer();
#endif /* ! SCOUT_DYNAMIC_BUFFERS */

#endif /*  SCOUT_INSTRUCTIONS */

#endif /* SCOUT_PIC_CODE */

#endif // __SCOUT__PIC__GLOBALS__H__
