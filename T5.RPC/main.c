#include <stdio.h>
#include <rpc/rpc.h>
#include <pthread.h>
#include <unistd.h>
#include "hw.h"
#include "source/lista.h"
#define clear() printf("\033[H\033[J")
#define gotoxy(x,y) printf("\033[%d;%dH", (x), (y))
/*
   Simple "hello world" program that demonstrates an rpc call.
*/

int my_id;
CLIENT *cl;
int writing = 1;

char * create_message(char * str) {
	char * m = malloc(1500);
	m[0] = '0' + my_id;
	m[1] = '-';
	strcpy(m+2, str);

	return m;
}

void * write_buffer(void * arg) {
	while(writing) {
		char * m = *(getmessages_1(&my_id, cl));
		if(strlen(m) != 0 && m != NULL)
			printf("%s", m);

		usleep(1000 * 50);
	}
}

void * read_buffer(void * arg) {
	char * m = malloc(1500);
	while(1) {
		setbuf(stdin, NULL);
		scanf("%[^\n]", m);
		m = create_message(m);
		newmessage_1(&m, cl);

		if(strcmp(m, strdup("quit")) == 0) {
			writing = 0;
			break;
		}
	}
}


int main (int argc, char *argv[]) {
	/***************************************************************************
	******************************DEFAULT***************************************
	****************************************************************************/
	if (argc != 3) {
		printf("Usage: client hostname\n");
		exit(1);
	}

	cl = clnt_create(argv[1], HELLO_WORLD_PROG, HELLO_WOLRD_VERS, "tcp");
	if (cl == NULL) {
		clnt_pcreateerror(argv[1]);
		exit(1);
	}
	/****************************************************************************/

	pthread_t t_writebuffer;
	pthread_t t_readbuffer;
	my_id = *(getid_1(&argv[2], cl));
	printf("%d\n", my_id);
	pthread_create(&(t_writebuffer), NULL, write_buffer, NULL);
	pthread_create(&(t_readbuffer), NULL, read_buffer, NULL);

	pthread_join(t_writebuffer, NULL);
	pthread_join(t_readbuffer, NULL);
	return 0;
}
