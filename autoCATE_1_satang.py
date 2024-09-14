import pandas as pd

# อ่านไฟล์ Excel
file_path = 'laohuexample.xlsx'
data = pd.read_excel(file_path)

# ค้นหาคอลัมน์ที่มีชื่อ "รายการ"
column_name = None
for col in data.columns:
    if "รายการ" in col:
        column_name = col
        break

if column_name:
    # นำข้อมูลจากคอลัมน์ "รายการ" มาใช้
    ingredients = data[column_name]

    # แสดงตัวอย่างข้อมูลจากคอลัมน์ "รายการ"
    print("ข้อมูลจากคอลัมน์ 'รายการ':")
    print(ingredients.head(), "\n")

    # ฟังก์ชันจัดหมวดหมู่วัตถุดิบ
    def classify_ingredient(ingredient_name):
        # ตรวจสอบว่าค่า ingredient_name เป็นข้อความหรือไม่
        if isinstance(ingredient_name, str):
            beef_keywords = [
                                "เนื้อ", "ใบพาย", 
                                "ริบอาย", "น่องลาย", 
                                "สันนอก", "สะโพก", 
                                "เสือร้องไห้"
                             ]
            
            pork_keywords = [
                                "หมู", "สันคอ", "สันนอก", 
                                "สามชั้น", "หมูนุ่ม", "พริกไทยดำ", 
                                "หมักงา", "หมูซ่า", "หมูเด้ง", 
                                "สะโพก"
                            ]
            chicken_keywords = [
                                    "ไก่", "น่องไก่", "อกไก่",
                                    "ไก่นุ่ม", "ไก่ซ่า", "ไก่เด้ง",
                                ]

            if any(keyword in ingredient_name for keyword in beef_keywords):
                return "เนื้อวัว"
            elif any(keyword in ingredient_name for keyword in pork_keywords):
                return "เนื้อหมู"
            elif any(keyword in ingredient_name for keyword in chicken_keywords):
                return "เนื้อไก่"
            else:
                return "ไม่ทราบประเภท"
        else:
            # กรณีที่ไม่ใช่ข้อความ (เช่น NaN)
            return "ไม่ทราบประเภท"

    # จัดหมวดหมู่วัตถุดิบ
    data['ประเภทวัตถุดิบ'] = ingredients.apply(classify_ingredient)
    
    # แสดงข้อมูลที่ถูกจัดหมวดหมู่แล้ว
    print("ข้อมูลที่ถูกจัดหมวดหมู่แล้ว:")
    print(data[['รายการ', 'ประเภทวัตถุดิบ']].head())

else:
    print("ไม่พบคอลัมน์ที่ชื่อ 'รายการ'")
