all: client server

hw.h: hw.x
	rpcgen hw.x

hw_svc.c hw_clnt.c main.c: hw.h

client: main.o hw_clnt.o
	cc -Isource source/lista.c -o client main.o hw_clnt.o  -lnsl -pthread

server: hw_server.o hw_svc.o
	cc -Isource source/lista.c -o server hw_server.o hw_svc.o -lnsl -pthread


.PHONY: clean

clean:
	-rm *.o
	-rm client*
	-rm server*
	-rm hw.h
	-rm hw_clnt.c
	-rm hw_svc.c
