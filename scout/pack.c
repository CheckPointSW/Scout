#include "scout/pack.h"

#ifndef SCOUT_LOADER /* We are short in space when compiling a loader */

void pack_uint8(uint8_t ** buffer, uint8_t value)
{
    uint8_t * writeHead = *buffer;
    *writeHead++ = value;
    *buffer = writeHead;
}

void pack_uint16(uint8_t ** buffer, uint16_t value)
{
    uint8_t * writeHead = *buffer;
    *writeHead++ = GET_BYTE(value,  1);
    *writeHead++ = GET_BYTE(value,  0);
    *buffer = writeHead;
}

void pack_uint32(uint8_t ** buffer, uint32_t value)
{
    uint8_t * writeHead = *buffer;
    *writeHead++ = GET_BYTE(value,  3);
    *writeHead++ = GET_BYTE(value,  2);
    *writeHead++ = GET_BYTE(value,  1);
    *writeHead++ = GET_BYTE(value,  0);
    *buffer = writeHead;
}

void pack_uint64(uint8_t ** buffer, uint64_t value)
{
    uint8_t * writeHead = *buffer;
    *writeHead++ = GET_BYTE(value,  7);
    *writeHead++ = GET_BYTE(value,  6);
    *writeHead++ = GET_BYTE(value,  5);
    *writeHead++ = GET_BYTE(value,  4);
    *writeHead++ = GET_BYTE(value,  3);
    *writeHead++ = GET_BYTE(value,  2);
    *writeHead++ = GET_BYTE(value,  1);
    *writeHead++ = GET_BYTE(value,  0);
    *buffer = writeHead;
}

void pack_addr(uint8_t ** buffer, addr_t value)
{
#ifdef SCOUT_BITS_32
    return pack_uint32( buffer, value );
#else
    return pack_uint64( buffer, value );
#endif /* SCOUT_BITS_32 */
}

uint8_t unpack_uint8(uint8_t ** buffer)
{
    uint8_t value = **buffer;
    *buffer += 1;
    return value;
}

uint16_t unpack_uint16(uint8_t ** buffer)
{
    uint16_t value = 0;
    uint8_t * readHead = *buffer;
    value |= SET_BYTE(*readHead++, 1);
    value |= SET_BYTE(*readHead++, 0);
    *buffer = readHead;
    return value;
}

uint32_t unpack_uint32(uint8_t ** buffer)
{
    uint32_t value = 0;
    uint8_t * readHead = *buffer;
    value |= SET_BYTE(*readHead++, 3);
    value |= SET_BYTE(*readHead++, 2);
    value |= SET_BYTE(*readHead++, 1);
    value |= SET_BYTE(*readHead++, 0);
    *buffer = readHead;
    return value;
}

uint64_t unpack_uint64(uint8_t ** buffer)
{
    uint64_t value = 0;
    uint8_t * readHead = *buffer;
    value |= SET_BYTE((uint64_t)*readHead++, 7);
    value |= SET_BYTE((uint64_t)*readHead++, 6);
    value |= SET_BYTE((uint64_t)*readHead++, 5);
    value |= SET_BYTE((uint64_t)*readHead++, 4);
    value |= SET_BYTE((uint64_t)*readHead++, 3);
    value |= SET_BYTE((uint64_t)*readHead++, 2);
    value |= SET_BYTE((uint64_t)*readHead++, 1);
    value |= SET_BYTE((uint64_t)*readHead++, 0);
    *buffer = readHead;
    return value;
}

addr_t unpack_addr(uint8_t ** buffer)
{
#ifdef SCOUT_BITS_32
    return unpack_uint32( buffer );
#else
    return unpack_uint64( buffer );
#endif /* SCOUT_BITS_32 */
}

#endif /* SCOUT_LOADER */

#ifdef SCOUT_EMBEDDED_ENV

uint16_t htons(uint16_t value)
{
#ifdef SCOUT_LITTLE_ENDIAN
    value = SET_BYTE(GET_BYTE(value, 0), 1) |
            SET_BYTE(GET_BYTE(value, 1), 0);
#endif /* SCOUT_LITTLE_ENDIAN */
    return value;
}

uint32_t htonl(uint32_t value)
{
#ifdef SCOUT_LITTLE_ENDIAN
    value = SET_BYTE(GET_BYTE(value, 0), 3) |
            SET_BYTE(GET_BYTE(value, 1), 2) |
            SET_BYTE(GET_BYTE(value, 2), 1) |
            SET_BYTE(GET_BYTE(value, 3), 0);
#endif /* SCOUT_LITTLE_ENDIAN */
    return value;
}

uint64_t htonq(uint64_t value)
{
#ifdef SCOUT_LITTLE_ENDIAN
    value = SET_BYTE((uint64_t)GET_BYTE(value, 0), 7) |
            SET_BYTE((uint64_t)GET_BYTE(value, 1), 6) |
            SET_BYTE((uint64_t)GET_BYTE(value, 2), 5) |
            SET_BYTE((uint64_t)GET_BYTE(value, 3), 4) |
            SET_BYTE((uint64_t)GET_BYTE(value, 4), 3) |
            SET_BYTE((uint64_t)GET_BYTE(value, 5), 2) |
            SET_BYTE((uint64_t)GET_BYTE(value, 6), 1) |
            SET_BYTE((uint64_t)GET_BYTE(value, 7), 0);
#endif /* SCOUT_LITTLE_ENDIAN */
    return value;
}

uint16_t ntohs(uint16_t value)
{
#ifdef SCOUT_LITTLE_ENDIAN
    return htons( value );
#else
    return value;
#endif /* SCOUT_LITTLE_ENDIAN */
}

uint32_t ntohl(uint32_t value)
{
#ifdef SCOUT_LITTLE_ENDIAN
    return htonl( value );
#else
    return value;
#endif /* SCOUT_LITTLE_ENDIAN */
}

uint64_t ntohq(uint64_t value)
{
#ifdef SCOUT_LITTLE_ENDIAN
    return htonq( value );
#else
    return value;
#endif /* SCOUT_LITTLE_ENDIAN */
}

#endif /* SCOUT_EMBEDDED_ENV */
