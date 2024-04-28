package server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;
import server.servants.bulbs.ColorBulbI;
import server.servants.bulbs.DimmableBulbI;
import server.servants.bulbs.SimpleBulbI;
import server.servants.cleaning_robots.SimpleCleaningRobotI;
import server.servants.cleaning_robots.SmartCleaningRobotI;

import java.util.ArrayList;
import java.util.List;

public class SmartHomeServantLocator implements ServantLocator {
    private final List<String> deviceNames = new ArrayList<>();

    @Override
    public LocateResult locate(Current current) throws UserException {
        System.out.println("locate " + current.id.name);
        String servantName = current.id.name;
        ObjectAdapter adapter = current.adapter;
        deviceNames.add(servantName);
        switch (servantName) {
            case "KitchenLampBulb", "BathroomLampBulb":
                SimpleBulbI kitchenLampBulb = new SimpleBulbI(servantName);
                adapter.add(kitchenLampBulb, kitchenLampBulb.getIdentity());
                return new LocateResult(kitchenLampBulb, null);
            case "BedRoomLampBulb":
                DimmableBulbI bedRoomLampBulb = new DimmableBulbI(servantName);
                adapter.add(bedRoomLampBulb, bedRoomLampBulb.getIdentity());
                return new LocateResult(bedRoomLampBulb, null);
            case "LivingRoomLampBulb":
                ColorBulbI livingRoomLampBulb = new ColorBulbI(servantName);
                adapter.add(livingRoomLampBulb, livingRoomLampBulb.getIdentity());
                return new LocateResult(livingRoomLampBulb, null);
            case "GarageCleaningRobot":
                 SimpleCleaningRobotI garageCleaningRobot = new SimpleCleaningRobotI(servantName);
                 adapter.add(garageCleaningRobot, garageCleaningRobot.getIdentity());
                 return new LocateResult(garageCleaningRobot, null);
             case "MainCleaningRobot":
                 SmartCleaningRobotI mainCleaningRobot = new SmartCleaningRobotI(servantName);
                 adapter.add(mainCleaningRobot, mainCleaningRobot.getIdentity());
                 return new LocateResult(mainCleaningRobot, null);
             default:
                 throw new RuntimeException("Unknown servant name: " + servantName);
        }
    }

    @Override
    public void finished(Current current, Object object, java.lang.Object o) throws UserException {}

    @Override
    public void deactivate(String s) {}

    public void printDevices() {
        System.out.println("Devices:");
        for (String deviceName : deviceNames) {
            System.out.println(" - " + deviceName);
        }
    }

}
