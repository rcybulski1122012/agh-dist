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

main(process.argv);