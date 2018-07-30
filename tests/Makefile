MAKE=make
RM=rm
FILE32=exploit_me_32
FILE64=exploit_me_64

# Build rules
all: $(FILE32) $(FILE64)

$(FILE32):
	gcc -m32 exploit_me.c -o $(FILE32)

$(FILE64):
	gcc exploit_me.c -o $(FILE64)

# Rebuild this project
rebuild: cleanall all

# Clean this project
clean:
	$(RM) -f $(FILE32)
	$(RM) -f $(FILE64)

# Clean this project and all dependencies
cleanall: clean
