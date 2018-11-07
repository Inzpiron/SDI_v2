/** HelloWorld.java **/
import java.rmi.*;

public interface HelloWorld extends Remote {
    public int iniciarConexao(String nome) throws RemoteException;
    public void enviarMensagem(int id, String msg) throws RemoteException;
    public String getMensagem(int id) throws RemoteException;
}
