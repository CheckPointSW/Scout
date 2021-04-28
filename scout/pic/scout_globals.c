#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_PIC_CODE

#ifdef SCOUT_INSTRUCTIONS
/* Scout API */
uint32_t * global_pNumInstructions()
{
    return &get_context()->globals.scout.numInstructions;
}

scout_instruction_t * global_Instructions()
{
    return get_context()->globals.scout.instructions;
}

#ifndef SCOUT_DYNAMIC_BUFFERS
/* TCP server */
uint8_t * global_RecvBuffer()
{
    return get_context()->globals.scout.recvBuffer;
}

uint8_t * global_SendBuffer()
{
    return get_context()->globals.scout.sendBuffer;
}
#endif /* ! SCOUT_DYNAMIC_BUFFERS */

#endif /* SCOUT_INSTRUCTIONS */

#endif /* SCOUT_PIC_CODE */