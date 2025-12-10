import os
import datetime  # เพิ่ม module สำหรับจัดการเวลา เพื่อสร้างชื่อไฟล์ไม่ซ้ำ
def save_evidence(app, test_name):
    """ฟังก์ชันช่วยบันทึกหน้าจอเมื่อเกิด Error"""
    # 1. สร้างโฟลเดอร์เก็บหลักฐานถ้ายังไม่มี
    evidence_dir = "evidence"
    if not os.path.exists(evidence_dir):
        os.makedirs(evidence_dir)

    # 2. สร้างชื่อไฟล์ตามเวลา (Timestamp)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{evidence_dir}/FAIL_{test_name}_{timestamp}.png"

    try:
        if app and app.top_window().exists():
            # 3. สั่ง Capture หน้าต่างโปรแกรม
            app.top_window().capture_as_image().save(filename)
            print(f"\n[!!] หลักฐาน (Evidence) ถูกบันทึกแล้วที่: {filename}")
            print(f"[!!] สาเหตุที่ไม่ผ่าน: ดูภาพ {filename} เพื่อตรวจสอบ Error บนหน้าจอ")
        else:
            # กรณีเชื่อมต่อ App ไม่ได้ ให้ Capture ทั้งหน้าจอ Desktop แทน (เผื่อ App หลุด)
            from PIL import ImageGrab
            ImageGrab.grab().save(filename)
            print(f"\n[!!] App ไม่ตอบสนอง บันทึกภาพ Desktop แทนที่: {filename}")
            
    except Exception as e:
        print(f"[!!] ไม่สามารถบันทึกหลักฐานได้: {e}")