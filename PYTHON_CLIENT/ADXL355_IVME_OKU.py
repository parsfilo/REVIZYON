from cmath import pi
from ADXL355_LIB import ADXL355
import numpy as np
from statistics import stdev
from math import sqrt, log10
from time import sleep
from configparser import ConfigParser

config = ConfigParser()
config.read('../config.ini')

SISMIK_ESIK = float(config['AYARLAR']['SISMIK_ESIK'])
DEPREM_ESIK = float(config['AYARLAR']['DEPREM_ESIK'])

FILTRE_ESIK = float(config['AYARLAR']['FILTRE_ESIK'])
FILTRE_YUZDE_ESIK = float(config['AYARLAR']['FILTRE_YUZDE_ESIK'])

ORNEK_SAYISI = int(config['AYARLAR']['ORNEK_SAYISI'])

x_kal_deger = int(config['AYARLAR']['x_kal_deger'])
y_kal_deger = int(config['AYARLAR']['y_kal_deger'])
z_kal_deger = int(config['AYARLAR']['z_kal_deger'])

YUVARLA = int(config['AYARLAR']['YUVARLA'])


adxl355 = ADXL355()
adxl355.start()
sleep(0.1)


def SINYAL_FILTRE(IVME_LISTE, FILTRE_ESIK):
    FILTRE_ESIK_USTU_LISTE = list(filter(lambda score: score >= FILTRE_ESIK, np.abs(IVME_LISTE)))
    FILTRE_YUZDE_DEGER = round(len(FILTRE_ESIK_USTU_LISTE) / len(IVME_LISTE) * 100, 1)
    return FILTRE_YUZDE_DEGER


def PGA_FONK(LISTE):
    ivme_max = np.amax(LISTE)
    ivme_min = np.amin(LISTE)
    pga = round(abs(ivme_max-ivme_min) / 2, 1)
    return pga


def ivme_dict_fonk(ORNEK_SAYISI, X_KALIBRE, Y_KALIBRE, Z_KALIBRE, YUVARLA, SISMIK_ESIK, DEPREM_ESIK):
    x_ivme_liste = []
    y_ivme_liste = []
    z_ivme_liste = []
    x_ivme_liste_ham = []
    y_ivme_liste_ham = []
    z_ivme_liste_ham = []
    while (len(x_ivme_liste) <= ORNEK_SAYISI and len(y_ivme_liste) <= ORNEK_SAYISI and len(z_ivme_liste) <= ORNEK_SAYISI):

        ivmeler = adxl355.getAxis()

        x_ivme_ham = ivmeler[0] * 980.1
        y_ivme_ham = ivmeler[1] * 980.1
        z_ivme_ham = ivmeler[2] * 980.1

        x_ivme_liste_ham.append(x_ivme_ham)
        y_ivme_liste_ham.append(y_ivme_ham)
        z_ivme_liste_ham.append(z_ivme_ham)

        if (x_ivme_ham == 0.0 or y_ivme_ham == 0.0 or z_ivme_ham == 0.0):
            print("SPI_ERROR")
            sleep(0.1)
            print()

        else:
            x_ivme = round(x_ivme_ham + X_KALIBRE, YUVARLA)
            y_ivme = round(y_ivme_ham + Y_KALIBRE, YUVARLA)
            z_ivme = round(z_ivme_ham + Z_KALIBRE, YUVARLA)

            x_ivme_liste.append(x_ivme)
            y_ivme_liste.append(y_ivme)
            z_ivme_liste.append(z_ivme)

    x_std_spm = round(stdev(x_ivme_liste), YUVARLA)
    y_std_spm = round(stdev(y_ivme_liste), YUVARLA)
    z_std_spm = round(stdev(z_ivme_liste), YUVARLA)

    r_ivme = round(sqrt((x_std_spm * x_std_spm) + (y_std_spm * y_std_spm) + (z_std_spm * z_std_spm)), YUVARLA)

    x_pga = PGA_FONK(x_ivme_liste)
    y_pga = PGA_FONK(y_ivme_liste)
    z_pga = PGA_FONK(z_ivme_liste)

    r_pga = sqrt((x_pga * x_pga) + (y_pga * y_pga) + (z_pga * z_pga))

    mmi_olcek = round((2.2 * log10(r_pga)) + 1, 1)

    FILTRE_YUZDE_DEGER = round((
        SINYAL_FILTRE(np.array(x_ivme_liste) - x_kal_deger, FILTRE_ESIK) +
        SINYAL_FILTRE(np.array(y_ivme_liste) - y_kal_deger, FILTRE_ESIK) +
        SINYAL_FILTRE(np.array(z_ivme_liste) - z_kal_deger, FILTRE_ESIK)
    ) / 3, 1)

    print("r_ivme:", r_ivme, "   FILTRE_YUZDE_DEGER:", FILTRE_YUZDE_DEGER)
    print()

    sismik_durum_dict = SISMIK_DURUM_DICT_FONK(r_ivme, FILTRE_YUZDE_DEGER, x_std_spm, y_std_spm, z_std_spm)

    ivme_veri_dict = {
        "x_ivme_liste": x_ivme_liste,
        "y_ivme_liste": y_ivme_liste,
        "z_ivme_liste": z_ivme_liste,

        "x_std_spm": x_std_spm,
        "y_std_spm": y_std_spm,
        "z_std_spm": z_std_spm,
        "r_ivme": r_ivme,

        "mmi_olcek": mmi_olcek,
        "sismik_durum_dict": sismik_durum_dict
    }

    return ivme_veri_dict


def SISMIK_DURUM_DICT_FONK(r_ivme, FILTRE_YUZDE_DEGER, x_std_spm, y_std_spm, z_std_spm):
    if (
        (DEPREM_ESIK > r_ivme > SISMIK_ESIK) and
        (FILTRE_YUZDE_DEGER > FILTRE_YUZDE_ESIK) and
        (x_std_spm != 0.1) and (y_std_spm != 0.1) and (z_std_spm != 0.1)
    ):
        SISMIK_ALARM = True
        DEPREM_ALARM = False
        print("r_ivme:", r_ivme, "   FILTRE_YUZDE_DEGER:", FILTRE_YUZDE_DEGER, "SISMIK_ALARM")
        print()

    elif (
        (r_ivme > DEPREM_ESIK) and
        (FILTRE_YUZDE_DEGER > FILTRE_YUZDE_ESIK) and
        (x_std_spm != 0.1) and (y_std_spm != 0.1) and (z_std_spm != 0.1)
        
    ):
        SISMIK_ALARM = True
        DEPREM_ALARM = True
        print("DEPREM_ALARM", FILTRE_YUZDE_DEGER)

    else:
        SISMIK_ALARM = False
        DEPREM_ALARM = False

    sismik_durum_dict = {
        "SISMIK_ALARM": SISMIK_ALARM,
        "DEPREM_ALARM": DEPREM_ALARM
    }
    return sismik_durum_dict


def kalibrasyon_oku():
    X_KALIBRE = 0
    Y_KALIBRE = 0
    Z_KALIBRE = 0

    ivme_dict = ivme_dict_fonk(
        ORNEK_SAYISI, X_KALIBRE, Y_KALIBRE, Z_KALIBRE, YUVARLA, SISMIK_ESIK, DEPREM_ESIK)

    x_ivme_liste = ivme_dict["x_ivme_liste"]
    y_ivme_liste = ivme_dict["y_ivme_liste"]
    z_ivme_liste = ivme_dict["z_ivme_liste"]

    x_liste_ort = round(sum(x_ivme_liste) / len(x_ivme_liste), YUVARLA)
    y_liste_ort = round(sum(y_ivme_liste) / len(y_ivme_liste), YUVARLA)
    z_liste_ort = round(sum(z_ivme_liste) / len(z_ivme_liste), YUVARLA)

    x_yeni_kal_deger = round(x_kal_deger - x_liste_ort, YUVARLA)
    y_yeni_kal_deger = round(y_kal_deger - y_liste_ort, YUVARLA)
    z_yeni_kal_deger = round(z_kal_deger - z_liste_ort, YUVARLA)

    return {
        "x_kal": x_yeni_kal_deger,
        "y_kal": y_yeni_kal_deger,
        "z_kal": z_yeni_kal_deger
    }


kalibre_dict = kalibrasyon_oku()

X_KALIBRE = kalibre_dict["x_kal"]
Y_KALIBRE = kalibre_dict["y_kal"]
Z_KALIBRE = kalibre_dict["z_kal"]
