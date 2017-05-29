CFLAGS = -fPIC -Wall -Wextra -Wno-unused-parameter
BUILDDIR = build

all: $(BUILDDIR) $(BUILDDIR)/sla_checker

$(BUILDDIR):
	mkdir -p $@

$(BUILDDIR)/sla_checker: sla_checker.c $(BUILDDIR)
	$(CC) $(LIBPATH) $(CFLAGS) $(LDFLAGS) -o$@ $< $(LIBS)

clean:
	rm -rf $(BUILDDIR)

.PHONY: all clean
