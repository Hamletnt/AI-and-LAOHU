import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# อ่านข้อมูลจากไฟล์ CSV (สมมติว่าไฟล์ชื่อ food_data.csv)
data = pd.read_csv("testtrain.csv")

# กำหนด Features (X) และ Target Variable (y)
X = data['ชื่อวัตถุดิบ']  # Features (ชื่อวัตถุดิบ)
y = data['ประเภทวัตถุดิบ']  # Target Variable (ประเภทวัตถุดิบ)

# แบ่งข้อมูลออกเป็น Training Set และ Testing Set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization (แปลงข้อความเป็นตัวเลข)
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# สร้างและฝึก Model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# ประเมินผล
accuracy = model.score(X_test_vec, y_test)
print("Accuracy:", accuracy)

# ทำนาย
new_item = "หมูสันคอ"
new_item_vec = vectorizer.transform([new_item])
predicted_category = model.predict(new_item_vec)[0]
print("Predicted category:", predicted_category)