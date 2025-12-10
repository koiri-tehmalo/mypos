import configparser
from pywinauto.application import Application
import time
import os
from evidence import save_evidence  # นำเข้าฟังก์ชันบันทึกหลักฐาน

# ชื่อไฟล์ Config
CONFIG_FILE = "config.ini"

def read_config(filename=CONFIG_FILE):
    """อ่านและโหลดค่าจากไฟล์ config.ini"""
    config = configparser.ConfigParser()
    try:
        if not os.path.exists(filename):
            print(f"[X] ไม่พบไฟล์ config ที่: {os.path.abspath(filename)}")
            return configparser.ConfigParser()
            
        config.read(filename, encoding='utf-8')
        return config
    except Exception as e:
        print(f"[X] FAILED: ไม่สามารถอ่านไฟล์ {filename} ได้: {e}")
        return configparser.ConfigParser()

# โหลด Config
CONFIG = read_config()
if not CONFIG.sections():
    print("ไม่สามารถโหลด config.ini ได้ โปรดตรวจสอบไฟล์")
    exit()

# ค่า Global
WINDOW_TITLE = CONFIG['GLOBAL']['WINDOW_TITLE']
SLEEP_TIME = CONFIG.getint('GLOBAL', 'LOAD_TIME_SEC')

def test_return_product(config):
    """ทดสอบระบบ Return Product (คืนสินค้า)"""
    print("=" * 50)
    print("[*] เริ่มทดสอบ: Return Product (คืนสินค้า)")

    # ดึงค่า Config ของส่วนคืนสินค้ามาเก็บไว้ในตัวแปรสั้นๆ
    RET_CFG = config['RETURN_PRODUCT']
    GL_CFG = config['GLOBAL']
    # 1. เตรียมรายการสินค้าจาก Config
    raw_codes = RET_CFG.get('PRODUCT_CODES', '')
    if not raw_codes:
        # Fallback กรณีไม่ได้แก้ config ให้ใช้ค่าเดิมตัวเดียว
        raw_codes = RET_CFG.get('PRODUCT_CODE', '')
        
    product_list = [x.strip() for x in raw_codes.split(',') if x.strip()]
    
    print(f"[*] พบรายการสินค้าที่จะทดสอบ: {len(product_list)} รายการ -> {product_list}")
    try:
        # 1. เชื่อมต่อ App
        print("\n[*] กำลังเชื่อมต่อหน้าจอหลัก...")
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        print("[/] เชื่อมต่อหน้าจอขายสำเร็จ")
        
        for i, code in enumerate(product_list):
            print(f"\n[{i+1}/{len(product_list)}] กำลังเริ่มรายการสำหรับรหัส: {code}")
        # 2. กด E เพื่อเข้าหน้าคืนสินค้า
            main_window.child_window(title=RET_CFG['HOTKEY_E_TITLE'], 
                                 auto_id=RET_CFG['HOTKEY_E_AUTO_ID'], 
                                 control_type="Text").click_input()
            time.sleep(SLEEP_TIME)
            print("[/] เปิดหน้าคืนสินค้าสำเร็จ")

            # 3. พิมพ์รหัสสินค้า
            product_code = RET_CFG['PRODUCT_CODE']
            main_window.type_keys(f"{product_code}{{ENTER}}")
            time.sleep(SLEEP_TIME)

        # 4. กดปุ่ม 'คืนเงินได้'
            main_window.child_window(title=RET_CFG['REFUND_BUTTON_TITLE'], 
                                 auto_id=RET_CFG['REFUND_BUTTON_AUTO_ID'], 
                                 control_type="Text").click_input()
            time.sleep(SLEEP_TIME)

        # 5. เลือกสาเหตุการคืน (ComboBox)
            combo_reason = main_window.child_window(auto_id=RET_CFG['REASON_COMBO_AUTO_ID'], control_type="ComboBox")
            combo_reason.expand()
            time.sleep(1) # รอ Dropdown กางออก
        
        # เลือกเหตุผล: ซื้อสินค้าผิดรายการ
            item_reason = combo_reason.child_window(title=RET_CFG['REASON_ITEM_TITLE'], 
                                                auto_id=RET_CFG['REASON_ITEM_AUTO_ID'], 
                                                control_type="ListItem")
            item_reason.click_input()
            time.sleep(SLEEP_TIME)

        # 6. เลือกสภาพสินค้า (ComboBox)
            combo_condition = main_window.child_window(title=RET_CFG['CONDITION_COMBO_TITLE'], 
                                                   auto_id=RET_CFG['CONDITION_COMBO_AUTO_ID'], 
                                                   control_type="ComboBox")
            combo_condition.expand()
            time.sleep(SLEEP_TIME)

        # เลือกสภาพ: ขายได้
            item_condition = combo_condition.child_window(title=RET_CFG['CONDITION_ITEM_TITLE'], 
                                                      auto_id=RET_CFG['CONDITION_ITEM_AUTO_ID'], 
                                                      control_type="ListItem")
            item_condition.click_input()
        
        # กด Enter ยืนยัน ComboBox
            main_window.type_keys("{ENTER}") 
            time.sleep(SLEEP_TIME)

        # 7. กดปุ่ม Submit (Custom Control)
            main_window.child_window(auto_id=RET_CFG['SUBMIT_AUTO_ID'], 
                                 control_type="Custom").click_input()
            time.sleep(SLEEP_TIME)

        # 8. ขั้นตอนการจ่ายเงิน (Refund)
        # กด จ่ายเงิน
            main_window.child_window(title=RET_CFG['PAY_BUTTON_TITLE'], control_type="Text").click_input()
            time.sleep(0.5)
        # กด เงินสด
            main_window.child_window(title=RET_CFG['CASH_BUTTON_TITLE'], control_type="Text").click_input()
            time.sleep(SLEEP_TIME)

        # 9. ยืนยันและจบรายการ
        # กด ตกลง
            main_window.child_window(title=RET_CFG['CONFIRM_OK_TITLE'], 
                                 auto_id=RET_CFG['CONFIRM_OK_AUTO_ID'], 
                                 control_type="Text").click_input()
            time.sleep(SLEEP_TIME)
        
        # กด ถัดไป
            main_window.child_window(title=RET_CFG['NEXT_TITLE'], 
                                 auto_id=RET_CFG['NEXT_AUTO_ID'], 
                                 control_type="Text").click_input()
            time.sleep(SLEEP_TIME)

        # 10. ยกเลิกการพิมพ์ (ใช้ค่าจาก GLOBAL เพราะใช้บ่อย)
            main_window.child_window(title=GL_CFG['ABORT_PRINT_TITLE'], 
                                 auto_id=GL_CFG['ABORT_PRINT_AUTO_ID'], 
                                 control_type="Button").click_input()
        
        print("[V] จบการทดสอบ: Return Product สำเร็จ")

    except Exception as e:
        print(f"[X] Error during Return Product Test: {e}")
        save_evidence(app, "return_product_test")
if __name__ == "__main__":
    test_return_product(CONFIG)