const {SmartHome} = require("../../generated/smarthome");
const DEVICE_COMMON_ACTIONS = ["turnOn", "turnOff", "isTurnedOn"];

async function handleDevice(deviceName, action, args, proxy) {
    switch(action) {
        case "turnOn":
            await proxy.turnOn();
            console.log(`${deviceName} has been turned on.`);
            break;
        case "turnOff":
            await proxy.turnOff();
            console.log(`${deviceName} has been turned off.`);
            break;
        case "isTurnedOn":
            const isTurnedOn = await proxy.isTurnedOn();
            if (isTurnedOn)
                console.log(`${deviceName} is turned on.`);
            else
                console.log(`${deviceName} is turned off.`);
            break;
        default:
            console.log("Invalid action");
            break;
    }
}
async function handleSimpleBulb(deviceName, action, args, proxy) {
    const availableActions = [...DEVICE_COMMON_ACTIONS];
    switch (action) {
        case "list":
            console.log(`Available actions: ${availableActions.join(", ")}`);
            break;
        default:
            await handleDevice(deviceName, action, args, proxy);
            break;
    }
}

async function handleDimmableBulb(deviceName, action, args, proxy) {
    const availableActions = [...DEVICE_COMMON_ACTIONS, "setBrightness", "getBrightness"];
    switch (action) {
        case "list":
            console.log(`Available actions: ${availableActions.join(", ")}`);
            break;
        case "setBrightness":
            try{
                const brightness_ = parseInt(args[0])
                await proxy.setBrightness(brightness_);
                console.log(`${deviceName} brightness has been set to ${brightness_}`);
            } catch (e) {
                console.log("Invalid arguments");
                return;
            }
            break;
        case "getBrightness":
            let brightness = await proxy.getBrightness();
            console.log(`${deviceName} brightness is ${brightness}`);
            break;
        default:
            await handleSimpleBulb(deviceName, action, args, proxy);
            break

    }
}

async function handleColorBulb(deviceName, action, args, proxy) {
    const availableActions = [
        ...DEVICE_COMMON_ACTIONS, "setBrightness", "getBrightness", "setColor", "getColor"
    ];
    switch (action) {
        case "list":
            console.log(`Available actions: ${availableActions.join(", ")}`);
            break;
        case "setColor":
            try {
                const red = parseInt(args[0]);
                const green = parseInt(args[1]);
                const blue = parseInt(args[2]);
                await proxy.setColor(new SmartHome.Color(red, green, blue));
                console.log(`${deviceName} color has been set to (${red}, ${green}, ${blue})`);
            } catch (e) {
                console.log("Invalid arguments");
                return;
            }
            break;
        case "getColor":
            let color = await proxy.getColor();
            console.log(`${deviceName} color is (${color.red}, ${color.green}, ${color.blue})`);
            break;
        default:
            await handleSimpleBulb(deviceName, action, args, proxy);
            break;
    }
}


async function handleSimpleCleaningRobot(deviceName, action, args, proxy) {
    const availableActions = [...DEVICE_COMMON_ACTIONS, "startCleaningAllRooms", "stopCleaning", "isCleaning"];
    switch (action) {
        case "list":
            console.log(`Available actions: ${availableActions.join(", ")}`);
            break;
        case "startCleaningAllRooms":
            try {
                await proxy.startCleaningAllRooms();
            } catch (e) {
                if (e instanceof SmartHome.DeviceTurnedOffError) {
                    console.log(`${deviceName} is turned off.`);
                    return;
                }
                else if (e instanceof SmartHome.OngoingCleanngError) {
                    console.log(`${deviceName} is already cleaning.`);
                    return;
                }
                else if (e instanceof SmartHome.CleaningScheduleConflictError) {
                    console.log(`${deviceName} has a cleaning schedule at the same time.`);
                    return;
                }
            }
            console.log(`${deviceName} has started cleaning all rooms.`);
            break;
        case "stopCleaning":
            await proxy.stopCleaning();
            console.log(`${deviceName} has stopped cleaning.`);
            break;
        case "isCleaning":
            const isCleaning = await proxy.isCleaning();
            if (isCleaning)
                console.log(`${deviceName} is cleaning.`);
            else
                console.log(`${deviceName} is not cleaning.`);
            break;
        default:
            await handleDevice(deviceName, action, args, proxy);
            break;
    }
}

async function handleSmartCleaningRobot(deviceName, action, args, proxy) {
    const availableActions = [
        ...DEVICE_COMMON_ACTIONS, "startCleaningAllRooms", "stopCleaning", "isCleaning",
        "startCleaningRoom", "getRooms", "setRoomName",
        "addCleaningSchedule", "removeCleaningSchedule", "getCleaningSchedules"
    ];
    switch(action) {
        case "list":
            console.log(`Available actions: ${availableActions.join(", ")}`);
            break;
        case "startCleaningRoom":
            try {
                const roomId = parseInt(args[0]);
                await proxy.startCleaningRoom(roomId);
                console.log(`${deviceName} has started cleaning room ${roomId}`);
            } catch(e) {
                if (e instanceof SmartHome.RoomNotFoundError) {
                    console.log("Room not found.");
                }
                else if(e instanceof SmartHome.DeviceTurnedOffError) {
                    console.log(`${deviceName} is turned off.`);
                }
                else if(e instanceof SmartHome.OngoingCleanngError) {
                    console.log(`${deviceName} is already cleaning.`);
                }
                else if (e instanceof SmartHome.CleaningScheduleConflictError) {
                    console.log(`${deviceName} has a cleaning schedule at the same time.`);
                }
                else {
                    console.log("Invalid arguments");
                    return;
                }
            }
            break;
        case "getRooms":
            const rooms = await proxy.getRooms();
            for(const room of rooms) {
                console.log(`Id: ${room.id}\t Name: ${room.name}\t Area: ${room.area} m^2`);
            }
            break;
        case "setRoomName":
            try{
                try {
                    const roomId = parseInt(args[0]);
                    const roomName = args[1];
                    await proxy.setRoomName(roomId, roomName);
                } catch(e) {
                    if (e instanceof SmartHome.RoomNotFoundError) {
                        console.log("Room not found.");
                    }
                    else {
                        console.log("Invalid arguments");
                        return;
                    }
                }

            } catch(e) {
                console.log("Invalid arguments");
                return;
            }
            break;
        case "addCleaningSchedule":
            try {
                const room = parseInt(args[0]);
                const date = new SmartHome.Date(
                    parseInt(args[1]),
                    parseInt(args[2]),
                    parseInt(args[3]),
                    parseInt(args[4]),
                    parseInt(args[5])
                );
                await proxy.addCleaningSchedule(room, date);
                console.log(`Cleaning schedule for room ${room} has been added.`);
            } catch (e) {
                if (e instanceof SmartHome.RoomNotFoundError) {
                    console.log("Room not found.");
                }
                else if (e instanceof SmartHome.CleaningScheduleConflictError) {
                    console.log("Cleaning schedule conflict.");
                }
                else if (e instanceof SmartHome.InvalidDate) {
                    console.log("Invalid date.");
                }
                else {
                    console.log("Invalid arguments");
                    return;
                }
            }
            break;
        case "removeCleaningSchedule":
            try {
                const scheduleId = parseInt(args[0]);
                await proxy.removeCleaningSchedule(scheduleId);
                console.log(`Cleaning schedule with id ${scheduleId} has been removed.`);
            } catch(e) {
                if (e instanceof SmartHome.ScheduleNotFoundError) {
                    console.log("Schedule not found.");
                }
                else {
                    console.log("Invalid arguments");
                }
            }
            break;
        case "getCleaningSchedules":
            const schedules = await proxy.getCleaningSchedules();
            for (const schedule of schedules) {
                const d = schedule.date
                const date = new Date(d.year, d.month, d.day, d.hour, d.minute)
                console.log(`Id: ${schedule.id}\t Room: ${schedule.room.id}\t Date: ${date}`);
            }
            break;
        default:
            await handleSimpleCleaningRobot(deviceName, action, args, proxy);
            break;
    }
}


module.exports = {
    handleSimpleBulb,
    handleDimmableBulb,
    handleColorBulb,
    handleSimpleCleaningRobot,
    handleSmartCleaningRobot
}