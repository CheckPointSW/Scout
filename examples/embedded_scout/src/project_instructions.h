#ifndef __SCOUT__EMBEDDED__INSTRUCTIONS__H__
#define __SCOUT__EMBEDDED__INSTRUCTIONS__H__

#include "scout/scout_api.h"

/******************************/
/*  Instruction Status Codes  */
/******************************/

/* Scout API Statuses */
#define STATUS_INVALID_FREE          30

/*******************************/
/*  Instructions Registration  */
/*******************************/

/**
 * This is the function that will be used by scout_api.c
 * 
 * @author eyalit (06/05/2018)
 */
void register_specific_instructions(void);

/***************************/
/*  Embedded Instructions  */
/***************************/

#define EMBEDDED_INST_COUNT_BASE     (SCOUT_MAX_BASIC_INSTR + 1)
#define EMBEDDED_INST_ALLOC          (EMBEDDED_INST_COUNT_BASE + 0)
#define EMBEDDED_INST_FREE           (EMBEDDED_INST_COUNT_BASE + 1)

/**
 * Memory allocation instruction
 * 
 * @author eyalit (06/05/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int32_t instruction_alloc(void * ctx, uint8_t * instruction, uint32_t length);

/**
 * Memory de-allocation (free) instruction
 * 
 * @author eyalit (06/05/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int32_t instruction_free(void * ctx, uint8_t * instruction, uint32_t length);

/* The instruction records */
#define INSTR_ALLOC_MIN_SIZE (sizeof(uint32_t))
#define INSTR_ALLOC_MAX_SIZE (sizeof(uint32_t))
#define INSTR_ALLOC_HANDLER  instruction_alloc

#define INSTR_FREE_MIN_SIZE (sizeof(addr_t))
#define INSTR_FREE_MAX_SIZE (sizeof(addr_t))
#define INSTR_FREE_HANDLER  instruction_free

#endif // __SCOUT__EMBEDDED__INSTRUCTIONS__H__