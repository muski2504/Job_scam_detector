import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import DistilBertTokenizer
from sklearn.model_selection import train_test_split

# 1. Load cleaned CSV
df = pd.read_csv('data/scam_posts_clean.csv')
print(f"Total rows: {len(df)}")

# 2. Tokenizer load karo
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# 3. PyTorch Dataset class
class JobPostDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=256):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'label': torch.tensor(self.labels[idx], dtype=torch.long)
        }

# 4. Train / Val / Test split — 80 / 10 / 10
X = df['text'].tolist()
y = df['is_scam'].tolist()

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

# 5. Dataset objects banao
train_dataset = JobPostDataset(X_train, y_train, tokenizer)
val_dataset   = JobPostDataset(X_val, y_val, tokenizer)
test_dataset  = JobPostDataset(X_test, y_test, tokenizer)

print("Data loader ready!")