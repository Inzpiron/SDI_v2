#include <rpc/rpc.h>
#include <unistd.h>
#include "hw.h"
#include "source/lista.h"
/*
   Hello world RPC server -- it just returns the string.
*/


struct msg {
	int msg_id;
	int cli_id;
	char * str;
};
typedef struct msg Msg;

Msg * novaMsg(int msg_id, int cli_id, char * str) {
	Msg * m = malloc(sizeof(Msg));
	m->msg_id = msg_id;
	m->cli_id = cli_id;
	m->str = malloc(1500);
	strcpy(m->str, str);

	return m;
}

void * get_cli_str(char * str, int * cli_id, char * msg) {
	str[1] = '\0';
	*cli_id = atol(str);
	strcpy(msg, str+2);
}

char * client_names[10];
int n_clientes = -1;
LDDE * lista_msg;
int pos_msg = 0;
NoLDDE * pos_cli[10];
int cli_msgs[10] = {-1};
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

int * getid_1_svc(char ** arg, struct svc_req *req) {
	pthread_mutex_lock(&lock);	
	if(lista_msg == NULL) {
		printf("[SVR] Criando Lista de mensagens\n");
		lista_msg = listaCriar(sizeof(Msg));
		
		printf("0\n");
		int i;
		for(i = 0; i < 10; i++) {
			pos_cli[i] = NULL;
		}
	}
	++n_clientes;
	client_names[n_clientes] = malloc(strlen(*arg)+1);
	strcpy(client_names[n_clientes], *arg);
	printf("[SVR] Nova conexão %s#%d\n", client_names[n_clientes], n_clientes);
	pthread_mutex_unlock(&lock);
	return &n_clientes;
}

char ** gettop_1_svc(int * arg, struct svc_req *req) {
	static char * ret;
	char * buff;
	buff = malloc(1000);
	int cli = *arg;
	buff[0] = '\0';
	ret = buff;

	if(lista_msg->fimLista == NULL)
		return &ret;
	else if(((Msg *)lista_msg->fimLista->dados)->cli_id == *arg)
		return &ret;
	else {
		Msg * m = (Msg *) lista_msg->fimLista->dados;
		if(m == NULL || m->msg_id == cli_msgs[cli])
			return &ret;
		else {
			strcat(buff, client_names[m->cli_id]);
			strcat(buff, "> ");
			strcat(buff, m->str);
			cli_msgs[cli] = m->msg_id;
			return &ret;
		}
	}
}

char ** getmessages_1_svc(int * arg, struct svc_req * req) {
	int cli = *arg;
	static char * ret;
	char * buff = malloc(2500);
	buff[0] = '\0';
	ret = buff;

	pthread_mutex_lock(&lock);
	if(lista_msg->fimLista == NULL || pos_cli[cli] == lista_msg->fimLista) {
		pthread_mutex_unlock(&lock);
		return &ret;
	} else if(lista_msg->inicioLista != NULL && pos_cli[cli] == NULL) {
		pos_cli[cli] = lista_msg->inicioLista;
	} else if(pos_cli[cli] != NULL){
		if((pos_cli[cli])->prox != NULL)
			(pos_cli[cli]) = (pos_cli[cli])->prox;
	}

	while(pos_cli[cli] != NULL){
		Msg * m = malloc(sizeof(Msg));
		memcpy(m, (pos_cli[cli])->dados, sizeof(Msg));

		if(cli != m->cli_id) {
			char * straux = malloc(2500);
			sprintf(straux, "%s#%d> %s\n", client_names[m->cli_id], m->cli_id,  m->str);
			strcat(buff, straux);
		}

		if((pos_cli[cli])->prox != NULL)
			pos_cli[cli] = pos_cli[cli]->prox;
		else
			break;
	}
	pthread_mutex_unlock(&lock);
	return &ret;
}




void * newmessage_1_svc(char ** arg, struct svc_req *req) {
	int cli_id;
	char * msg = malloc(1500);
	get_cli_str(*arg, &cli_id, msg);
	pthread_mutex_lock(&lock);
	listaInserir(lista_msg, novaMsg(pos_msg, cli_id, msg));
	pthread_mutex_unlock(&lock);
	printf("[MSG-%d] %s#%d \"%s\"\n", pos_msg, client_names[cli_id],cli_id,  msg);
	pos_msg++;
}

char **hw_1_svc(void *a, struct svc_req *req) {
	printf("NEW CONNECTION: %d\n", n_clientes);
	printf("FODEO\n");
	n_clientes++;
	char * str = malloc(sizeof(char) * 256);
	scanf("%s", str);

	static char msg[256];
	static char *p;

	printf("getting ready to return value\n");
	strcpy(msg, "Hello world3");
	p = str;
	printf("Returning...\n");

	return(&p);
}
