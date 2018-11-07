package hello;

import javax.jws.WebMethod;
import javax.jws.WebService;
import javax.jws.soap.SOAPBinding;
import javax.jws.soap.SOAPBinding.Style;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;


@WebService
@SOAPBinding(style = Style.RPC)
public interface HelloWorldServer {
	@WebMethod
	String sayHello(String name);

	@WebMethod
	int iniciarConexao(String nome);

	@WebMethod
	void enviarMensagem(int id, String msg);

	@WebMethod
	String getMensagem(int id);
}
