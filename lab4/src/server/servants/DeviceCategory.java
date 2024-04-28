package server.servants;

public enum DeviceCategory {
    BULB,
    CLEANING_ROBOT;

    public String toString() {
        switch(this) {
            case BULB:
                return "Bulb";
            case CLEANING_ROBOT:
                return "CleaningRobot";
            default:
                return "Unknown";
        }
    }
}
