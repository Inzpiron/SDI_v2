/** HelloClient.java **/
import java.rmi.registry.*;
import java.lang.*;
import java.util.Scanner;

public class HelloClient extends Thread{
    public static int meuId = -1;
    public static HelloWorld stub;

    private static Runnable lerMensagens = new Runnable() {
        public void run() {
            Scanner scanner = new Scanner(System.in);
            while(true) {
                try {
                    Thread.sleep(200);
                    String msg;
                    msg = stub.getMensagem(meuId);
                    //stub.enviarMensagem(meuId, "KKKKKKKKKKKKKKKKKKKKKK");
                    System.out.printf("%s", msg);
                } 
                catch(Exception ex) {
                    ex.printStackTrace();
                }
            }
        }
    };

    public static void main(String[] args) {
        String host = (args.length < 1) ? null : args[0];
        try {
            // Obtém uma referência para o registro do RMI
            Registry registry = LocateRegistry.getRegistry(host,6600);

            // Obtém a stub do servidor
            stub = (HelloWorld) registry.lookup("Hello");

            // Chama o método do servidor e imprime a mensagem
            meuId = stub.iniciarConexao(args[1]);

            new Thread(lerMensagens).start();
            Scanner scanner = new Scanner(System.in);

            while(true) {
                stub.enviarMensagem(meuId, scanner.nextLine());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        System.out.printf("Bem-vindo a sala de bate papo\n");   
    }
}
