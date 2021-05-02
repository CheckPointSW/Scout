#ifndef __SCOUT__PACK__H__
#define __SCOUT__PACK__H__

#include "scout/scout.h"

#define GET_BYTE(_V_,  _N_)     ((uint8_t)((_V_) >> ((_N_) * 8) & 0xFF))
#define SET_BYTE(_V_,  _N_)     (((_V_) & 0xFF) << ((_N_) * 8))

/**
 * Packs a single byte value into the packed buffer. This operation
 * advances the buffer's write pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 * @param value - single byte value to be stored
 */
void pack_uint8( uint8_t ** buffer, uint8_t value);

/**
 * Packs a 2 bytes value into the packed buffer. This operation
 * advances the buffer's write pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 * @param value - 2 bytes value to be stored
 */
void pack_uint16(uint8_t ** buffer, uint16_t value);

/**
 * Packs a 4 bytes value into the packed buffer. This operation
 * advances the buffer's write pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 * @param value - 4 bytes value to be stored
 */
void pack_uint32(uint8_t ** buffer, uint32_t value);

/**
 * Packs an 8 byte value into the packed buffer. This operation
 * advances the buffer's write pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 * @param value - 8 byte value to be stored
 */
void pack_uint64(uint8_t ** buffer, uint64_t value);

/**
 * Packs an address value into the packed buffer. This operation
 * advances the buffer's write pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 * @param value - address value to be stored
 */
void pack_addr(uint8_t ** buffer, addr_t value);

/**
 * Unpacks (extracts) a single byte value from the packed
 * buffer. This operation advances the buffer's read pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 *
 * @return uint8_t - extracted single byte value
 */
uint8_t  unpack_uint8( uint8_t ** buffer);

/**
 * Unpacks (extracts) a 2 bytes value from the packed
 * buffer. This operation advances the buffer's read pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 *
 * @return uint16_t - extracted 2 bytes value
 */
uint16_t unpack_uint16(uint8_t ** buffer);

/**
 * Unpacks (extracts) a 4 bytes value from the packed
 * buffer. This operation advances the buffer's read pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 *
 * @return uint32_t - extracted 4 bytes value
 */
uint32_t unpack_uint32(uint8_t ** buffer);

/**
 * Unpacks (extracts) an 8 bytes value from the packed buffe.
 * This operation advances the buffer's read pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 *
 * @return uint64_t - extracted 8 bytes value
 */
uint64_t unpack_uint64(uint8_t ** buffer);

/**
 * Unpacks (extracts) an address from the packed buffer.
 * This operation advances the buffer's read pointer.
 *
 * @author eyalit (07/03/2018)
 *
 * @param buffer - packed buffer
 *
 * @return addr_t - extracted address value
 */
addr_t unpack_addr(uint8_t ** buffer);

#ifdef SCOUT_ISOLATED_ENV

/**
 * Converts the given value from host order to network order
 *
 * @author eyalit (07/03/2018)
 *
 * @param value - value to be converted
 *
 * @return uint16_t - converted value
 */
uint16_t htons(uint16_t value);

/**
 * Converts the given value from host order to network order
 *
 * @author eyalit (07/03/2018)
 *
 * @param value - value to be converted
 *
 * @return uint32_t - converted value
 */
uint32_t htonl(uint32_t value);

/**
 * Converts the given value from host order to network order
 *
 * @author eyalit (07/03/2018)
 *
 * @param value - value to be converted
 *
 * @return uint64_t - converted value
 */
uint64_t htonq(uint64_t value);

/**
 * Converts the given value from network order to host order
 *
 * @author eyalit (07/03/2018)
 *
 * @param value - value to be converted
 *
 * @return uint16_t - converted value
 */
uint16_t ntohs(uint16_t value);

/**
 * Converts the given value from network order to host order
 *
 * @author eyalit (07/03/2018)
 *
 * @param value - value to be converted
 *
 * @return uint32_t - converted value
 */
uint32_t ntohl(uint32_t value);

/**
 * Converts the given value from network order to host order
 *
 * @author eyalit (07/03/2018)
 *
 * @param value - value to be converted
 *
 * @return uint64_t - converted value
 */
uint64_t ntohq(uint64_t value);

#endif /* SCOUT_ISOLATED_ENV */

#endif // __SCOUT__PACK__H__
