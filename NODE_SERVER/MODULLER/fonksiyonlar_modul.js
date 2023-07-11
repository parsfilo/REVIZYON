var { exec } = require("child_process");


module.exports = {
    SISTEM_RESET_FONK: function (LOCAL_SOKET_PORT) {
        exec('killall python3');
        exec('rm -rf /home/pi/Desktop/REVIZYON/PYTHON_CLIENT/__pycache__');
        exec('killall chromium-browser');
        exec(`export DISPLAY=:0;chromium-browser --disable-gpu --kiosk http://localhost:${LOCAL_SOKET_PORT}/`);
        exec('export DISPLAY=:0;lxterminal --geometry=2x8 --command="/usr/bin/python3 /home/pi/Desktop/REVIZYON/PYTHON_CLIENT/SOKET_MAIN.py"');
        // console.log("SISTEM_RESET_FONK");
    },

    INTERNET_KONTROL: function () {
        exec(`ping -c 1 ${REMOTE_SERVER_IP}`, function (error, stdout, stderr) {
            if (error !== null) {
                console.log("İnternet Kesildi");
                console.log(moment().format("HH:mm:ss DD/MM/YYYY"));
            }
        });
        // setInterval(INTERNET_KONTROL,10000);
    }

}