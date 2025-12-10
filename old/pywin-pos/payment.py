import time
import configparser
from pywinauto.application import Application
from evidence import save_evidence  # อย่าลืม import ฟังก์ชันเก็บหลักฐานเข้ามาด้วย
import os
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


WINDOW_TITLE = CONFIG['GLOBAL']['WINDOW_TITLE']
SLEEP_TIME = CONFIG.getint('GLOBAL', 'LOAD_TIME_SEC')
# -----------------------------------------------------------------------------------------------------------------------------
#ทำได้แล้ว
def payment1(config):
    print("ชำระด้วย เงินสด")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    RS_CFG = config['RETAIL_SALES']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['CASH_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.type_keys(f"{PM_CFG['CASH_AMOUNT']}{{ENTER}}")
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()
        
    except Exception as e:
        print(f"[X] Error during Payment 1: {e}")
        save_evidence(app, "payment_1")
#ทำได้แล้ว

def payment2(config):
    print("ชำระด้วย เงินพอดี")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['PAYMENT_FAST'], auto_id=PM_CFG['HOTKEY_F_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 2: {e}")
        save_evidence(app, "payment_2")
#ยังทำไม่ได้
def payment3(config):
    print("Payment 5 executed")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    RS_CFG = config['RETAIL_SALES']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['QR_CODE_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()
    except Exception as e:
        print(f"[X] Error during Payment 3: {e}")
        save_evidence(app, "payment_3")
#ทำได้แล้ว
def payment4(config):
    print("ชำระด้วย เช็ด")
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
        print(f"[X] Error during Payment 4: {e}")
        save_evidence(app, "payment_4")
#ยังทำไม่ได้
def payment5(config):
    print("ชำระด้วย บัตรเครดิต")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    RS_CFG = config['RETAIL_SALES']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['CREDIT_CARD_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.type_keys(f"{PM_CFG['CREDIT_CARD_AMOUNT']}{{ENTER}}")
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 5: {e}")
        save_evidence(app, "payment_5")
#ยังทำไม่ได้
def payment6(config):
    print("ชำระด้วย บัตรเดบิต")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    RS_CFG = config['RETAIL_SALES']

    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['DEBIT_CARD_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 6: {e}")
        save_evidence(app, "payment_6")
#ยังทำไม่ได้
def payment7(config):
    print("ชำระด้วย อาลีเพย์")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['ALIPYAY_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 7: {e}")
#ยังทำไม่ได้
def payment8(config):
    print("ชำระด้วย วีแชท")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['WECHAT_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 8: {e}")
        save_evidence(app, "payment_8")
#ยังทำไม่ได้
def payment9(config):
    print("ชำระด้วย กระเป๋าตสตางค์@ไปรษณีย์")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['THP_PEYMENT_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 9: {e}")
        save_evidence(app, "payment_9")

#ยังทำไม่ได้
def payment10(config):
    print("ชำระด้วย คิวอาร์ เครดิต")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['QR_CREDIT_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 10: {e}")
        save_evidence(app, "payment_10")    
#ยังทำไม่ได้
def payment11(config):
    print("ชำระด้วย กระเป๋าตสตางค์ทรูมันนี่")
    # ดึงค่าที่เกี่ยวข้องกับ Payment
    PM_CFG = CONFIG['PAYMENT']
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.child_window(title=PM_CFG['TRUEMANEY_TITLE'], auto_id=PM_CFG['PAYMENT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()

    except Exception as e:
        print(f"[X] Error during Payment 11: {e}")
        save_evidence(app, "payment_11")