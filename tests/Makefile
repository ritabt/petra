BIN := libtest_struct.so
FILENAME := test_structs.c.o
LDFLAGS += -shared

.SUFFIXES: # disable builtin rules (results in cyclic dependency on .py)

.PHONY: all
all: $(BIN)

%.c.o: %.c
	$(CC) $(CFLAGS) $^ -c -o $@

$(BIN): 
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

.PHONY: clean
clean:
	rm -f $(BIN) *.o
