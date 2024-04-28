const {PORT, SERVER_ADDRESS, USE_UDP} = require("./config");

const {SmartHome} = require("../../generated/smarthome");


function getProxyString(category, name) {
    let result = `${category}/${name}:tcp -h ${SERVER_ADDRESS} -p ${PORT}`;
    if (USE_UDP) {
        result += `:udp -h ${SERVER_ADDRESS} -p ${PORT}`;
    }
    return result;
}

async function getKitchenBulbPrx(communicator) {
    const kitchenBulbBase = communicator.stringToProxy(getProxyString("Bulb", "KitchenLampBulb"));
    const kitchenBulbPrx = await SmartHome.SimpleBulbPrx.checkedCast(kitchenBulbBase);
    if (!kitchenBulbPrx) {
        throw new Error("Invalid proxy");
    }
    return kitchenBulbPrx;
}

async function getBathroomBulbPrx(communicator) {
    const bathroomBulbBase = communicator.stringToProxy(getProxyString("Bulb", "BathroomLampBulb"));
    const bathroomBulbPrx = await SmartHome.SimpleBulbPrx.checkedCast(bathroomBulbBase);
    if (!bathroomBulbPrx) {
        throw new Error("Invalid proxy");
    }
    return bathroomBulbPrx;
}

async function getBedRoomBulbPrx(communicator) {
    const bedRoomBulbBase = communicator.stringToProxy(getProxyString("Bulb", "BedRoomLampBulb"));
    const bedRoomBulbPrx = await SmartHome.DimmableBulbPrx.checkedCast(bedRoomBulbBase);
    if (!bedRoomBulbPrx) {
        throw new Error("Invalid proxy");
    }
    return bedRoomBulbPrx;
}

async function getLivingRoomBulbPrx(communicator) {
    const livingRoomBulbBase = communicator.stringToProxy(getProxyString("Bulb", "LivingRoomLampBulb"));
    const livingRoomBulbPrx = await SmartHome.ColorBulbPrx.checkedCast(livingRoomBulbBase);
    if (!livingRoomBulbPrx) {
        throw new Error("Invalid proxy");
    }
    return livingRoomBulbPrx;
}


async function getGarageCleaningRobotPrx(communicator) {
    const garageCleaningRobotBase = communicator.stringToProxy(getProxyString("CleaningRobot", "GarageCleaningRobot"));
    const garageCleaningRobotPrx = await SmartHome.SimpleCleaningRobotPrx.checkedCast(garageCleaningRobotBase);
    if (!garageCleaningRobotPrx) {
        throw new Error("Invalid proxy");
    }
    return garageCleaningRobotPrx;
}

async function getMainCleaningRobotPrx(communicator) {
    const mainCleaningRobotBase = communicator.stringToProxy(getProxyString("CleaningRobot", "MainCleaningRobot"));
    const mainCleaningRobotPrx = await SmartHome.SmartCleaningRobotPrx.checkedCast(mainCleaningRobotBase);
    if (!mainCleaningRobotPrx) {
        throw new Error("Invalid proxy");
    }
    return mainCleaningRobotPrx;
}

module.exports = {
    getKitchenBulbPrx,
    getBathroomBulbPrx,
    getBedRoomBulbPrx,
    getLivingRoomBulbPrx,
    getGarageCleaningRobotPrx,
    getMainCleaningRobotPrx
}