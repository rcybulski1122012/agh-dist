const SERVER_ADDRESS = "127.0.0.1";
const PORT = getServerPort(process.argv);
const USE_UDP = false;

function getServerPort(argv) {
    for (let arg of argv) {
        if (arg.startsWith("--port=")) {
            return arg.split("=")[1];
        }
    }

    return 10000;
}

module.exports = {
    SERVER_ADDRESS,
    PORT,
    USE_UDP
}