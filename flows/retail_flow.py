# flows/retail_flow.py
import time
from configparser import ConfigParser
from core.app_context import AppContext
from core.ui_helper import click, type_keys, run_step


class RetailFlow:
    """Flow เกี่ยวกับการขายปลีก (Retail Sales)"""

    def __init__(self, config: ConfigParser, ctx: AppContext):
        self.config = config
        self.ctx = ctx
        self.RS_CFG = config["RETAIL_SALES"]
        self.T1_CFG = config["TEST_1_SEARCH_BY_TEXT"]
        self.T2_CFG = config["TEST_2_SEARCH_BY_CATEGORY"]
        self.SLEEP_TIME = config.getint("GLOBAL", "LOAD_TIME_SEC")

    # --------- Flow 1: ค้นหาสินค้าด้วยการพิมพ์ชื่อ ---------
    def search_by_text_and_go_payment(self):
        app, win = self.ctx.connect()

        def _inner():
            # 1) เปิดหน้าขายปลีก (R)
            click(
                win,
                title=self.RS_CFG["HOTKEY_R_TITLE"],
                auto_id=self.RS_CFG["HOTKEY_R_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 2) คลิกช่อง "ค้นหาสินค้า" แล้วพิมพ์คำค้น
            click(
                win,
                title=self.T1_CFG["SEARCH_TITLE"],
                auto_id=self.T1_CFG["SEARCH_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)
            type_keys(win, f"{self.T1_CFG['SEARCH_KEYWORD']}{{ENTER}}")
            time.sleep(1)

            # 3) เลือกสินค้า
            try:
                click(
                win,
                title=self.RS_CFG["PRODUCT_DETAIL_TITLE"],
                auto_id=self.RS_CFG["NEXT_AUTO_ID"],
            )
            except Exception:
                print(f"[!] ไม่มี {self.RS_CFG['PRODUCT_DETAIL_TITLE']} ให้เลือก")
                raise Exception(f"ไม่มี {self.RS_CFG['PRODUCT_DETAIL_TITLE']} ให้เลือก")  
            time.sleep(self.SLEEP_TIME)

            # 4) ถัดไป
            click(
                win,
                title=self.RS_CFG["NEXT_TITLE"],
                auto_id=self.RS_CFG["NEXT_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 5) รับเงิน
            click(win, title=self.RS_CFG["RECEIVE_PAYMENT_TITLE"])
            time.sleep(self.SLEEP_TIME)

        run_step(app, "retail_search_by_text", _inner)

    # --------- Flow 2: ค้นหาสินค้าตามหมวดหมู่ ---------
    def search_by_category_and_go_payment(self):
        app, win = self.ctx.connect()

        def _inner():
            # 1) เปิดหน้าขายปลีก (R)
            click(
                win,
                title=self.RS_CFG["HOTKEY_R_TITLE"],
                auto_id=self.RS_CFG["HOTKEY_R_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 2) คลิก "ค้นหาสินค้าตามหมวดหมู่"
            click(
                win,
                title=self.T2_CFG["CATEGORY_SEARCH_TITLE"],
                auto_id=self.T2_CFG["CATEGORY_SEARCH_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 3) เลือกหมวดหมู่ 1
            try:
                click(
                win,
                title=self.T2_CFG["CATEGORY_1_TITLE"],
                auto_id=self.T2_CFG["CATEGORY_SEARCH_AUTO_ID"],
            )
            except Exception:
                print(f"[!] ไม่มี {self.T2_CFG['CATEGORY_1_TITLE']} ให้เลือก")
                raise Exception(f"ไม่มี {self.T2_CFG['CATEGORY_1_TITLE']} ให้เลือก")  
            time.sleep(self.SLEEP_TIME)

            # 4) เลือกหมวดหมู่ 2
            click(
                win,
                title=self.T2_CFG["CATEGORY_2_TITLE"],
                auto_id=self.T2_CFG["CATEGORY_SEARCH_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 5) เลือกสินค้า
            click(
                win,
                title=self.RS_CFG["PRODUCT_DETAIL_TITLE"],
                auto_id=self.RS_CFG["NEXT_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 6) ดูรายละเอียด
            click(
                win,
                title=self.T2_CFG["DETAIL_BUTTON_TITLE"],
                auto_id=self.T2_CFG["DETAIL_BUTTON_AUTO_ID"],
                control_type="Button",
            )
            time.sleep(self.SLEEP_TIME)

            # 7) ถัดไป
            click(
                win,
                title=self.RS_CFG["NEXT_TITLE"],
                auto_id=self.RS_CFG["NEXT_AUTO_ID"],
            )
            time.sleep(self.SLEEP_TIME)

            # 8) รับเงิน
            click(win, title=self.RS_CFG["RECEIVE_PAYMENT_TITLE"])
            time.sleep(self.SLEEP_TIME)

        run_step(app, "retail_search_by_category", _inner)
