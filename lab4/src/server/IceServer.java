package server;

import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.ObjectAdapter;
import com.zeroc.Ice.Util;

import java.util.Scanner;

public class IceServer implements Runnable {
    private static final String SERVER_ADDRESS = "127.0.0.1";
    private final static SmartHomeServantLocator servantLocator = new SmartHomeServantLocator();
    private final String[] args;

    public IceServer(String[] args) {
        this.args = args;
    }

    @Override
    public void run() {
        int status = 0;
        Communicator communicator = null;
        try {
            communicator = Util.initialize(this.args);
            String adapterEndpoint = getAdapterEndpoint(this.args);
            System.out.println(adapterEndpoint);
            ObjectAdapter smartHomeAdapter = communicator.createObjectAdapterWithEndpoints(
                "SmartHomeAdapter", adapterEndpoint
            );
            smartHomeAdapter.addServantLocator(servantLocator, "");
            smartHomeAdapter.activate();
            System.out.println("Entering event processing loop...");
            communicator.waitForShutdown();
        } catch (Exception e) {
            e.printStackTrace(System.err);
            status = 1;
        }
        if (communicator != null) {
            try {
                communicator.destroy();
            } catch (Exception e) {
                e.printStackTrace(System.err);
                status = 1;
            }
        }
        System.exit(status);
    }

    private static void handleUserInput() {
        while(true) {
            Scanner scanner = new Scanner(System.in);
            String input = scanner.nextLine();
            if (input.equals("devices")) {
                servantLocator.printDevices();
            }
            else if (input.equals("exit")) {
                System.exit(0);
            }
            else {
                System.out.println("Unknown command");
            }
        }
    }

    private String getAdapterEndpoint(String[] args) {
        int port = getServerPort(args);
        return String.format(
            "tcp -h %s -p %d -z : udp -h %s -p %d -z",
            SERVER_ADDRESS, port, SERVER_ADDRESS, port
        );
    }

    private int getServerPort(String[] args) {
        for (String arg : args) {
            if (arg.startsWith("--port=")) {
                return Integer.parseInt(arg.substring(7));
            }
        }
        return 10000;
    }

    public static void main(String[] args) {
        Runnable serverRunnable = new IceServer(args);
        Thread server = new Thread(serverRunnable);
        server.start();
        handleUserInput();
    }
}
