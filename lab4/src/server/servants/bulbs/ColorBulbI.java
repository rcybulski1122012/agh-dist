package server.servants.bulbs;

import SmartHome.Color;
import SmartHome.ColorBulb;
import SmartHome.InvalidColorError;
import com.zeroc.Ice.Current;

public class ColorBulbI extends DimmableBulbI implements ColorBulb {
    private Color color;


    public ColorBulbI(String deviceName) {
        super(deviceName);
        this.color = new Color(0, 0, 0);
    }

    @Override
    public void setColor(Color color, Current current) throws InvalidColorError {
        if (
            color.red < 0 || color.red > 255 ||
            color.green < 0 || color.green > 255 ||
            color.blue < 0 || color.blue > 255
        ) {
            System.out.printf("Invalid color value for %s\n", deviceName);
            throw new InvalidColorError();
        }
        System.out.printf("%s's color set to (%d, %d, %d)\n", deviceName, color.red, color.green, color.blue);
        this.color = color;
    }


    @Override
    public Color getColor(Current current) {
        return color;
    }
}
