MAKE=make
RM=rm
OUTFILE=embedded_scout.bin
LOADERFILE=scout_loader.bin
SCOUT_SRC=../../../src/scout

# Build rules
all: $(OUTFILE) $(LOADERFILE)

$(OUTFILE):
	python3 compile_scout.py

# Rebuild this project
rebuild: cleanall all

# Clean this project
clean:
	$(RM) -f $(OUTFILE)
	$(RM) -f $(LOADERFILE)
	$(RM) -f *.elf
	$(RM) -f *.o
	$(RM) -f *.S
	$(RM) -f $(SCOUT_SRC)/*.o
	$(RM) -f $(SCOUT_SRC)/*.S
	$(RM) -f $(SCOUT_SRC)/pic/*.o
	$(RM) -f $(SCOUT_SRC)/pic/*.S
	$(RM) -f $(SCOUT_SRC)/arc/*.o
	$(RM) -f $(SCOUT_SRC)/arc/*.S
	$(RM) -f $(SCOUT_SRC)/loaders/*.o
	$(RM) -f $(SCOUT_SRC)/loaders/*.S

# Clean this project and all dependencies
cleanall: clean
