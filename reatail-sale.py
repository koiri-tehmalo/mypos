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

# ==============================================================================

def test_retail_sales_1(config):
    """ทดสอบการค้นหาสินค้าด้วยการพิมพ์ชื่อ"""
    print("=" * 50)
    print("[*] เริ่มทดสอบ Retail Sales: การค้นหาสินค้า")
    
    # ดึงค่าที่เกี่ยวข้องกับ Test 1
    RS_CFG = config['RETAIL_SALES']
    T1_CFG = config['TEST_1_SEARCH_BY_TEXT']
    
    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        print("[/] เชื่อมต่อหน้าจอขายสำเร็จ")
        
        # 1. R เปิดหน้าขายปลีก
        main_window.child_window(title=RS_CFG['HOTKEY_R_TITLE'], auto_id=RS_CFG['HOTKEY_R_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME) 
        print("[/] เปิดหน้าขายปลีกสำเร็จ")
        
        # 2. ค้นหาสินค้าด้วยชื่อ
        main_window.child_window(title=T1_CFG['SEARCH_TITLE'], auto_id=T1_CFG['SEARCH_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.type_keys(f"{T1_CFG['SEARCH_KEYWORD']}{{ENTER}}") 
        time.sleep(1)
        
        # 3. เลือกสินค้า
        main_window.child_window(title=RS_CFG['PRODUCT_DETAIL_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 4. ถัดไป (ยืนยันสินค้า)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 5. รับเงิน
        main_window.child_window(title=RS_CFG['RECEIVE_PAYMENT_TITLE'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 6. เลือกยอดเงินและยกเลิกการพิมพ์
        main_window.child_window(title=config['GLOBAL']['PAYMENT_AMOUNT'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()
        
        print("[V] จบการทดสอบ Retail Sales: การค้นหาสินค้าสำเร็จ")

    except Exception as e:
        print(f"[X] Error during Retail Sales Test 1: {e}")

# ------------------------------------------------------------------------------

def test_retail_sales_2(config):
    """ทดสอบการค้นหาสินค้าตามหมวดหมู่"""
    print("=" * 50)
    print("[*] เริ่มทดสอบ Retail Sales: ค้นหาสินค้าตามหมวดหมู่")
    
    # ดึงค่าที่เกี่ยวข้องกับ Test 2
    RS_CFG = config['RETAIL_SALES']
    T2_CFG = config['TEST_2_SEARCH_BY_CATEGORY']

    try:
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        print("[/] เชื่อมต่อหน้าจอขายสำเร็จ")
        
        # 1. R เปิดหน้าขายปลีก
        main_window.child_window(title=RS_CFG['HOTKEY_R_TITLE'], auto_id=RS_CFG['HOTKEY_R_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME) 
        print("[/] เปิดหน้าขายปลีกสำเร็จ")
        
        # 2. ค้นหาสินค้าตามหมวดหมู่
        main_window.child_window(title=T2_CFG['CATEGORY_SEARCH_TITLE'], auto_id=T2_CFG['CATEGORY_SEARCH_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 3. เลือกหมวดหมู่ 1
        main_window.child_window(title=T2_CFG['CATEGORY_1_TITLE'], auto_id=T2_CFG['CATEGORY_SEARCH_AUTO_ID'], control_type= "Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 4. เลือกหมวดหมู่ 2
        main_window.child_window(title=T2_CFG['CATEGORY_2_TITLE'], auto_id=T2_CFG['CATEGORY_SEARCH_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 5. เลือกสินค้า
        main_window.child_window(title=RS_CFG['PRODUCT_DETAIL_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 6. ดูรายละเอียด
        main_window.child_window(title=T2_CFG['DETAIL_BUTTON_TITLE'], auto_id=T2_CFG['DETAIL_BUTTON_AUTO_ID'], control_type="Button").click_input()
        time.sleep(SLEEP_TIME)
        
        # 7. ถัดไป (ยืนยันสินค้า)
        main_window.child_window(title=RS_CFG['NEXT_TITLE'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 8. รับเงิน
        main_window.child_window(title=RS_CFG['RECEIVE_PAYMENT_TITLE'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        
        # 9. เลือกยอดเงินและยกเลิกการพิมพ์
        main_window.child_window(title=config['GLOBAL']['PAYMENT_AMOUNT'], auto_id=RS_CFG['NEXT_AUTO_ID'], control_type="Text").click_input()
        time.sleep(SLEEP_TIME)
        main_window.child_window(title=config['GLOBAL']['ABORT_PRINT_TITLE'], auto_id=config['GLOBAL']['ABORT_PRINT_AUTO_ID'], control_type="Button").click_input()
        
        print("[V] จบการทดสอบ Retail Sales: ค้นหาสินค้าตามหมวดหมู่สำเร็จ")

    except Exception as e:
        print(f"[X] Error during Retail Sales Test 2: {e}")

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # ส่ง CONFIG Object เข้าไปในทุกฟังก์ชันที่ต้องการใช้ค่า Dynamic
    test_retail_sales_1(CONFIG)
    test_retail_sales_2(CONFIG)