from pymongo import MongoClient
from os import system
from pyautogui import screenshot
from datetime import datetime

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["CIHAZ_VERILER"]
SON_SISMIK_TABLO = mydb["SON_SISMIK"]
SON_DEPREM_TABLO = mydb["SON_DEPREM"]
SON_SENSOR_TABLO = mydb["SON_SENSOR"]


def EKRAN_GORUNTUSU_AL():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    dt_object = str(datetime.fromtimestamp(timestamp))
    tarih = dt_object.split(" ")[0]
    saat = dt_object.split(" ")[1].split(".")[0]
    myScreenshot = screenshot()
    system("mkdir -p /home/pi/Desktop/REVIZYON/EKRAN_GORUNTULERI/%s" % (tarih))
    myScreenshot.save(
        '/home/pi/Desktop/REVIZYON/EKRAN_GORUNTULERI/%s/%s.PNG' % (tarih, saat,))


def MONGO_SISMIK_VERI_GIR(SISMIK_ALARM_ZAMANI, tum_veri_dict):
    son_sismik_dict = {
        "SISMIK_ALARM_ZAMANI": SISMIK_ALARM_ZAMANI,
        "x_std": tum_veri_dict["ivme_dict"]["x_std_spm"],
        "y_std": tum_veri_dict["ivme_dict"]["y_std_spm"],
        "z_std": tum_veri_dict["ivme_dict"]["z_std_spm"],
        "r_std": tum_veri_dict["ivme_dict"]["r_ivme"],
        "mmi_olcek": tum_veri_dict["ivme_dict"]["mmi_olcek"]
    }
    SON_SISMIK_TABLO.insert_one(son_sismik_dict)


def MONGO_DEPREM_VERI_GIR(DEPREM_ALARM_ZAMANI, tum_veri_dict):
    son_deprem_dict = {
        "DEPREM_ALARM_ZAMANI": DEPREM_ALARM_ZAMANI,
        "x_std": tum_veri_dict["ivme_dict"]["x_std_spm"],
        "y_std": tum_veri_dict["ivme_dict"]["y_std_spm"],
        "z_std": tum_veri_dict["ivme_dict"]["z_std_spm"],
        "r_std": tum_veri_dict["ivme_dict"]["r_ivme"],
        "mmi_olcek": tum_veri_dict["ivme_dict"]["mmi_olcek"]
    }
    SON_DEPREM_TABLO.insert_one(son_deprem_dict)


def MONGO_SENSOR_VERI_GIR(SENSOR_ALARM_ZAMANI, sensor_dict):
    sensor_dict["SENSOR_ALARM_ZAMANI"] = SENSOR_ALARM_ZAMANI
    SON_SENSOR_TABLO.insert_one(sensor_dict)


def TELEGRAM_SISMIK_UYARI_GONDER_FONK(SISMIK_ALARM_BOT_TOKEN,SISMIK_ALARM_KANAL,SISMIK_ALARM_ZAMANI,tum_veri_dict):
    import requests
    from datetime import datetime
    SAAT = datetime.fromtimestamp(SISMIK_ALARM_ZAMANI).strftime("%H:%M:%S")
    TARIH = datetime.fromtimestamp(SISMIK_ALARM_ZAMANI).strftime("%d/%m/%Y")
    BOT_MESAJ = (
        "*-SİSMİK ALARM-*" + "\n" +
        "*Cihaz ID: *" + str(tum_veri_dict["CIHAZ_ID"]) + "\n" +
        "*SAAT: *" + str(SAAT) + "\n" +
        "*TARIH: *" + str(TARIH) + "\n" +
        "*X(cm/s2): *" + str(tum_veri_dict["ivme_dict"]["x_std_spm"]) + "\n" +
        "*Y(cm/s2): *" + str(tum_veri_dict["ivme_dict"]["y_std_spm"]) + "\n" +
        "*Z(cm/s2): *" + str(tum_veri_dict["ivme_dict"]["z_std_spm"]) + "\n" +
        "*MMI Olcek *" + str(tum_veri_dict["ivme_dict"]["mmi_olcek"]) + "\n"
    )
    REQ_URL = f'https://api.telegram.org/bot{SISMIK_ALARM_BOT_TOKEN}/sendMessage?chat_id={SISMIK_ALARM_KANAL}&parse_mode=Markdown&text={BOT_MESAJ}'
    req = requests.get(REQ_URL)


def TELEGRAM_DEPREM_UYARI_GONDER_FONK(DEPREM_ALARM_BOT_TOKEN,DEPREM_ALARM_KANAL,DEPREM_ALARM_ZAMANI,tum_veri_dict):
    import requests
    from datetime import datetime
    SAAT = datetime.fromtimestamp(DEPREM_ALARM_ZAMANI).strftime("%H:%M:%S")
    TARIH = datetime.fromtimestamp(DEPREM_ALARM_ZAMANI).strftime("%d/%m/%Y")
    BOT_MESAJ = (
        "*-DEPREM ALARM-*" + "\n" +
        "*Cihaz ID: *" + str(tum_veri_dict["CIHAZ_ID"]) + "\n" +
        "*SAAT: *" + str(SAAT) + "\n" +
        "*TARIH: *" + str(TARIH) + "\n" +
        "*X(cm/s2): *" + str(tum_veri_dict["ivme_dict"]["x_std_spm"]) + "\n" +
        "*Y(cm/s2): *" + str(tum_veri_dict["ivme_dict"]["y_std_spm"]) + "\n" +
        "*Z(cm/s2): *" + str(tum_veri_dict["ivme_dict"]["z_std_spm"]) + "\n" +
        "*MMI Olcek *" + str(tum_veri_dict["ivme_dict"]["mmi_olcek"]) + "\n"
    )
    REQ_URL = f'https://api.telegram.org/bot{DEPREM_ALARM_BOT_TOKEN}/sendMessage?chat_id={DEPREM_ALARM_KANAL}&parse_mode=Markdown&text={BOT_MESAJ}'
    req = requests.get(REQ_URL)

