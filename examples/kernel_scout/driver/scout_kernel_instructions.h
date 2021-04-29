#ifndef __KERNEL__SCOUT__INSTRUCTIONS__H__
#define __KERNEL__SCOUT__INSTRUCTIONS__H__

#include "scout/scout_api.h"

/*************/
/*  Structs  */
/*************/

typedef struct __kernel_ctx
{
	int      status;
	uint32_t written;
	uint8_t  * __user output;
	uint32_t * __user stats;
} scout_kernel_ctx_t;

/*******************************/
/*  Instructions Registration  */
/*******************************/

/**
 * This is the function that will be used by scout_api.c
 * 
 * @author eyalit (06/05/2018)
 */
void register_specific_instructions(void);

/*************************/
/*  Kernel Instructions  */
/*************************/

#define KERNEL_INST_COUNT_BASE     (SCOUT_MAX_BASIC_INSTR + 1)
#define KERNEL_INST_PHY_READ       (KERNEL_INST_COUNT_BASE + 0)
#define KERNEL_INST_PHY_WRITE      (KERNEL_INST_COUNT_BASE + 1)
#define KERNEL_INST_LEAK_ADDR      (KERNEL_INST_COUNT_BASE + 2)

/**
 * Read physical memory
 * 
 * @author eyalit (06/05/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int instruction_phy_read( void * ctx, uint8_t * instruction, uint32_t length);

/**
 * Write physical memory
 * 
 * @author eyalit (06/05/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int instruction_phy_write(void * ctx, uint8_t * instruction, uint32_t length);

/**
 * Leak the address of a pre-defined kernel function: add_input_randomness
 * 
 * @author eyalit (06/05/2018)
 * 
 * @param ctx - general context
 * @param instruction - raw instruction buffer
 * @param length - number of bytes in the instruction buffer
 * 
 * @return int32_t - success status
 */
int instruction_leak_addr(void * ctx, uint8_t * instruction, uint32_t length);

/* The instruction records */
#define INSTR_PHY_READ_MIN_SIZE (sizeof(addr_t) + sizeof(uint32_t))
#define INSTR_PHY_READ_MAX_SIZE (sizeof(addr_t) + sizeof(uint32_t))
#define INSTR_PHY_READ_HANDLER  instruction_phy_read

#define INSTR_PHY_WRITE_MIN_SIZE (sizeof(addr_t))
#define INSTR_PHY_WRITE_MAX_SIZE (sizeof(addr_t) + 256)
#define INSTR_PHY_WRITE_HANDLER  instruction_phy_write

#define INSTR_LEAK_ADDR_MIN_SIZE 0
#define INSTR_LEAK_ADDR_MAX_SIZE 0
#define INSTR_LEAK_ADDR_HANDLER  instruction_leak_addr

#endif // __KERNEL__SCOUT__INSTRUCTIONS__H__