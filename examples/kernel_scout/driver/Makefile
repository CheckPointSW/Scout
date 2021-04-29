RM=rm
SCOUT_SRC=../../../src/scout

obj-m+=scout.o
EXTRA_CFLAGS := -I$(src) -I$(src)/../.. -Wno-incompatible-pointer-types
scout-objs := $(SCOUT_SRC)/pack.o $(SCOUT_SRC)/scout_api.o scout_driver.o scout_kernel_instructions.o

# Build rules
all:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) modules

# Rebuild this project
rebuild: cleanall all

# Clean this project
clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) clean
	$(RM) -f $(SCOUT_SRC)/*.o

# Clean this project and all dependencies
cleanall: clean