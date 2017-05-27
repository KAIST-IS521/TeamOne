CFLAGS = -fPIC -Wall -Wextra -Wno-unused-parameter -O2 -g -lrt -D_FILE_OFFSET_BITS=64 `gpgme-config --libs`# C flags
LIBPATH = -L$(LIB)
LDFLAGS = -Wl,-rpath,$(LIB)
LIB = ./
LIBS = -lsla
BUILDDIR = build

all: packages $(BUILDDIR) $(BUILDDIR)/sla_checker

packages:
	sudo apt-get install libgpgme11-dev
	sudo apt-get install libssl-dev

$(BUILDDIR):
	mkdir -p $@

$(BUILDDIR)/sla_checker: sla_checker.c $(BUILDDIR)
	$(CC) $(LIBPATH) $(CFLAGS) $(LDFLAGS) -o$@ $< $(LIBS)

clean:
	rm -rf $(BUILDDIR)

.PHONY: all clean
