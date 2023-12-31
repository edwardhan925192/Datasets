!pip install torch transformers
!pip install sentencepiece

from transformers import XLNetTokenizer, XLNetForSequenceClassification

model_id = 'xlnet-base-cased'
tokenizer = XLNetTokenizer.from_pretrained(model_id)
model = XLNetForSequenceClassification.from_pretrained(model_id, num_labels=10)  # Assuming 10 classes for classification

"""#Processing text data to tokens"""

import transformers
from torch.utils.data import Dataset, DataLoader
import pandas as pd

class CustomDataset(Dataset):
    def __init__(self, dataframe, tokenizer, text_column_name, label_column_name=None):
        self.dataframe = dataframe
        self.texts = dataframe[text_column_name].tolist()
        self.tokenizer = tokenizer
        if label_column_name:
            self.labels = dataframe[label_column_name].tolist()
        else:
            self.labels = None

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        inputs = self.tokenizer(self.texts[idx], return_tensors="pt", truncation=True, padding='max_length', max_length=300)
        if self.labels:
            return inputs, self.labels[idx]
        return inputs

tokenizer = transformers.AutoTokenizer.from_pretrained('xlnet-base-cased')
train_dataset = CustomDataset(dataframe=train, tokenizer=tokenizer, text_column_name='content', label_column_name='rating')
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

"""#Setting up device"""

import torch

# Check for CUDA availability and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Inform the user about the device being used
if device.type == "cuda":
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("Using CPU")

# Move the model to the device
model = model.to(device)

"""#Training
- you have to understand what gets inside the model and what it returns
"""

from transformers import AdamW
import torch.nn as nn

loss_function = nn.CrossEntropyLoss()

optimizer = AdamW(model.parameters(), lr=5e-5)

num_epochs = 1

for epoch in range(num_epochs):
    for batch_inputs, batch_labels in train_loader:
        print(batch_labels)

        # Convert the tuple of strings to a tensor of integers
        batch_labels_tensor = torch.tensor([int(label) for label in batch_labels], dtype=torch.long)

        # Send the tensor to the device
        batch_labels_tensor = batch_labels_tensor.to(device)

        for key in batch_inputs:
            batch_inputs[key] = batch_inputs[key].to(device)

        # Forward pass
        outputs = model(**batch_inputs,labels = batch_labels).loss

        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
