import board
from busio import I2C
from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction
from time import sleep

i2c = I2C(board.SCL, board.SDA)
sleep(0.1)

ROLE_MCP = MCP23017(i2c, 0x20)
SENSOR_MCP = MCP23017(i2c, 0x21)

# ------------------------------ ROLE_MCP ------------------------------
id_220_role_1_pin = ROLE_MCP.get_pin(0)
id_220_role_2_pin = ROLE_MCP.get_pin(1)
id_220_role_3_pin = ROLE_MCP.get_pin(2)
id_220_role_4_pin = ROLE_MCP.get_pin(3)
id_kontak_role_1_pin = ROLE_MCP.get_pin(4)
id_kontak_role_2_pin = ROLE_MCP.get_pin(5)
id_kontak_role_3_pin = ROLE_MCP.get_pin(6)
id_kontak_role_4_pin = ROLE_MCP.get_pin(7)
id_12_role_1_pin = ROLE_MCP.get_pin(8)
id_12_role_2_pin = ROLE_MCP.get_pin(9)
id_12_role_3_pin = ROLE_MCP.get_pin(10)
id_12_role_4_pin = ROLE_MCP.get_pin(11)
sistem_led_pin = ROLE_MCP.get_pin(12)
alarm_led_pin = ROLE_MCP.get_pin(13)
buzzer_out_pin = ROLE_MCP.get_pin(14)


id_220_role_1_pin.direction = Direction.OUTPUT
id_220_role_2_pin.direction = Direction.OUTPUT
id_220_role_3_pin.direction = Direction.OUTPUT
id_220_role_4_pin.direction = Direction.OUTPUT
id_12_role_1_pin.direction = Direction.OUTPUT
id_12_role_2_pin.direction = Direction.OUTPUT
id_12_role_3_pin.direction = Direction.OUTPUT
id_12_role_4_pin.direction = Direction.OUTPUT
id_kontak_role_1_pin.direction = Direction.OUTPUT
id_kontak_role_2_pin.direction = Direction.OUTPUT
id_kontak_role_3_pin.direction = Direction.OUTPUT
id_kontak_role_4_pin.direction = Direction.OUTPUT
# ------------------------------ ROLE_MCP ------------------------------

# ------------------------------ SENSOR_MCP ------------------------------
id_12_sensor_1_pin = SENSOR_MCP.get_pin(0)
id_12_sensor_2_pin = SENSOR_MCP.get_pin(1)
id_12_sensor_3_pin = SENSOR_MCP.get_pin(2)
id_12_sensor_4_pin = SENSOR_MCP.get_pin(3)
id_220_sensor_1_pin = SENSOR_MCP.get_pin(4)
id_220_sensor_2_pin = SENSOR_MCP.get_pin(5)
id_220_sensor_3_pin = SENSOR_MCP.get_pin(6)
id_220_sensor_4_pin = SENSOR_MCP.get_pin(7)

id_12_sensor_1_pin.direction = Direction.INPUT
id_12_sensor_2_pin.direction = Direction.INPUT
id_12_sensor_3_pin.direction = Direction.INPUT
id_12_sensor_4_pin.direction = Direction.INPUT
id_220_sensor_1_pin.direction = Direction.INPUT
id_220_sensor_2_pin.direction = Direction.INPUT
id_220_sensor_3_pin.direction = Direction.INPUT
id_220_sensor_4_pin.direction = Direction.INPUT
# ------------------------------ SENSOR_MCP ------------------------------

# ------------------------------ LED_BUZZER_MCP ------------------------------


sistem_led_pin.direction = Direction.OUTPUT
buzzer_out_pin.direction = Direction.OUTPUT
alarm_led_pin.direction = Direction.OUTPUT
# ------------------------------ LED_BUZZER_MCP ------------------------------


def durum_text(bool_veri):
    if bool_veri == True:
        DURUM = "AKTIF"
    else:
        DURUM = "DEAKTIF"
    return DURUM


def ROLERI_HIGH_YAP_FONK():
    id_220_role_1_pin.value = True
    id_220_role_2_pin.value = True
    id_220_role_3_pin.value = True
    id_220_role_4_pin.value = True
    id_12_role_1_pin.value = True
    id_12_role_2_pin.value = True
    id_12_role_3_pin.value = True
    id_12_role_4_pin.value = True
    id_kontak_role_1_pin.value = True
    id_kontak_role_2_pin.value = True
    id_kontak_role_3_pin.value = True
    id_kontak_role_4_pin.value = True

    role_dict = {
        "id_12_r_1": "AKTIF",
        "id_12_r_2": "AKTIF",
        "id_12_r_3": "AKTIF",
        "id_12_r_4": "AKTIF",
        "id_220_r_1": "AKTIF",
        "id_220_r_2": "AKTIF",
        "id_220_r_3": "AKTIF",
        "id_220_r_4": "AKTIF",
        "id_kk_r_1": "AKTIF",
        "id_kk_r_2": "AKTIF",
        "id_kk_r_3": "AKTIF",
        "id_kk_r_4": "AKTIF",
        "buzzer_pin": "AKTIF"
    }
    return role_dict


def ROLERI_LOW_YAP_FONK():
    id_220_role_1_pin.value = False
    id_220_role_2_pin.value = False
    id_220_role_3_pin.value = False
    id_220_role_4_pin.value = False
    id_12_role_1_pin.value = False
    id_12_role_2_pin.value = False
    id_12_role_3_pin.value = False
    id_12_role_4_pin.value = False
    id_kontak_role_1_pin.value = False
    id_kontak_role_2_pin.value = False
    id_kontak_role_3_pin.value = False
    id_kontak_role_4_pin.value = False

    role_dict = {
        "id_12_r_1": "DEAKTIF",
        "id_12_r_2": "DEAKTIF",
        "id_12_r_3": "DEAKTIF",
        "id_12_r_4": "DEAKTIF",
        "id_220_r_1": "DEAKTIF",
        "id_220_r_2": "DEAKTIF",
        "id_220_r_3": "DEAKTIF",
        "id_220_r_4": "DEAKTIF",
        "id_kk_r_1": "DEAKTIF",
        "id_kk_r_2": "DEAKTIF",
        "id_kk_r_3": "DEAKTIF",
        "id_kk_r_4": "DEAKTIF",
        "buzzer_pin": "DEAKTIF"
    }
    return role_dict


def SENSOR_OKU_FONK():
    sensor_alarm_liste = []

    # id_12_s_1_durum = durum_text(id_12_sensor_1_pin.value)
    # id_12_s_2_durum = durum_text(id_12_sensor_2_pin.value)
    # id_12_s_3_durum = durum_text(id_12_sensor_3_pin.value)
    # id_12_s_4_durum = durum_text(id_12_sensor_4_pin.value)

    # id_220_s_1_durum = durum_text(id_220_sensor_1_pin.value)
    # id_220_s_2_durum = durum_text(id_220_sensor_2_pin.value)
    # id_220_s_3_durum = durum_text(id_220_sensor_3_pin.value)
    # id_220_s_4_durum = durum_text(id_220_sensor_4_pin.value)
    # sensor_dict = {
    #     "id_12_s_1": id_12_s_1_durum,
    #     "id_12_s_2": id_12_s_2_durum,
    #     "id_12_s_3": id_12_s_3_durum,
    #     "id_12_s_4": id_12_s_4_durum,
    #     "id_220_s_1": id_220_s_1_durum,
    #     "id_220_s_2": id_220_s_2_durum,
    #     "id_220_s_3": id_220_s_3_durum,
    #     "id_220_s_4": id_220_s_4_durum
    # }
    sensor_dict = {
        "id_12_s_1": "DEAKTIF",
        "id_12_s_2": "DEAKTIF",
        "id_12_s_3": "DEAKTIF",
        "id_12_s_4": "DEAKTIF",
        "id_220_s_1": "DEAKTIF",
        "id_220_s_2": "DEAKTIF",
        "id_220_s_3": "DEAKTIF",
        "id_220_s_4": "DEAKTIF"
    }
    for sensor_isim, sensor_alam_durum in sensor_dict.items():
        if sensor_alam_durum == "AKTIF":
            sensor_alarm_liste.append(sensor_isim)
    if len(sensor_alarm_liste) > 0:
        sensor_alarm = True
    else:
        sensor_alarm = False
    sensor_dict["SENSOR_ALARM"] = sensor_alarm
    return sensor_dict


def LED_BUZZER_NORMAL_DURUM():
    sistem_led_pin.value = True
    buzzer_out_pin.value = False
    alarm_led_pin.value = False


def LED_BUZZER_ALARM_DURUM():
    sistem_led_pin.value = False
    buzzer_out_pin.value = True
    alarm_led_pin.value = True


def LED_BUZZER_TEST_DURUM():
    sistem_led_pin.value = True
    buzzer_out_pin.value = True
    alarm_led_pin.value = True


def ROLE_DURUM_OKU_FONK():
    role_dict = {
        "id_12_r_1": id_12_role_1_pin.value,
        "id_12_r_2": id_12_role_2_pin.value,
        "id_12_r_3": id_12_role_3_pin.value,
        "id_12_r_4": id_12_role_4_pin.value,

        "id_220_r_1": id_220_role_1_pin.value,
        "id_220_r_2": id_220_role_2_pin.value,
        "id_220_r_3": id_220_role_3_pin.value,
        "id_220_r_4": id_220_role_4_pin.value,

        "id_kk_r_1": id_kontak_role_1_pin.value,
        "id_kk_r_2": id_kontak_role_2_pin.value,
        "id_kk_r_3": id_kontak_role_3_pin.value,
        "id_kk_r_4": id_kontak_role_4_pin.value
    }
    return role_dict


def LED_BUZZER_OKU_FONK():
    led_buzzer_dict = {
        "sistem_led_pin": sistem_led_pin.value,
        "buzzer_out_pin": buzzer_out_pin.value,
        "alarm_led_pin": alarm_led_pin.value
    }
    return led_buzzer_dict

