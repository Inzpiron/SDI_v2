
/** HelloServer.java **/

import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;

public class HelloServer implements HelloWorld {
    private int clientIdx;
    private ArrayList<Msg>[] listaMsg;
    private String[] nomes;
    public HelloServer() {}

    public static void main(String[] args) {
        try {
            // Instancia o objeto servidor e a sua stub
            HelloServer server = new HelloServer();
            HelloWorld stub = (HelloWorld) UnicastRemoteObject.exportObject(server, 0);
            // Registra a stub no RMI Registry para que ela seja obtAida pelos clientes
            Registry registry = LocateRegistry.createRegistry(6600);
            //Registry registry = LocateRegistry.getRegistry(9999);
            registry.bind("Hello", stub);
            System.out.println("Servidor pronto");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public int iniciarConexao(String nome) throws RemoteException {
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

    public void enviarMensagem(int id, String msg) throws RemoteException {
        for(int i = 0; i < 10; i++) {
            listaMsg[i].add(new Msg(id, msg));
        }
        System.out.printf("[CLI#%d] %s\n", id, msg);
    }

    public String getMensagem(int id) throws RemoteException {
        String ret = "";
        while(!listaMsg[id].isEmpty()) {
            Msg aux = listaMsg[id].get(0);
            if(aux.cli != id) {
                ret += "[" + nomes[aux.cli] + "] " + aux.str + "\n";
            }
            listaMsg[id].remove(0);
        }

        return ret;
    }
}
