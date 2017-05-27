all: db auth sla

db:
	make -C $@

auth:
	make -C $@

sla:
	make -C $@

clean:
	
.PHONY: all db auth sla clean

