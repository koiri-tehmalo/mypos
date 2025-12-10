# flows/return_flow.py
import time
from configparser import ConfigParser
from core.app_context import AppContext
from core.ui_helper import click, select_combobox_item, type_keys, run_step
from evidence import save_evidence  # เผื่อใช้ในระดับ flow


class ReturnFlow:
    """Flow เกี่ยวกับคืนสินค้า (Return Product)"""

    def __init__(self, config: ConfigParser, ctx: AppContext):
        self.config = config
        self.ctx = ctx
        self.RET = config["RETURN_PRODUCT"]
        self.GL = config["GLOBAL"]
        self.SLEEP = config.getint("GLOBAL", "LOAD_TIME_SEC")

        raw_codes = self.RET.get("PRODUCT_CODES", "")
        if not raw_codes:
            raw_codes = self.RET.get("PRODUCT_CODE", "")
        self.product_list = [x.strip() for x in raw_codes.split(",") if x.strip()]

    def process_all(self):
        app, win = self.ctx.connect()

        def _inner():
            print(f"[*] พบสินค้าสำหรับคืน: {len(self.product_list)} รายการ -> {self.product_list}")

            for idx, code in enumerate(self.product_list, start=1):
                print(f"\n[{idx}/{len(self.product_list)}] เริ่มคืนสินค้า รหัส: {code}")

                # เข้าหน้าคืนสินค้า (E)
                click(
                    win,
                    title=self.RET["HOTKEY_E_TITLE"],
                    auto_id=self.RET["HOTKEY_E_AUTO_ID"],
                )
                time.sleep(self.SLEEP)

                # พิมพ์รหัสสินค้า
                type_keys(win, f"{code}{{ENTER}}", sleep=self.SLEEP)

                # ปุ่ม "คืนเงินได้"
                click(
                    win,
                    title=self.RET["REFUND_BUTTON_TITLE"],
                    auto_id=self.RET["REFUND_BUTTON_AUTO_ID"],
                )
                time.sleep(self.SLEEP)

                # เลือกสาเหตุการคืน
                select_combobox_item(
                    win,
                    combo_auto_id=self.RET["REASON_COMBO_AUTO_ID"],
                    item_title=self.RET["REASON_ITEM_TITLE"],
                    sleep=self.SLEEP,
                )

                # เลือกสภาพสินค้า
                select_combobox_item(
                    win,
                    combo_auto_id=self.RET["CONDITION_COMBO_AUTO_ID"],
                    item_title=self.RET["CONDITION_ITEM_TITLE"],
                    sleep=self.SLEEP,
                )

                # กด Enter ยืนยัน
                type_keys(win, "{ENTER}", sleep=self.SLEEP)

                # Submit
                click(
                    win,
                    auto_id=self.RET["SUBMIT_AUTO_ID"],
                    control_type="Custom",
                )
                time.sleep(self.SLEEP)

                # จ่ายเงินคืน
                click(win, title=self.RET["PAY_BUTTON_TITLE"])
                time.sleep(0.5)
                click(win, title=self.RET["CASH_BUTTON_TITLE"])
                time.sleep(self.SLEEP)

                # กด ตกลง
                click(
                    win,
                    title=self.RET["CONFIRM_OK_TITLE"],
                    auto_id=self.RET["CONFIRM_OK_AUTO_ID"],
                )
                time.sleep(self.SLEEP)

                # ถัดไป
                click(
                    win,
                    title=self.RET["NEXT_TITLE"],
                    auto_id=self.RET["NEXT_AUTO_ID"],
                )
                time.sleep(self.SLEEP)

                # ยกเลิกการพิมพ์
                click(
                    win,
                    title=self.GL["ABORT_PRINT_TITLE"],
                    auto_id=self.GL["ABORT_PRINT_AUTO_ID"],
                    control_type="Button",
                )

            print("[V] จบการทดสอบคืนสินค้า (Return Product) สำหรับทุกรายการ")

        run_step(app, "return_all_products", _inner)
