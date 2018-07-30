#include "project_instructions.h"
#include "scout/pack.h"

void register_specific_instructions()
{
    register_instruction(EMBEDDED_INST_ALLOC, INSTR_ALLOC_MIN_SIZE, INSTR_ALLOC_MAX_SIZE, INSTR_ALLOC_HANDLER);
    register_instruction(EMBEDDED_INST_FREE,  INSTR_FREE_MIN_SIZE,  INSTR_FREE_MAX_SIZE,  INSTR_FREE_HANDLER);
}

int32_t instruction_alloc(void * ctx, uint8_t * instruction, uint32_t length)
{
    uint8_t * readHead = instruction;
    uint32_t size;

    size = unpack_uint32( &readHead );

    /* Allocate the recv buffer */
    uint8_t * buffer = (uint8_t *)malloc(size);
    if(buffer == NULL)
    {
        return STATUS_ALLOC_FAILED;
    }
    
    /* Pass on the output */    
    write_output(ctx, (uint8_t *)&buffer, sizeof(buffer));

    return STATUS_OK;
}

int32_t instruction_free(void * ctx, uint8_t * instruction, uint32_t length)
{
    uint8_t * readHead = instruction;
    uint32_t addr;

    addr = unpack_uint32( &readHead );
    free((uint8_t *)addr);

    return STATUS_OK;
}
