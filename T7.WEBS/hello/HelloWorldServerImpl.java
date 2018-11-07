package hello;
 
import javax.jws.WebService;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;

@WebService(endpointInterface = "hello.HelloWorldServer")
public class HelloWorldServerImpl implements HelloWorldServer {
	private int clientIdx;
    private ArrayList<Msg>[] listaMsg;
    private String[] nomes;

	public String sayHello(String name) {
		return "Hello " + name + " !, Hope you are doing well !!";
	}

    public int iniciarConexao(String nome) {
        if(listaMsg == null) {
            listaMsg = new ArrayList[10];
            clientIdx = 0;
            nomes = new String[10];
            nomes[0] = "SVR";
            for(int i = 0; i < 10; i++) {
                listaMsg[i] = new ArrayList();
            }
        }

        clientIdx++;

        nomes[clientIdx] = nome;
        System.out.println(nomes[clientIdx]);
        System.out.printf("[SVR] Nova conexão com %s#%d\n", nome,clientIdx);
        enviarMensagem(0, String.format("%s Entrou no chat", nome));
        return clientIdx;
    }

    public void enviarMensagem(int id, String msg) {
        for(int i = 0; i < 10; i++) {
            listaMsg[i].add(new Msg(id, msg));
        }
        System.out.printf("[CLI#%d] %s\n", id, msg);
    }

    public String getMensagem(int id) {
        String ret = "";
        while(!listaMsg[id].isEmpty()) {
            Msg aux = listaMsg[id].get(0);
            if(aux.cli != id) {
                ret += nomes[aux.cli] + "> " + aux.str + "\n";
            }
            listaMsg[id].remove(0);
        }

        return ret;
    }
 
}
