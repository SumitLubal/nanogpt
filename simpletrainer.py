import torch
from transformers import AutoModelWithLMHead, AutoTokenizer

# Load the dataset
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModelWithLMHead.from_pretrained('bert-base-uncased', num_labels=20)
train_dataset = tokenizer.batch_encode(file_path="input.txt", max_length=32, padding='max_length', truncation=True)

# Train the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-5)
for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in train_dataset:
        input_ids, attention_masks = batch
        input_ids = input_ids.to(device)
        attention_masks = attention_masks.to(device)
        labels = model(input_ids, attention_masks=attention_masks).logits
        loss = criterion(labels, input_ids)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print('Epoch {}: Loss = {:.4f}'.format(epoch+1, total_loss/(len(train_dataset)-1)))