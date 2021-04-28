#ifndef __SCOUT__PIC__WRAPPER__H__
#define __SCOUT__PIC__WRAPPER__H__

#include "scout/scout.h"

#ifdef SCOUT_PIC_CODE

#include "scout/pic/scout_plt.h"
#include "scout/pic/scout_globals.h"
/* Project Extensions */
#ifdef SCOUT_LOADER
#include "loader_plt.h"
#include "loader_globals.h"
#else /* !SCOUT_LOADER */
#include "project_plt.h"
#include "project_globals.h"
#endif /* SCOUT_LOADER */

/***************/
/**  Structs  **/
/***************/

typedef struct __pic_full_got
{
    pic_got_t       scout;
    project_got_t   project;
} pic_full_got_t;

typedef struct __pic_full_vars
{
    pic_vars_t      scout;
    project_vars_t  project;
} pic_full_vars_t;

typedef struct __pic_context
{
    pic_full_got_t  functions;
    pic_full_vars_t globals;
} pic_context_t;

/***********/
/**  API  **/
/***********/

/**
 * API function that signals the "main" function of scout projects
 *
 * @author eyalit (22/03/2018)
 */
void scout_main();

/*****************/
/**  Functions  **/
/*****************/

#ifdef SCOUT_ARCH_MIPS
void __start(void);
#else
void _start(void);
#endif

/**
 * Returns a pointer to the PIC management context
 *
 * @author eyalit (22/03/2018)
 *
 * @return pic_context_t * - pointer to the PIC context
 */
pic_context_t * get_context();

/**
 * Converts a static address to the actual live address
 *
 * @author eyalit (22/03/2018)
 *
 * @param address - static address
 *
 * @return void * - fixed dynamic address
 */
void * get_live_address(const void * address);

#endif /* SCOUT_PIC_CODE */

#endif // __SCOUT__PIC__WRAPPER__H__
