package server.servants.cleaning_robots;

import SmartHome.*;
import com.zeroc.Ice.Current;
import server.servants.DeviceCategory;
import server.servants.DeviceI;

import java.time.DateTimeException;
import java.util.ArrayList;
import java.util.List;
import java.time.LocalDateTime;

public class SmartCleaningRobotI extends DeviceI implements SmartCleaningRobot {
    private final static double SQUARE_METER_CLEANING_TIME = 0.2;
    private final static Room[] rooms = {
            new Room(0, "Living Room", 20),
            new Room(1, "Bath Room", 8),
            new Room(2, "Kitchen", 14),
            new Room(3, "Bed Room", 10),
    };

    private final List<CleaningSchedule> cleaningSchedules;

    private LocalDateTime cleaningEndTime = null;

    public SmartCleaningRobotI(String deviceName) {
        super(deviceName);
        cleaningSchedules = new ArrayList<>();
    }

    @Override
    public void startCleaningAllRooms(Current current) throws DeviceTurnedOffError, OngoingCleanngError, CleaningScheduleConflictError {
        if (!_isTurnedOn) {
            System.out.printf("%s is turned off\n", deviceName);
            throw new DeviceTurnedOffError();
        }
        else if (_isCleaning()) {
            System.out.printf("%s is already cleaning\n", deviceName);
            throw new OngoingCleanngError();
        }

        double totalArea = getTotalHouseArea();
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime possibleCleaningEndTime = getCleaningEndTime(totalArea);
        if (isCleaningScheduled(now, possibleCleaningEndTime)) {
            System.out.printf("Cleaning schedule conflict for %s\n", deviceName);
            throw new CleaningScheduleConflictError();
        }

        System.out.printf("%s has started cleaning\n", deviceName);
        cleaningEndTime = possibleCleaningEndTime;
    }

    private boolean _isCleaning() {
        if (cleaningEndTime == null) {
            return false;
        }
        else if (LocalDateTime.now().isBefore(cleaningEndTime)) {
            return true;
        }
        else if (getOngoingSchedule() != null) {
            return true;
        }
        else {
            cleaningEndTime = null;
            return false;
        }
    }

    private double getTotalHouseArea() {
        double totalArea = 0;
        for (Room room : rooms) {
            totalArea += room.area;
        }
        return totalArea;
    }

    private LocalDateTime getCleaningEndTime(double area) {
        LocalDateTime now = LocalDateTime.now();
        return now.plusSeconds((long) (area * SQUARE_METER_CLEANING_TIME));
    }

    private boolean isCleaningScheduled(LocalDateTime start, LocalDateTime stop) {
        for (CleaningSchedule schedule : cleaningSchedules) {
            if(isScheduleColliding(schedule, start, stop)) {
                return true;
            }
        }
        return false;
    }

    private boolean isScheduleColliding(CleaningSchedule schedule, LocalDateTime start, LocalDateTime end) {
        LocalDateTime scheduleStart = LocalDateTime.of(
                schedule.date.year,
                schedule.date.month,
                schedule.date.day,
                schedule.date.hour,
                schedule.date.minute
        );
        LocalDateTime scheduleEnd = scheduleStart.plusSeconds((long) (schedule.room.area * SQUARE_METER_CLEANING_TIME));
        return (start.isAfter(scheduleStart) && start.isBefore(scheduleEnd)) || // this event starts during another one
                (end.isAfter(scheduleStart) && end.isBefore(scheduleEnd)) || // this event ends during another one
                (start.isBefore(scheduleStart) && end.isAfter(scheduleEnd)) || // this event starts before another one and ends after it
                (start.equals(scheduleStart) || end.equals(scheduleEnd)); // this event starts or ends exactly when another one does

    }

    @Override
    public void stopCleaning(Current current) {
        CleaningSchedule schedule = getOngoingSchedule();
        if (schedule != null) {
            cleaningSchedules.remove(schedule);
        }
        System.out.printf("%s has stopped cleaning\n", deviceName);
        cleaningEndTime = null;
    }
    private CleaningSchedule getOngoingSchedule() {
        for (CleaningSchedule schedule : cleaningSchedules) {
            LocalDateTime scheduleStart = LocalDateTime.of(
                schedule.date.year,
                schedule.date.month,
                schedule.date.day,
                schedule.date.hour,
                schedule.date.minute
            );
            LocalDateTime scheduleEnd = scheduleStart.plusSeconds((long) (schedule.room.area * SQUARE_METER_CLEANING_TIME));
            LocalDateTime now = LocalDateTime.now();
            if (now.isAfter(scheduleStart) && now.isBefore(scheduleEnd)) {
                return schedule;
            }
        }

        return null;
    }
    @Override
    public boolean isCleaning(Current current) {
        return _isCleaning();
    }


    @Override
    public void startCleaningRoom(int roomId, Current current) throws DeviceTurnedOffError, OngoingCleanngError, RoomNotFoundError, CleaningScheduleConflictError {
        if (!_isTurnedOn) {
            System.out.printf("%s is turned off\n", deviceName);
            throw new DeviceTurnedOffError();
        }
        else if (_isCleaning()) {
            System.out.printf("%s is already cleaning\n", deviceName);
            throw new OngoingCleanngError();
        }

        Room room = getRoomById(roomId);

        LocalDateTime now = LocalDateTime.now();

        LocalDateTime possibleCleaningEndTime = getCleaningEndTime(room.area);
        System.out.println(possibleCleaningEndTime);
        if (isCleaningScheduled(now, possibleCleaningEndTime)) {
            System.out.printf("Cleaning schedule conflict for %s\n", deviceName);
            throw new CleaningScheduleConflictError();
        }

        System.out.printf("%s has started cleaning %s\n", deviceName, room.name);
        cleaningEndTime = possibleCleaningEndTime;
    }

    private Room getRoomById(int roomId) throws RoomNotFoundError {
        for (Room room : rooms) {
            if (room.id == roomId) {
                return room;
            }
        }
        System.out.printf("Room with id %d not found\n", roomId);
        throw new RoomNotFoundError();
    }

    @Override
    public CleaningSchedule addCleaningSchedule(int roomId, Date date, Current current) throws InvalidDate, RoomNotFoundError, CleaningScheduleConflictError {
        Room room = getRoomById(roomId);
        LocalDateTime cleaningStartDateTime = _validateDate(date);
        LocalDateTime cleaningEndDateTime = getCleaningEndTime(room.area);
        if (isCleaningScheduled(cleaningStartDateTime, cleaningEndDateTime)) {
            System.out.printf("Cleaning schedule conflict for %s\n", deviceName);
            throw new CleaningScheduleConflictError();
        }
        CleaningSchedule cleaningSchedule = new CleaningSchedule(
            getNextScheduleId(),
            room,
            new Date(
                cleaningStartDateTime.getYear(),
                cleaningStartDateTime.getMonthValue(),
                cleaningStartDateTime.getDayOfMonth(),
                cleaningStartDateTime.getHour(),
                cleaningStartDateTime.getMinute()
            )
        );
        System.out.printf("Cleaning schedule added for %s\n", deviceName);
        cleaningSchedules.add(cleaningSchedule);
        return cleaningSchedule;
    }

    private int getNextScheduleId() {
        int maxScheduleId = 0;
        for (CleaningSchedule schedule : cleaningSchedules) {
            if (schedule.id > maxScheduleId) {
                maxScheduleId = schedule.id;
            }
        }
        return maxScheduleId + 1;
    }

    private LocalDateTime _validateDate(Date date) throws InvalidDate {
        try {
            LocalDateTime cleaningDate = LocalDateTime.of(
                date.year,
                date.month,
                date.day,
                date.hour,
                date.minute
            );
            if (cleaningDate.isBefore(LocalDateTime.now())) {
                System.out.printf("Cleaning date for %s is in the past\n", deviceName);
                throw new InvalidDate();
            }
            return cleaningDate;
        } catch (DateTimeException e) {
            System.out.printf("Invalid date for %s\n", deviceName);
            throw new InvalidDate();
        }
    }

    @Override
    public CleaningSchedule removeCleaningSchedule(int scheduleId, Current current) throws ScheduleNotFoundError {
        CleaningSchedule schedule = getScheduleById(scheduleId);
        System.out.printf("Cleaning schedule %d removed for %s\n", scheduleId, deviceName);
        cleaningSchedules.remove(schedule);
        return schedule;
    }

    private CleaningSchedule getScheduleById(int scheduleId) throws ScheduleNotFoundError {
        for (CleaningSchedule schedule : cleaningSchedules) {
            if (schedule.id == scheduleId) {
                return schedule;
            }
        }
        System.out.printf("Cleaning schedule with id %d not found\n", scheduleId);
        throw new ScheduleNotFoundError();
    }

    @Override
    public CleaningSchedule[] getCleaningSchedules(Current current) {
        return cleaningSchedules.toArray(new CleaningSchedule[0]);
    }

    @Override
    public Room[] getRooms(Current current) {
        return rooms;
    }

    @Override
    public void setRoomName(int roomId, String name, Current current) throws RoomNotFoundError {
        Room room = getRoomById(roomId);
        System.out.printf("Room with id %s renamed to %s\n", room.id, name);
        room.name = name;
    }

    @Override
    protected DeviceCategory getDeviceCategory() {
        return DeviceCategory.CLEANING_ROBOT;
    }
}
