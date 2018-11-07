package hello;

import javax.xml.ws.Endpoint;

public class HelloWorldServerPublisher {
	public static void main(String[] args) {
		System.out.println("Beginning to publish HelloWorldService now");
		Endpoint.publish("http://192.168.100.7:9876/WSHello", new HelloWorldServerImpl());
		System.out.println("Done publishing");
	}

}
