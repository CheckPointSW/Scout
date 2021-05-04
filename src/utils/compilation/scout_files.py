############################
##  Files Configurations  ##
############################

# scout file list
scout_arc_files       = ['arc/arm.c', 'arc/mips.c', 'arc/intel.c']
scout_pic_files       = ['pic/arm_pic_wrapper.c', 'pic/mips_pic_wrapper.c', 'pic/intel_pic_wrapper.c', 'pic/scout_plt.c', 'pic/scout_globals.c']
# PIC files vanish upon compilation without the SCOUT_PIC_CODE flag
scout_loader_deps     = scout_pic_files + scout_arc_files + ['pack.c']
scout_net_loader_deps = scout_loader_deps + ['tcp_server.c']
scout_all_files       = scout_pic_files + scout_arc_files + ['pack.c', 'scout_api.c', 'tcp_server.c']

scout_server_loader   = 'loaders/tcp_server_loader.c'
scout_client_loader   = 'loaders/tcp_client_loader.c'

scout_server_loader_deps = scout_net_loader_deps + [scout_server_loader]
scout_client_loader_deps = scout_net_loader_deps + [scout_client_loader]
