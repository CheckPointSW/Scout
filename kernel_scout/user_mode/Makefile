MAKE=make
RM=rm
OUTFILE=scout_user
SCOUT_SRC=../../scout

# Build rules
all: $(OUTFILE)

$(OUTFILE):
	python compile_scout.py

# Rebuild this project
rebuild: cleanall all

# Clean this project
clean:
	$(RM) -f $(OUTFILE)
	$(RM) -f *.o
	$(RM) -f $(SCOUT_SRC)/*.o
	$(RM) -f $(SCOUT_SRC)/pic/*.o
	$(RM) -f $(SCOUT_SRC)/arc/*.o

# Clean this project and all dependencies
cleanall: clean
