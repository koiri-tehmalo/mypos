import configparser
from pywinauto.application import Application
import time
import os

# ชื่อไฟล์ Config
CONFIG_FILE = "config.ini"

def read_config(filename=CONFIG_FILE):
    """อ่านและโหลดค่าจากไฟล์ config.ini"""
    config = configparser.ConfigParser()
    try:
        # ตรวจสอบว่าไฟล์มีอยู่จริงหรือไม่
        if not os.path.exists(filename):
            # *** เพิ่มการแจ้งเตือนที่ชัดเจนเกี่ยวกับพาธที่กำลังค้นหา ***
            print(f"[X] FAILED: ไม่พบไฟล์ {filename} ที่พาธ: {os.path.abspath(filename)}")
            return configparser.ConfigParser()

        # ใช้ utf-8 สำหรับรองรับภาษาไทย
        config.read(filename, encoding='utf-8')
        return config
    except Exception as e:
        # แสดง Error ที่เกิดขึ้นจริง
        print(f"[X] FAILED: ไม่สามารถอ่านไฟล์ {filename} ได้: {e}")
        return configparser.ConfigParser()

# โหลด config ล่วงหน้า
CONFIG = read_config()
if not CONFIG.sections():
    print("ไม่สามารถโหลด config.ini ได้ โปรดตรวจสอบไฟล์และพาธ")
    exit()

# ดึงค่า Global ที่ใช้ร่วมกัน
WINDOW_TITLE = CONFIG['GLOBAL']['WINDOW_TITLE']
SLEEP_TIME = CONFIG.getint('GLOBAL', 'LOAD_TIME_SEC')
def payment2(config):
    print("Payment 2 executed")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    RS_CFG = config['RETAIL_SALES']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['CHECK_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        # กรอกข้อมูลเช็ค
        main_window.type_keys(f"{PM_CFG['NUMBER_P']}{{TAB}}")
        time.sleep(SLEEP_TIME)
        main_window.type_keys(f"{PM_CFG['NUMBER_C']}{{TAB}}")
        time.sleep(SLEEP_TIME)
        main_window.type_keys(f"{PM_CFG['DATE_C']}{{TAB}}")
        time.sleep(SLEEP_TIME)
        combobox_bank = main_window.child_window(title=PM_CFG['BANK_TITLE'], auto_id=PM_CFG['BANK_COMBO_AUTO_ID'], control_type="ComboBox")
        combobox_bank.expand()
        time.sleep(1) # รอ Dropdown กางออก
        bank_item = combobox_bank.child_window(title=PM_CFG['BANK_C'], control_type="Text")
        bank_item.click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 2: {e}")

if __name__ == "__main__":
    payment2(CONFIG)
