# core/config_loader.py
# ใช้สำหรับโหลด config กลาง
import configparser
import os

CONFIG_FILE = "config.ini"


def load_config(filename: str = CONFIG_FILE) -> configparser.ConfigParser:
    """อ่าน config.ini และคืนค่าเป็น object config
    - แยกส่วนนี้ออกมาให้ชัด เพื่อให้ไฟล์อื่น import ใช้ได้ง่าย
    """
    config = configparser.ConfigParser()

    if not os.path.exists(filename):
        print(f"[X] FAILED: ไม่พบไฟล์ {filename} ที่พาธ: {os.path.abspath(filename)}")
        return config

    try:
        config.read(filename, encoding="utf-8")
        if not config.sections():
            print(f"[X] FAILED: ไฟล์ {filename} ไม่มี section ใด ๆ")
        return config
    except Exception as e:
        print(f"[X] FAILED: อ่านไฟล์ {filename} ไม่สำเร็จ: {e}")
        return config
