const Ice = require("ice").Ice;
const readline = require('readline');
const {
    getKitchenBulbPrx,
    getBathroomBulbPrx,
    getBedRoomBulbPrx,
    getGarageCleaningRobotPrx,
    getLivingRoomBulbPrx,
    getMainCleaningRobotPrx
} = require("./proxies");
const {
    handleSimpleBulb,
    handleDimmableBulb,
    handleColorBulb,
    handleSimpleCleaningRobot,
    handleSmartCleaningRobot
} = require("./handlers");



const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

async function main(args) {
    let communicator;
    try {
        communicator = Ice.initialize(args);
        const devices = {
            "KitchenLampBulb": await getKitchenBulbPrx(communicator),
            "BathroomLampBulb": await getBathroomBulbPrx(communicator),
            "BedRoomLampBulb": await getBedRoomBulbPrx(communicator),
            "LivingRoomLampBulb": await getLivingRoomBulbPrx(communicator),
            "GarageCleaningRobot": await getGarageCleaningRobotPrx(communicator),
            "MainCleaningRobot": await getMainCleaningRobotPrx(communicator),
        }

        rl.setPrompt(">>> ");
        rl.prompt();
        rl.on("line", async (command) => {
            if(command === "exit") {
                rl.close();
                process.exit(0);
            }
            else if(command === "list") {
                for (const deviceName in devices) {
                    console.log(" - " + deviceName);
                }
            }
            else if (command === "test_bulbs") {
                await testBulbs(devices);
            }
            else if (command === "test_robots") {
                await testCleaningRobots(devices);
            }
            else if (command !== "") {
                await handleCommand(command, devices);
            }


            rl.prompt();
        });

        while(true) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    catch(ex)
    {
        console.log(ex.toString());
        process.exitCode = 1;
    }
    finally
    {
        if(communicator)
        {
            await communicator.destroy();
        }
    }

    console.log("Main func finished");
}

async function handleCommand(command, proxies) {
    const parts = command.split(":");
    if (parts.length < 2) {
        console.log("Invalid command");
        return;
    }

    const [deviceName, action, ...args] = parts;
    const proxy = proxies[deviceName];
    switch (deviceName) {
        case "KitchenLampBulb":
        case "BathroomLampBulb":
            await handleSimpleBulb(deviceName, action, args, proxy);
            break;
        case "BedRoomLampBulb":
            await handleDimmableBulb(deviceName, action, args, proxy);
            break;
        case "LivingRoomLampBulb":
            await handleColorBulb(deviceName, action, args, proxy);
            break;
        case "GarageCleaningRobot":
            await handleSimpleCleaningRobot(deviceName, action, args, proxy);
            break;
        case "MainCleaningRobot":
            await handleSmartCleaningRobot(deviceName, action, args, proxy);
            break;
        default:
            console.log("Invalid device name or it's unavailable");
    }
}

async function testBulbs(proxies) {
    await handleCommand("KitchenLampBulb:isTurnedOn", proxies);
    await handleCommand("KitchenLampBulb:turnOn", proxies);
    await handleCommand("BathroomLampBulb:turnOff", proxies);

    await handleCommand("BedRoomLampBulb:getBrightness", proxies);
    await handleCommand("BedRoomLampBulb:setBrightness:100", proxies);
    await handleCommand("BedRoomLampBulb:setBrightness:150", proxies);
    await handleCommand("BedRoomLampBulb:setBrightness:-50", proxies);

    await handleCommand("LivingRoomLampBulb:getColor", proxies);
    await handleCommand("LivingRoomLampBulb:setColor:255:0:0", proxies);
    await handleCommand("LivingRoomLampBulb:getColor", proxies);
    await handleCommand("LivingRoomLampBulb:setColor:256:0:0", proxies);
}

async function testCleaningRobots(proxies) {
    await handleCommand("GarageCleaningRobot:isCleaning", proxies);
    await handleCommand("GarageCleaningRobot:startCleaningAllRooms", proxies);
    await handleCommand("GarageCleaningRobot:turnOn", proxies);
    await handleCommand("GarageCleaningRobot:startCleaningAllRooms", proxies);
    await new Promise(resolve => setTimeout(resolve, 5000));
    await handleCommand("GarageCleaningRobot:isCleaning", proxies);
    await handleCommand("GarageCleaningRobot:startCleaningAllRooms", proxies);
    await handleCommand("GarageCleaningRobot:stopCleaning", proxies);
    console.log("-----------------------")
    await handleCommand("MainCleaningRobot:isCleaning", proxies);
    await handleCommand("MainCleaningRobot:turnOn", proxies);
    await handleCommand("MainCleaningRobot:getRooms", proxies);
    await handleCommand("MainCleaningRobot:getCleaningSchedules", proxies);
    await handleCommand("MainCleaningRobot:addCleaningSchedule:1:2024:10:10:10:10", proxies);
    await handleCommand("MainCleaningRobot:addCleaningSchedule:1:2022:10:10:10:10", proxies);
    await handleCommand("MainCleaningRobot:getCleaningSchedules", proxies);
    await handleCommand("MainCleaningRobot:removeCleaningSchedule:1", proxies);
    await handleCommand("MainCleaningRobot:startCleaningRoom:1", proxies);



}


main(process.argv);