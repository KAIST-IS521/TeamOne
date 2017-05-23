CFLAGS = -fPIC -Wall -Wextra -O2 -g -lrt -D_FILE_OFFSET_BITS=64 `gpgme-config --libs`# C flags
LIBPATH = -L$(LIB)
LDFLAGS = -Wl,-rpath,$(LIB)
LIB = ./
LIBS = -lsla
BUILDDIR = build

all: $(BUILDDIR) $(BUILDDIR)/sla_auth

$(BUILDDIR):
	mkdir -p $@

$(BUILDDIR)/sla_auth: sla_auth.c $(BUILDDIR)
	$(CC) $(LIBPATH) $(CFLAGS) $(LDFLAGS) -o$@ $< $(LIBS)

clean:
	rm -rf $(BUILDDIR)

.PHONY: all clean
