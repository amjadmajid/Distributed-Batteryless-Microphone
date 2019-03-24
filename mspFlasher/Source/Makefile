CC=g++
CFLAGS=-std=c++0x -I./Inc
LDFLAGS=-L../ -lmsp430
SOURCES=MSP430_Flasher.cpp Support.cpp StdUseCase.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=../MSP430Flasher

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS) 
	$(CC) -o $@ $(CFLAGS) $(OBJECTS) $(LDFLAGS) 

.cpp.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf *.o
	rm -rf ../MSP430Flasher
