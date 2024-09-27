import pandas as pd
import sys
from pythainlp.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

sys.stdout.reconfigure(encoding='utf-8')

# โหลดข้อมูลจากไฟล์ CSV
data = pd.read_csv('Dataset_train - Sheet1.csv')

# ตัดคำภาษาไทย
data['food_item'] = data['food_item'].apply(lambda x: ' '.join(word_tokenize(x, engine='newmm')))

# แยก features (ชื่ออาหาร) และ labels (หมวดหมู่)
X = data['food_item']
y = data['category']

# แปลงข้อความเป็นตัวเลข (Bag of Words)
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# แบ่งข้อมูลเป็นชุดฝึกและชุดทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# สร้างโมเดล RandomForest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# ทำนายผลการทดสอบและวัดความแม่นยำ
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# ทดสอบการจำแนกข้อมูลใหม่
new_food = ['ไข่','เนื้อริบอาย', 'เนื้อใบพาย', 'เนื้อน่องลาย', 'เนื้อสักนอก', 'เนื้อสะโพก', 'เนื้อเสือร้องไห้', 'เนื้อ', 'เนื้อวัว', 'ริบอาย', 'ใบพาย', 'น่องลาย', 'เสือร้องไห้', 'ริบอายเนื้อ', 'อายริบเนื้อ', 'เนื้ออายริบ', 'อายเนื้อริบ', 'เนื้อใบพาย', 'พายใบเนื้อ', 'ใบพายเนื้อ', 'พายเนื้อใบ', 'ใบเนื้อพาย', 'เนื้อพายใบ', 'หมูสามชั้น', 'สามชั้นหมู', 'สันนอกหมู', 'หมูสันคอ', 'หมูนุ่ม', 'หมูพริกไทยดำ', 'หมูหมักงา', 'หมูซ่า', 'หมูเด้ง', 'สะโพกหมู', 'หมู', 'หมูสันนอก', 'สันคอหมู', 'สามชั้น', 'สันคอหมู', 'สันหมูคอ', 'หมูคอสัน', 'หมูสันคอ', 'คอหมูสัน', 'คอสันหมู', 'สันคอหมูสไลด์', 'สันหมูคอสไลด์', 'หมูคอสันสไลด์', 'หมูสันคอสไลด์', 'คอหมูสันสไลด์', 'คอสันหมูสไลด์', 'สไลด์หมูสันคอ', 'สไลด์สันหมูคอ', 'สไลด์คอสันหมู', 'สไลด์คอหมูสัน', 'สันนอกหมู', 'สันหมูนอก', 'หมูนอกสัน', 'หมูสันนอก', 'นอกหมูสัน', 'นอกสันหมู', 'สันนอกหมูสไลด์', 'สันหมูนอกสไลด์', 'หมูนอกสันสไลด์', 'หมูสันนอกสไลด์', 'นอกหมูสันสไลด์', 'นอกสันหมูสไลด์', 'สไลด์หมูสันนอก', 'สไลด์สันหมูนอก', 'สไลด์นอกสันหมู', 'สไลด์นอกหมูสัน', 'หมูหมักงา', 'หมูงาหมัก', 'หมักหมูงา', 'หมักงาหมู', 'งาหมักหมู', 'งาหมูหมัก', 'หมูพริกไทดำ', 'หมูพริกดำไท', 'หมูไทดำพริก', 'หมูไทพริกดำ', 'หมูดำไทพริก', 'หมูดำพริกไท', 'พริกหมูไทดำ', 'พริกหมูดำไท', 'พริกไทหมูดำ', 'พริกไทดำหมู', 'พริกดำไทหมู', 'พริกดำหมูไท', 'หมูพริกไทยดำ', 'หมูพริกดำไทย', 'หมูไทยดำพริก', 'หมูไทยพริกดำ', 'หมูดำไทยพริก', 'หมูดำพริกไทย', 'พริกหมูไทยดำ', 'พริกหมูดำไทย', 'พริกไทยหมูดำ', 'พริกไทยดำหมู', 'พริกดำไทยหมู', 'พริกดำหมูไทย', 'สามชั้นหมูสไลด์', 'สามหมูชั้นสไลด์', 'หมูชั้นสามสไลด์', 'หมูสามชั้นสไลด์', 'ชั้นหมูสามสไลด์', 'ชั้นสามหมูสไลด์', 'สไลด์หมูสามชั้น', 'สไลด์สามหมูชั้น', 'สไลด์ชั้นสามหมู', 'สไลด์ชั้นหมูสาม', 'สามชั้นหมักงา', 'สามหมูชั้นหมักงา', 'หมูชั้นสามหมักงา', 'หมูสามชั้นหมักงา', 'ชั้นหมูสามหมักงา', 'ชั้นสามหมูหมักงา', 'หมักงาหมูสามชั้น', 'หมักงาสามหมูชั้น', 'หมักงาชั้นสามหมู', 'หมักงาชั้นหมูสาม', 'หมูเด้ง', 'เด้งหมู', 'ตับสไลด์', 'สไลด์ตับ', 'เนื้อไก่', 'ไก่นุ่ม', 'ไก่ซ่า', 'ไก่เด้ง', 'เนื้อไก่', 'ไก่', 'น่องไก่', 'สะโพกไก่', 'โครงไก่', 'ปีกไก่', 'เนื้อไก่', 'อกไก่', 'อกไก่สไลด์', 'อกสไลด์ไก่', 'ไก่สไลด์อก', 'ไก่อกสไลด์', 'สไลด์อกไก่', 'สไลด์ไก่อก', 'สันในไก่สไลด์', 'สันในสไลด์ไก่', 'สันไก่ในสไลด์', 'สันไก่สไลด์ใน', 'ในสันไก่สไลด์', 'ในสันสไลด์ไก่', 'ในไก่สันสไลด์', 'ในไก่สไลด์สัน', 'ไก่สันในสไลด์', 'ไก่สันสไลด์ใน', 'ไก่ในสไลด์สัน', 'ไก่ในสันสไลด์', 'สไลด์ไก่ในสัน', 'สไลด์ไก่สันใน', 'สไลด์สันไก่ใน', 'สไลด์สันในไก่', 'ขนมจีบ', 'เกี๊ยวซ่าไก่', 'หมูทรัฟเฟิล', 'สามชั้นทอดเหล้าจีน', 'ชีสบอล', 'เฟรนช์ฟรายส์', 'คางกุ้งทอด', 'ไก่เกี๊ยวซ่า', 'กำหล่ำปลีซอย', 'ผักกาดขาว', 'ผักบุ้ง', 'ผักขึ้นฉ่าย', 'ข้าวโพดอ่อน', 'เห็ดออรินจิ', 'เห็ดเข็มทอง', 'เห็ดหูหนู', 'เห็ดหอม', 'สาหร่ายวากาเมะ', 'ข้าวโพด', 'แครอท', 'หอมหัวใหญ่', 'ผัก', 'ขึ้นฉ่าย', 'กะหล่ำปลีซอย', 'ผักกาดขาว', 'ผักขึ้นฉ่าย', 'ข้าวโพดอ่อน', 'เห็ดออรินจิ', 'เห็ดเข็มทอง', 'เห็ดหูหนู', 'เห็ดหอม', 'สาหร่ายวากาเมะ', 'เผือก', 'แครอท', 'หอมหัวใหญ่', 'ซอยกะหล่ำปลี', 'ขาวผักกาด', 'ขึ้นฉ่าย', 'ข้าวโพด', 'เห็ด', 'ออรินจิ', 'เข็มทอง', 'หูหนู', 'หอม', 'สาหร่าย', 'วากาเมะ', 'หอมหัว', 'กะหล่ำ', 'กะหล่ำปลี', 'ผักกาด', 'ฉ่าย', 'ไอศกรีม', 'เค้ก', 'ไอติม', 'ไอศกรีมช็อกโกแลต', 'ไอศกรีมไมโล', 'ไอศกรีมช็อกโกแลตชิพ', 'ไอศกรีมวานิลลา', 'ไอศกรีมมะนาว', 'ไอศกรีมชาเขียว', 'ไอศกรีมกะทิ', 'ไอศกรีมสตอเบอรี่ ทวิสท์', 'ไอศกรีมสตอเบอรี่', 'ไอติมช็อกโกแลต', 'ไอติมไมโล', 'ไอติมช็อกโกแลตชิพ', 'ไอติมวานิลลา', 'ไอติมมะนาว', 'ไอติมชาเขียว', 'ไอติมกะทิ', 'ไอติมสตอเบอรี่', 'ช็อกโกแลต', 'ไมโล', 'ช็อกโกแลตชิพ', 'สตอเบอรี่', 'วานิลลา', 'น้ำดื่ม', 'น้ำเปล่า', 'น้ำ', 'โค้ก', 'แฟนต้า', 'สไปรท์', 'เป๊ปซี่', 'น้ำพั้นซ์', 'น้ำชาเขียว', 'น้ำฝรั่ง', 'น้ำโค้ก', 'น้ำแฟนต้า', 'น้ำสไปรท์', 'น้ำเป๊ปซี่', 'หมี่หยกลวกน้ำมันทรัฟเฟิล', 'วุ้นเส้น', 'เส้นบุก', 'มาม่า', 'หมี่หยก', 'เส้น', 'ลูกชิ้น', 'ลูกชิ้นเอ็นเนื้อ', 'ลูกชิ้นปลาหมึก', 'ลูกชิ้นลาวาไข่กุ้ง', 'ลูกชิ้นลาวาไข่ปลา', 'ลูกชิ้นลาวาชีส', 'ลูกชิ้นครีมซอส', 'เอ็นเนื้อลูกชิ้น', 'ปลาหมึกลูกชิ้น', 'ลาวาไข่กุ้งลูกชิ้น', 'ลาวาไข่ปลาลูกชิ้น', 'ลาวาชีสลูกชิ้น', 'ครีมซอสลูกชิ้น', 'ลูกชิ้น', 'ลูกชิ้นเอ็นเนื้อ', 'ลูกชิ้นปลาหมึก', 'ลูกชิ้นลาวาไข่กุ้ง', 'ลูกชิ้นลาวาไข่ปลา', 'ลูกชิ้นลาวาชีส', 'ลูกชิ้นครีมซอส', 'เอ็นเนื้อลูกชิ้น', 'ปลาหมึกลูกชิ้น', 'ลาวาไข่กุ้งลูกชิ้น', 'ลาวาไข่ปลาลูกชิ้น', 'ลาวาชีสลูกชิ้น', 'ครีมซอสลูกชิ้น', 'ฟองเต้าหู้ซีฟู้ด']
new_food = [' '.join(word_tokenize(food, engine='newmm')) for food in new_food]
new_food_vectorized = vectorizer.transform(new_food)
predictions = model.predict(new_food_vectorized)
print(f"Predictions for new food: {predictions}")

# บันทึกโมเดลไว้ใช้งานในอนาคต
joblib.dump(model, 'food_classifier_model.pkl')
