package server.servants.cleaning_robots;

import SmartHome.DeviceTurnedOffError;
import SmartHome.OngoingCleanngError;
import SmartHome.SimpleCleaningRobot;
import com.zeroc.Ice.Current;
import server.servants.DeviceCategory;
import server.servants.DeviceI;

import java.time.LocalDateTime;


public class SimpleCleaningRobotI extends DeviceI implements SimpleCleaningRobot {
    private LocalDateTime cleaningEndTime;

    private final static int CLEANING_TIME = 2;

    public SimpleCleaningRobotI(String deviceName) {
        super(deviceName);
        cleaningEndTime = null;
    }

    @Override
    public void startCleaningAllRooms(Current current) throws DeviceTurnedOffError, OngoingCleanngError {
        if (!_isTurnedOn) {
            System.out.printf("%s is turned off\n", deviceName);
            throw new DeviceTurnedOffError();
        }
        else if(_isCleaning()) {
            System.out.printf("%s is already cleaning\n", deviceName);
            throw new OngoingCleanngError();
        }
        else {
            System.out.printf("%s has started cleaning\n", deviceName);
            cleaningEndTime = LocalDateTime.now().plusSeconds(CLEANING_TIME);
        }
    }

    @Override
    public void stopCleaning(Current current) {
        System.out.printf("%s has stopped cleaning\n", deviceName);
        cleaningEndTime = null;
    }

    @Override
    public boolean isCleaning(Current current) {
        return _isCleaning();
    }

    private boolean _isCleaning() {
        if (cleaningEndTime == null) {
            return false;
        }
        else if (cleaningEndTime.isAfter(LocalDateTime.now())) {
            return true;
        }
        else {
            cleaningEndTime = null;
            return false;
        }
    }

    @Override
    protected DeviceCategory getDeviceCategory() {
        return DeviceCategory.CLEANING_ROBOT;
    }
}
