from socketio import Client
import time
from os import system
from FONKSIYONLAR import *
from ADXL355_IVME_OKU import *
from MCP23017_LIB import *
from configparser import ConfigParser
from threading import Timer



sio = Client()

config = ConfigParser()
config.read('../config.ini')


CIHAZ_ID = config['AYARLAR']['CIHAZ_ID']

SISMIK_ALARM_KANAL = str(config['AYARLAR']['SISMIK_ALARM_KANAL'])
DEPREM_ALARM_KANAL = str(config['AYARLAR']['DEPREM_ALARM_KANAL'])
SISMIK_ALARM_BOT_TOKEN = str(config['AYARLAR']['SISMIK_ALARM_BOT_TOKEN'])
DEPREM_ALARM_BOT_TOKEN = str(config['AYARLAR']['DEPREM_ALARM_BOT_TOKEN'])

DEPREM_ALARM_SURESI = int(config['AYARLAR']['DEPREM_ALARM_SURESI'])
SENSOR_ALARM_SURESI = int(config['AYARLAR']['SENSOR_ALARM_SURESI'])
SISTEM_TEST_SURESI = int(config['AYARLAR']['SISTEM_TEST_SURESI'])

print(config['AYARLAR']['CIHAZ_ID'])

LED_BUZZER_NORMAL_DURUM()
ROLERI_LOW_YAP_FONK()


def tum_veri_dict_fonk():
    zaman = int(time.time())
    zaman_ms = int(time.time() * 1000)
    ivme_dict = ivme_dict_fonk(ORNEK_SAYISI, X_KALIBRE, Y_KALIBRE, Z_KALIBRE, YUVARLA, SISMIK_ESIK, DEPREM_ESIK)
    sismik_durum_dict = ivme_dict["sismik_durum_dict"]
    sensor_dict = SENSOR_OKU_FONK()
    veri_dict = {
        "CIHAZ_ID": CIHAZ_ID,
        "zaman": zaman,
        "zaman_ms": zaman_ms,
        "ivme_dict": ivme_dict,
        "sismik_durum_dict": sismik_durum_dict,
        "sensor_dict": sensor_dict,
        "SISMIK_ESIK": SISMIK_ESIK,
        "DEPREM_ESIK": DEPREM_ESIK
    }
    return veri_dict


def tum_veri_yolla():
    while True:
        try:
            tum_veri_dict = tum_veri_dict_fonk()
            SISMIK_ALARM = tum_veri_dict["sismik_durum_dict"]["SISMIK_ALARM"]
            DEPREM_ALARM = tum_veri_dict["sismik_durum_dict"]["DEPREM_ALARM"]
            SENSOR_ALARM = tum_veri_dict["sensor_dict"]["SENSOR_ALARM"]

            tum_veri_dict["SISTEM_DURUM"] = "NORMAL"
            sio.emit('tum_veri_dict', tum_veri_dict)

            # print("x_std_spm: ", tum_veri_dict["ivme_dict"]["x_std_spm"])
            # print("y_std_spm: ", tum_veri_dict["ivme_dict"]["y_std_spm"])
            # print("z_std_spm: ", tum_veri_dict["ivme_dict"]["z_std_spm"])
            # print("r_ivme: ", tum_veri_dict["ivme_dict"]["r_ivme"])
            # print("mmi_olcek: ", tum_veri_dict["ivme_dict"]["mmi_olcek"])
            # print()

            while SISMIK_ALARM == True and DEPREM_ALARM == False:
                SISMIK_ALARM_ZAMANI = int(time.time())

                Timer(0.0, MONGO_SISMIK_VERI_GIR(SISMIK_ALARM_ZAMANI, tum_veri_dict)).start()
                Timer(0.0, TELEGRAM_SISMIK_UYARI_GONDER_FONK(SISMIK_ALARM_BOT_TOKEN,SISMIK_ALARM_KANAL,SISMIK_ALARM_ZAMANI,tum_veri_dict)).start()
                Timer(1.5, EKRAN_GORUNTUSU_AL).start()

                tum_veri_dict = tum_veri_dict_fonk()
                SISMIK_ALARM = tum_veri_dict["sismik_durum_dict"]["SISMIK_ALARM"]
                DEPREM_ALARM = tum_veri_dict["sismik_durum_dict"]["DEPREM_ALARM"]
                tum_veri_dict["SISTEM_DURUM"] = "SISMIK_ALARM"
                sio.emit('tum_veri_dict', tum_veri_dict)
                

            while DEPREM_ALARM == True:
                role_dict = ROLERI_HIGH_YAP_FONK()
                sio.emit('role_dict', role_dict)
                LED_BUZZER_ALARM_DURUM()

                SISMIK_ALARM_ZAMANI = int(time.time())
                DEPREM_ALARM_ZAMANI = int(time.time())

                Timer(0.0, MONGO_SISMIK_VERI_GIR(SISMIK_ALARM_ZAMANI, tum_veri_dict)).start()
                Timer(0.0, MONGO_DEPREM_VERI_GIR(DEPREM_ALARM_ZAMANI, tum_veri_dict)).start()
                Timer(0.0, TELEGRAM_DEPREM_UYARI_GONDER_FONK(DEPREM_ALARM_BOT_TOKEN,DEPREM_ALARM_KANAL,DEPREM_ALARM_ZAMANI,tum_veri_dict)).start()
                Timer(1.5, EKRAN_GORUNTUSU_AL).start()

                sio.emit('tum_veri_dict', tum_veri_dict)
                for n in range(DEPREM_ALARM_SURESI):
                    tum_veri_dict = tum_veri_dict_fonk()
                    DEPREM_ALARM = tum_veri_dict["sismik_durum_dict"]["DEPREM_ALARM"]
                    tum_veri_dict["SISTEM_DURUM"] = "DEPREM_ALARM"
                    sio.emit('tum_veri_dict', tum_veri_dict)

                role_dict = ROLERI_LOW_YAP_FONK()
                sio.emit('role_dict', role_dict)
                LED_BUZZER_NORMAL_DURUM()
                

            while SENSOR_ALARM == True:
                f = open("../sensor_dict.txt", "a")
                f.write(str(time.time()))
                f.write('\n')
                f.write(str(tum_veri_dict["sensor_dict"]))
                f.write('\n')
                f.write('\n')
                f.close()

                # role_dict = ROLERI_HIGH_YAP_FONK()
                # sio.emit('role_dict', role_dict)
                # LED_BUZZER_ALARM_DURUM()

                # sensor_dict = tum_veri_dict["sensor_dict"]
                # SENSOR_ALARM_ZAMANI = int(time.time())

                # MONGO_SENSOR_VERI_GIR(SENSOR_ALARM_ZAMANI, sensor_dict)

                # for n in range(SENSOR_ALARM_SURESI):
                #     tum_veri_dict = tum_veri_dict_fonk()
                #     SENSOR_ALARM = tum_veri_dict["sismik_durum_dict"]["SENSOR_ALARM"]
                #     tum_veri_dict["SISTEM_DURUM"] = "SENSOR_ALARM"
                #     sio.emit('tum_veri_dict', tum_veri_dict)

                # role_dict = ROLERI_LOW_YAP_FONK()
                # sio.emit('role_dict', role_dict)
                # LED_BUZZER_NORMAL_DURUM()
                # EKRAN_GORUNTUSU_AL()

        except Exception as e:
            print(e)
            continue


@sio.event
def komut_kanal(data):
    if data == "SISTEM_TEST":
        LED_BUZZER_TEST_DURUM()
        role_dict = ROLERI_HIGH_YAP_FONK()
        sio.emit('role_dict', role_dict)
        for n in range(SISTEM_TEST_SURESI):
            time.sleep(1)
        LED_BUZZER_NORMAL_DURUM()
        role_dict = ROLERI_LOW_YAP_FONK()
        sio.emit('role_dict', role_dict)

    if data == "SISTEM_RESET":
        LED_BUZZER_NORMAL_DURUM()
        role_dict = ROLERI_LOW_YAP_FONK()
        sio.emit('role_dict', role_dict)

    if data == "CIHAZ_RESET":
        LED_BUZZER_NORMAL_DURUM()
        role_dict = ROLERI_LOW_YAP_FONK()
        sio.emit('role_dict', role_dict)
        system("sudo reboot")


@sio.event
def connect():
    print('SOKET SERVER BAGLANDI')
    sio.start_background_task(tum_veri_yolla)
    LED_BUZZER_NORMAL_DURUM()
    role_dict = ROLERI_LOW_YAP_FONK()
    sio.emit('role_dict', role_dict)


@sio.event
def disconnect():
    print('SOKET SERVER BAGLANTI KESILDI')


sio.connect('http://localhost:3001/')
sio.wait()
