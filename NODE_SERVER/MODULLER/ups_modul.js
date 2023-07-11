var { exec } = require("child_process");


module.exports = {

    UPS_VERI_FUNC: function (io) {
        exec("upsc makelsan", (error, stdout, stderr) => {
            var ups_dict = {}
            var ups_durum;
            var ups_giris_voltaj;
            var ups_batarya_voltaj;
            var sebeke_durum;

            ups_satirlar = stdout.split('\n')

            if (ups_satirlar.length < 2) {
                ups_dict["ups_durum"] = "BAGLI_DEGIL";
                ups_dict["ups_giris_voltaj"] = 0;
                ups_dict["ups_batarya_voltaj"] = 0;
                ups_dict["sebeke_durum"] = 0;
                io.emit('ups_dict', ups_dict);
            } else {
                for (let i = 0; i < ups_satirlar.length - 1; i++) {
                    if (ups_satirlar[i].startsWith('battery.voltage: ')) {
                        ups_batarya_voltaj = ups_satirlar[i].split(': ')[1];
                    }

                    if (ups_satirlar[i].startsWith('input.voltage: ')) {
                        ups_giris_voltaj = ups_satirlar[i].split(': ')[1]
                    }

                    if (ups_satirlar[i].startsWith('ups.status: ')) {
                        if (ups_satirlar[i].split(': ')[1] == "OL") {
                            sebeke_durum = "AKTIF"
                            ups_durum = "BAGLI"

                        } else {
                            sebeke_durum = "DEAKTIF"
                            ups_durum = "AKU"
                        }
                    }
                }
                ups_dict["ups_durum"] = ups_durum;
                ups_dict["ups_giris_voltaj"] = ups_giris_voltaj;
                ups_dict["ups_batarya_voltaj"] = ups_batarya_voltaj;
                ups_dict["sebeke_durum"] = sebeke_durum;
                io.emit('ups_dict', ups_dict);
            }
        });
    }
}