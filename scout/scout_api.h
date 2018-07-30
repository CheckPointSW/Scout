#ifndef __SCOUT__API__H__
#define __SCOUT__API__H__

#include "scout/architecture.h" // There is a dependency issue in PIC mode, so we can't include "scout.h" yet
#include <stdbool.h>

#ifdef SCOUT_INSTRUCTIONS

/*****************************/
/**  API defined functions  **/
/*****************************/

/**
 * Appends the given data to the output (data) stream
 * 
 * @author eyalit (07/03/2018)
 *  
 * @param ctx - general context 
 * @param buffer - data to be appended to the output
 * @param length - number of bytes in the data buffer
 */
void write_output(void * ctx, uint8_t * buffer, uint32_t length);

/**
 * Marks the success status of the command and writes it to the 
 * (control) stream 
 * 
 * @author eyalit (07/03/2018)
 *  
 * @param ctx - general context 
 * @param status - command success status
 */
void mark_status(void * ctx, int32_t status);

/***************/
/**  Structs  **/
/***************/

typedef struct __scout_header
{
    uint16_t instrID;
    uint32_t length;
} scout_header_t;

typedef int32_t (*instrHandler)(void * ctx, uint8_t * instruction, uint32_t length);

typedef struct __scout_instruction
{
    uint16_t        instrID;
    uint32_t        minLength;
    uint32_t        maxLength;
    instrHandler    handler;
} scout_instruction_t;

/***************/
/**  Defines  **/
/***************/

#define SCOUT_HEADER_SIZE   (sizeof(uint16_t) + sizeof(uint32_t))
#define SCOUT_MAX_INSTRS    (10)

#include "scout/scout.h" // Now we can safely include this file, even in PIC mode

/******************************/
/**  Instruction Processing  **/
/******************************/

/**
 * Parses the command's header from the raw buffer
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param buffer - raw command buffer
 * @param length - length in bytes of the raw command buffer
 * @param header - commadn header struct to be initialized 
 *  
 * @return int32_t - success status
 */
int32_t parse_header(uint8_t * buffer, uint32_t length, scout_header_t * header, bool validateLen);

/**
 * Verifies and Handles the given instruction
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param ctx - general context
 * @param header - scout header as extracted from the buffer
 * @param buffer - instruction raw buffer
 * 
 * @return int32_t - success status
 */
int32_t handle_instruction(void * ctx, scout_header_t * header, uint8_t * buffer);

#ifdef SCOUT_PROXY
/**
 * Passes the instruction to the real instruction handler
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param ctx - general context
 * @param header - scout header as extracted from the buffer
 * @param buffer - instruction raw buffer
 * 
 * @return int32_t - success status
 */
int32_t proxy_handle_instruction(void * ctx, scout_header_t * header, uint8_t * buffer);
#endif /* SCOUT_PROXY */

/********************************/
/**  Instruction Registration  **/
/********************************/

/**
 * Retrieves the number of registerred instructions
 * 
 * @author eyalit (07/03/2018)
 * 
 * @return uint16_t - number of registerred instruction
 */
uint16_t get_instruction_count(void);

/**
 * Retrieves the instruction at the given index
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param index - index of the wanted instruction
 * 
 * @return scout_instruction_t * - pointer to the wanted 
 *         instruction (NULL in case of error)
 */
scout_instruction_t * get_instruction(uint16_t index);

/**
 * Registers the given instructions. 
 * Assumption:
 *  The operation will silently fail if the maximum number of
 *  instructions was already reached.
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param instrID - instruction ID
 * @param minLength - minimal instruction input length
 * @param maxLength - maximal instruction input length
 * @param handler - handler for the instruction
 */
void register_instruction(uint16_t instrID, uint32_t minLength, uint32_t maxLength, instrHandler handler);

/**
 * Registers all of the basic instructions
 * 
 * @author eyalit (07/03/2018)
 */
void register_basic_instructions(void);

/**
 * Registers the project specific instructions.
 * NOTE:
 * Should be implemented by the project
 * 
 * @author eyalit (06/05/2018)
 */
void register_specific_instructions(void);

/**
 * Registers all of the instructions
 * 
 * @author eyalit (06/05/2018)
 */
void register_all_instructions(void);

/**************************/
/**  Basic Instructions  **/
/**************************/

#define SCOUT_INST_NOP          0
#define SCOUT_INST_MEM_READ     1
#define SCOUT_INST_MEM_WRITE    2

#define SCOUT_MAX_BASIC_INSTR   SCOUT_INST_MEM_WRITE

/**
 * The NOP instruction - does nothing, returns OK.
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int32_t instruction_nop(void * ctx, uint8_t * instruction, uint32_t length);

/**
 * Reads basic memory (usually virtual RAM memory) and writes it 
 * to the output. 
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int32_t instruction_mem_read(void * ctx, uint8_t * instruction, uint32_t length);

/**
 * Basic memory update (usually virtual RAM memory) with given 
 * input. 
 * 
 * @author eyalit (07/03/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int32_t instruction_mem_write(void * ctx, uint8_t * instruction, uint32_t length);

/* The instruction records */
#define INSTR_NOP_MIN_SIZE 0
#define INSTR_NOP_MAX_SIZE 0
#define INSTR_NOP_HANDLER  instruction_nop

#define INSTR_MEM_READ_MIN_SIZE (sizeof(addr_t) + sizeof(uint32_t))
#define INSTR_MEM_READ_MAX_SIZE (sizeof(addr_t) + sizeof(uint32_t))
#define INSTR_MEM_READ_HANDLER  instruction_mem_read

#define INSTR_MEM_WRITE_MIN_SIZE (sizeof(addr_t))
#define INSTR_MEM_WRITE_MAX_SIZE (sizeof(addr_t) + 256)
#define INSTR_MEM_WRITE_HANDLER  instruction_mem_write

#endif /* SCOUT_INSTRUCTIONS */

#endif // __SCOUT__API__H__
