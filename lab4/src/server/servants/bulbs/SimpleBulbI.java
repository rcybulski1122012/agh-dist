package server.servants.bulbs;

import SmartHome.SimpleBulb;
import server.servants.DeviceCategory;
import server.servants.DeviceI;

public class SimpleBulbI extends DeviceI implements SimpleBulb {
    public SimpleBulbI(String deviceName) {
        super(deviceName);
    }

    public DeviceCategory getDeviceCategory() {
        return DeviceCategory.BULB;
    }
}
