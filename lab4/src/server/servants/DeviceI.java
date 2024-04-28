package server.servants;

import com.zeroc.Ice.Current;
import com.zeroc.Ice.Identity;

abstract public class DeviceI implements SmartHome.Device {
    protected boolean _isTurnedOn;
    protected final String deviceName;
    private final Identity identity;
    protected abstract DeviceCategory getDeviceCategory();
    public DeviceI(String deviceName) {
        _isTurnedOn = false;
        this.deviceName = deviceName;
        this.identity = new Identity(deviceName, getDeviceCategory().toString());
    }
    @Override
    public boolean turnOn(Current current) {
        _isTurnedOn = true;
        System.out.printf("%s has been turned on\n", deviceName);
        return isTurnedOn(current);
    }

    @Override
    public boolean turnOff(Current current) {
        _isTurnedOn = false;
        System.out.printf("%s has been turned off\n", deviceName);
        return isTurnedOn(current);
    }

    @Override
    public boolean isTurnedOn(Current current) {
        return _isTurnedOn;
    }

    @Override
    public String getDeviceName(Current current) {
        return deviceName;
    }

    public Identity getIdentity() {
        return identity;
    }
}
