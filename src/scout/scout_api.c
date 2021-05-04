#include "scout/scout_api.h"
#include "scout/pack.h"
#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_INSTRUCTIONS

/* Global Variables */

#ifndef SCOUT_PIC_CODE
static uint16_t gNumInstructions = 0;
static uint16_t * gpNumInstructions = &gNumInstructions;
static scout_instruction_t gInstructions[SCOUT_MAX_INSTRS] = {0};
#endif /* !SCOUT_PIC_CODE */

int32_t parse_header(uint8_t * buffer, uint32_t length, scout_header_t * header, bool validateLen)
{
    uint8_t * readHead;

    /* Sanity Check #1 - buffer is not NULL */
    if (buffer == NULL)
    {
        return STATUS_INVALID_ARGS;
    }

    /* Sanity Check #2 - length is big enough */
    if (length < SCOUT_HEADER_SIZE)
    {
        return STATUS_SMALL_HEADER;
    }

    /* Now parse the fields from the raw header */
    readHead = buffer;
    header->instrID = unpack_uint16(&readHead);
    header->length  = unpack_uint32(&readHead);

    /* Validate the length */
    if (validateLen && header->length != length - SCOUT_HEADER_SIZE)
    {
        return STATUS_ILLEGAL_LENGTH;
    }

    /* All was OK */
    return STATUS_OK;
}

#ifndef SCOUT_PROXY
int32_t handle_instruction(void * ctx, scout_header_t * header, uint8_t * buffer)
{
    uint16_t index = 0;
    int32_t status = STATUS_ILLEGAL_INSTR_ID;

    /* Find and verify the given instruction */
    for (index = 0; index < get_instruction_count() ; index++ )
    {
        scout_instruction_t *instr = get_instruction(index);
        if (instr->instrID != header->instrID)
        {
            continue;
        }

        /* Found our instruction - now verify it */
        if (header->length < instr->minLength ||
            instr->maxLength < header->length)
        {
            status = STATUS_ILLEGAL_LENGTH;
            break;
        }

        /* Can now handle the instruction */
        status = INVOKE_HANDLER(instr, ctx, buffer, header->length);
        break;
    }

    mark_status(ctx, status);
    return status;
}
#endif /* SCOUT_PROXY */

uint16_t get_instruction_count(void)
{
    return (uint16_t)*GLOBAL(pNumInstructions);
}

scout_instruction_t * get_instruction(uint16_t index)
{
    /* Sanity check #1 - index must be legal */
    if (index >= get_instruction_count())
    {
        return NULL;
    }
    return &GLOBAL(Instructions)[index];
}

void register_instruction(uint16_t instrID, uint32_t minLength, uint32_t maxLength, instrHandler handler)
{
    /* Sanity check #1 - array must not be full */
    if (get_instruction_count() >= SCOUT_MAX_INSTRS)
    {
        return;
    }

    /* Fill up the struct */
    GLOBAL(Instructions)[get_instruction_count()].instrID   = instrID;
    GLOBAL(Instructions)[get_instruction_count()].minLength = minLength;
    GLOBAL(Instructions)[get_instruction_count()].maxLength = maxLength;
    GLOBAL(Instructions)[get_instruction_count()].handler   = handler;
    /* Advance the counter */
    *GLOBAL(pNumInstructions) += 1;
}

void register_basic_instructions(void)
{
#ifdef SCOUT_PIC_CODE
    /* Prepare the globals (won't be set without an executable's loader) */
    *GLOBAL(pNumInstructions) = 0;
    memset(GLOBAL(Instructions), 0, SCOUT_MAX_INSTRS * sizeof(scout_instruction_t));
#endif /* SCOUT_PIC_CODE */

    /* Can now quietly register the basic instructions */
    register_instruction(SCOUT_INST_NOP,       INSTR_NOP_MIN_SIZE,       INSTR_NOP_MAX_SIZE,       INSTR_NOP_HANDLER);
    register_instruction(SCOUT_INST_MEM_READ,  INSTR_MEM_READ_MIN_SIZE,  INSTR_MEM_READ_MAX_SIZE,  INSTR_MEM_READ_HANDLER);
    register_instruction(SCOUT_INST_MEM_WRITE, INSTR_MEM_WRITE_MIN_SIZE, INSTR_MEM_WRITE_MAX_SIZE, INSTR_MEM_WRITE_HANDLER);
}

void register_all_instructions(void)
{
    /* First, register the basic instructions */
    register_basic_instructions();
    /* Now, register the specific instructions */
    register_specific_instructions();
}

int32_t instruction_nop(void * ctx, uint8_t * instruction, uint32_t length)
{
    (void)ctx;
    (void)instruction;
    (void)length;
    return STATUS_OK;
}

int32_t instruction_mem_read(void * ctx, uint8_t * instruction, uint32_t length)
{
    addr_t src;
    uint8_t * readHead = instruction;

    src    = unpack_addr(   &readHead );
    length = unpack_uint32( &readHead );

    write_output(ctx, (uint8_t *)src, length);
    return STATUS_OK;
}

int32_t instruction_mem_write(void * ctx, uint8_t * instruction, uint32_t length)
{
    addr_t dst;
    uint8_t * readHead = instruction;

    (void)ctx;

    dst    = unpack_addr( &readHead );
    length = length - sizeof(dst);

    /* Preform the write */
    memcpy((void *)dst, (void *)readHead, length);

    return STATUS_OK;
}

#endif /* SCOUT_INSTRUCTIONS */
