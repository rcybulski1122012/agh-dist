module SmartHome {
    // Common
    exception DeviceTurnedOffError {};
    exception InvalidColorError {};
    exception InvalidDate {};

    struct Color {
        int red;
        int green;
        int blue;
    };

    struct Date {
        int year;
        int month;
        int day;
        int hour;
        int minute;
    };

    interface Device {
        idempotent string getDeviceName();
        idempotent bool turnOn();
        idempotent bool turnOff();
        idempotent bool isTurnedOn();
    };

    // Light bulbs
    exception InvalidBrightnessError {};

    interface SimpleBulb extends Device {};
    interface DimmableBulb extends SimpleBulb {
        idempotent void setBrightness(int brightness) throws InvalidBrightnessError;
        idempotent int getBrightness();
    };
    interface ColorBulb extends DimmableBulb {
        idempotent void setColor(Color color) throws InvalidColorError;
        idempotent Color getColor();
    };

    // CleaningRobots
    exception RoomNotFoundError {};
    exception ScheduleNotFoundError {};
    exception OngoingCleanngError {};
    exception CleaningScheduleConflictError {};

    struct Room {
        int id;
        string name;
        double area;
    };

    struct CleaningSchedule {
        int id;
        Room room;
        Date date;
    };
    sequence<Room> RoomList;
    sequence<CleaningSchedule> CleaningScheduleList;

    interface SimpleCleaningRobot extends Device {
        void startCleaningAllRooms() throws DeviceTurnedOffError, OngoingCleanngError, CleaningScheduleConflictError;
        idempotent void stopCleaning();
        idempotent bool isCleaning();
    };

    interface SmartCleaningRobot extends SimpleCleaningRobot {
        void startCleaningRoom(int roomId) throws DeviceTurnedOffError, OngoingCleanngError, RoomNotFoundError, CleaningScheduleConflictError;
        CleaningSchedule addCleaningSchedule(int roomId, Date date) throws RoomNotFoundError, InvalidDate, CleaningScheduleConflictError;
        CleaningSchedule removeCleaningSchedule(int scheduleId) throws ScheduleNotFoundError;
        idempotent CleaningScheduleList getCleaningSchedules();
        idempotent RoomList getRooms();
        idempotent void setRoomName(int roomId, string name) throws RoomNotFoundError;
    };
};
