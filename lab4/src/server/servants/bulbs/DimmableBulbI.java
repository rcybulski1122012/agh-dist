package server.servants.bulbs;

import SmartHome.DimmableBulb;
import SmartHome.InvalidBrightnessError;
import com.zeroc.Ice.Current;

public class DimmableBulbI extends SimpleBulbI implements DimmableBulb {
    private final static int BRIGHTNESS_MAX = 100;
    private final static int BRIGHTNESS_MIN = 1;
    private int brightness;
    public DimmableBulbI(String deviceName) {
        super(deviceName);
        this.brightness = 50;
    }

    @Override
    public void setBrightness(int brightness, Current current) throws InvalidBrightnessError {
        if (brightness < BRIGHTNESS_MIN || brightness > BRIGHTNESS_MAX) {
            System.out.printf("Invalid brightness value for %s\n", deviceName);
            throw new InvalidBrightnessError();
        }
        System.out.printf("%s's brightness set to %d\n", deviceName, brightness);
        this.brightness = brightness;
    }

    @Override
    public int getBrightness(Current current) {
        return brightness;
    }
}
