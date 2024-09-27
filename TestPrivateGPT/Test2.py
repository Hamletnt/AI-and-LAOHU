from transformers import BertTokenizer, BertForSequenceClassification
import torch

# โหลดโมเดลและ Tokenizer
tokenizer = BertTokenizer.from_pretrained('./model')
model = BertForSequenceClassification.from_pretrained('./model')

# เตรียมข้อมูล
text = "หมูสามชั้น"
inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

# ทำนาย
outputs = model(**inputs)
prediction = torch.argmax(outputs.logits, dim=-1)

# แสดงผล
labels = ["หมู", "ผัก", "เนื้อ"]
print(f"Prediction: {labels[prediction.item()]}")