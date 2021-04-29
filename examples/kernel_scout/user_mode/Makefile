MAKE=make
RM=rm
OUTFILE=scout_user
SCOUT_SRC=../../../src/scout

# Build rules
all: $(OUTFILE)

$(OUTFILE):
	python3 compile_scout.py

# Rebuild this project
rebuild: cleanall all

# Clean this project
clean:
	$(RM) -f $(OUTFILE)
	$(RM) -f *.o
	$(RM) -f $(SCOUT_SRC)/*.o

# Clean this project and all dependencies
cleanall: clean
