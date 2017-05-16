all: db auth

db:
	make -C $@

auth:
	make -C $@

clean:
	
.PHONY: all db auth clean

