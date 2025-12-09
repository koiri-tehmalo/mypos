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
def payment1():
    print("Payment 1 executed")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT_AMOUNT']

    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['CASH_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
    except Exception as e:
        print(f"[X] Error during Payment 1: {e}")

if __name__ == "__main__":
    payment1()