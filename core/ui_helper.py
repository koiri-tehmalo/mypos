# core/ui_helper.py
# รวม helper ที่ใช้บ่อย: click / type / wait / combo
import time
from typing import Optional, Any, Dict
from pywinauto.base_wrapper import BaseWrapper
from evidence import save_evidence  # ใช้ของคุณเดิม


def _find_element(win: BaseWrapper, **kwargs) -> BaseWrapper:
    """wrapper หา element เดียวให้ทุกฟังก์ชันใช้ร่วมกัน"""
    return win.child_window(**kwargs)


def click(
    win: BaseWrapper,
    title: Optional[str] = None,
    auto_id: Optional[str] = None,
    control_type: str = "Text",
    sleep: float = 0.5,
) -> None:
    """คลิก element ตาม title/auto_id"""
    elem_kwargs: Dict[str, Any] = {"control_type": control_type}
    if title is not None:
        elem_kwargs["title"] = title
    if auto_id is not None:
        elem_kwargs["auto_id"] = auto_id

    element = _find_element(win, **elem_kwargs)
    element.click_input()
    time.sleep(sleep)


def type_keys(win: BaseWrapper, text: str, sleep: float = 0.5) -> None:
    """พิมพ์ข้อความลง active control"""
    win.type_keys(text)
    time.sleep(sleep)


def wait_and_click(
    win: BaseWrapper,
    timeout: float = 5.0,
    retry_interval: float = 0.2,
    title: Optional[str] = None,
    auto_id: Optional[str] = None,
    control_type: str = "Text",
) -> None:
    """รอ element จนกว่าจะหาเจอแล้วค่อย click (เพิ่มความเสถียรของ test)"""
    start = time.time()
    last_error: Optional[Exception] = None

    while time.time() - start < timeout:
        try:
            click(
                win,
                title=title,
                auto_id=auto_id,
                control_type=control_type,
                sleep=0.2,
            )
            return
        except Exception as e:  # noqa
            last_error = e
            time.sleep(retry_interval)

    raise TimeoutError(f"ไม่พบ element: title={title}, auto_id={auto_id}, last_error={last_error}")


def select_combobox_item(
    win: BaseWrapper,
    combo_auto_id: str,
    item_title: str,
    sleep: float = 0.5,
) -> None:
    """เลือก item จาก ComboBox โดยใช้ auto_id ของ ComboBox + title ของ item"""
    combo = win.child_window(auto_id=combo_auto_id, control_type="ComboBox")
    combo.expand()
    time.sleep(0.5)
    item = combo.child_window(title=item_title, control_type="ListItem")
    item.click_input()
    time.sleep(sleep)


def run_step(app, step_name: str, func, *args, **kwargs):
    """Wrapper สำหรับรัน 1 step
    - ถ้า error → เซฟ evidence ให้โดยอัตโนมัติ
    - คืนค่า return ของฟังก์ชัน ถ้าสำเร็จ
    """
    print(f"[*] เริ่ม Step: {step_name}")
    try:
        result = func(*args, **kwargs)
        print(f"[V] Step '{step_name}' สำเร็จ")
        return result
    except Exception as e:
        print(f"[X] Step '{step_name}' ล้มเหลว: {e}")
        save_evidence(app, step_name)
        # จะ raise ต่อหรือไม่แล้วแต่ design
        raise
