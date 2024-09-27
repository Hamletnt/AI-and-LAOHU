from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import load_dataset, load_metric

# โหลด Tokenizer และ โมเดล
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# เตรียมข้อมูล
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, padding='max_length')

dataset = load_dataset('imdb', split='train[:10%]')
tokenized_dataset = dataset.map(preprocess_function, batched=True)
tokenized_dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])

# ฝึกอบรมโมเดล
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=8,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()

# บันทึกโมเดล
model.save_pretrained('./model')
tokenizer.save_pretrained('./model')
