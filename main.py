# main.py
from core.config_loader import load_config
from core.app_context import AppContext
from flows.retail_flow import RetailFlow
from flows.payment_flow import PaymentFlow
from flows.return_flow import ReturnFlow


def main():
    # 1) โหลด config
    config = load_config()
    if not config.sections():
        print("[X] Config โหลดไม่สำเร็จ ยุติการทำงาน")
        return

    # 2) สร้าง AppContext (ใช้ WINDOW_TITLE จาก config)
    window_title_regex = config["GLOBAL"]["WINDOW_TITLE"]
    ctx = AppContext(window_title_regex=window_title_regex)

    # 3) สร้าง Flow ต่างๆ
    retail = RetailFlow(config, ctx)
    payment = PaymentFlow(config, ctx)
    ret = ReturnFlow(config, ctx)

    # 4) เรียก Scenario ที่ต้องการทดสอบ (ปรับได้ตามใจ)
    # ตัวอย่าง: ขายแบบค้นหาชื่อ → จ่ายเงินสด → ขายแบบหมวดหมู่ → จ่ายเงินสด → คืนสินค้า
    retail.search_by_text_and_go_payment()
    payment.pay_cash()

    retail.search_by_category_and_go_payment()
    payment.pay_cash()

    # ทดลอง flow อื่นๆ:
    # payment.pay_exact()
    # payment.pay_qr()
    # payment.pay_cheque()
    # ...

    # ทดสอบ Return Product
    ret.process_all()


if __name__ == "__main__":
    main()
