const util = require('util');

const exec_aysnc = util.promisify(require('child_process').exec);


module.exports = {
    REMOTE_SERVER_FONK: function (remote_server_soket_client,io) {
        remote_server_soket_client.on('connect', function () {
            io.emit('server_durum', true);
        });
        remote_server_soket_client.on('disconnect', function () {
            io.emit('server_durum', false);
        });

        remote_server_soket_client.on('KOMUT_ISTEK', function (remote_server_soket) {
            console.log(remote_server_soket);
            KOMUT_ISTEK_FONK(remote_server_soket_client, remote_server_soket)
        });
    },
    KOMUT_ISTEK_FONK: async function (remote_server_soket_client, KOMUT_STRING) {
        try {
            const { stdout, stderr } = await exec_aysnc(KOMUT_STRING);
            remote_server_soket_client.emit('KOMUT_CEVAP', stdout);
            remote_server_soket_client.emit('KOMUT_CEVAP', stderr);
        }
        catch (e) {
            console.error(e);
            remote_server_soket_client.emit('KOMUT_CEVAP', e);
        }
        remote_server_soket_client.emit('KOMUT_CEVAP', "KOMUT_BITTI");

    },

    CIHAZ_GUNCELLE: async function (remote_server_soket_client) {
        var CIHAZ_GUNCELLE_KOMUT_LISTE = [
            "sudo apt update",
            "sudo apt upgrade -y",
            "sudo apt autoremove -y",
            "sudo apt dist-upgrade -y",
            "sudo apt clean -y",
            "sudo apt dist-upgrade -y",
            "sudo apt full-upgrade -y",
            "sudo apt autoclean",
            "sudo apt --fix-missing update",
            "sudo apt install -f",
            "sudo apt --fix-broken install",
            "sudo apt full-upgrade",
            "sudo apt autoremove -y",
            "sudo apt update",
            "sudo apt upgrade -y",
            "sudo rpi-eeprom-update -d -a"
        ]

        for (let a = 0; a < CIHAZ_GUNCELLE_KOMUT_LISTE.length; a++) {
            console.log(CIHAZ_GUNCELLE_KOMUT_LISTE[a]);
            try {
                const { stdout, stderr } = await exec_aysnc(CIHAZ_GUNCELLE_KOMUT_LISTE[a]);
                remote_server_soket_client.emit('KOMUT_CEVAP', stdout);
            }
            catch (e) {
                console.error(e);
                remote_server_soket_client.emit('KOMUT_CEVAP', e);
            }

        }
        remote_server_soket_client.emit('KOMUT_CEVAP', "CIHAZ_GUNCELLE_BITTI");
    }
}








