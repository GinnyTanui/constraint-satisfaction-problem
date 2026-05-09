import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ── Load dataset ──────────────────────────────────────────────
train_data = pd.read_csv("mnist_train.csv")
test_data  = pd.read_csv("mnist_test.csv")

# ── Split features and labels ─────────────────────────────────
X_train = torch.tensor(train_data.iloc[:, 1:].values / 255.0, dtype=torch.float32)
y_train = torch.tensor(train_data.iloc[:, 0].values,          dtype=torch.long)

X_test  = torch.tensor(test_data.iloc[:, 1:].values / 255.0,  dtype=torch.float32)
y_test  = torch.tensor(test_data.iloc[:, 0].values,           dtype=torch.long)

# ── DataLoaders ───────────────────────────────────────────────
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
test_loader  = DataLoader(TensorDataset(X_test,  y_test),  batch_size=32)

# ── Build model ───────────────────────────────────────────────
model = nn.Sequential(
    nn.Linear(784, 128), nn.ReLU(),
    nn.Linear(128, 64),  nn.ReLU(),
    nn.Linear(64, 10)
)

optimizer = optim.Adam(model.parameters())
loss_fn   = nn.CrossEntropyLoss()

# ── Train ─────────────────────────────────────────────────────
for epoch in range(5):
    model.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(X_batch), y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch+1}/5  |  Loss: {avg_loss:.4f}")

# ── Evaluate ──────────────────────────────────────────────────
model.eval()
correct = 0
with torch.no_grad():
    for X_batch, y_batch in test_loader:
        preds   = model(X_batch).argmax(dim=1)
        correct += (preds == y_batch).sum().item()

print(f"\nTest Accuracy: {correct / len(y_test) * 100:.2f}%")

# ── Show 10 sample predictions ────────────────────────────────
model.eval()
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
fig.suptitle("MNIST Predictions", fontsize=14)

with torch.no_grad():
    for i, ax in enumerate(axes.flat):
        sample = X_test[i].unsqueeze(0)
        pred   = model(sample).argmax(dim=1).item()
        actual = y_test[i].item()

        ax.imshow(X_test[i].reshape(28, 28), cmap='gray')
        ax.set_title(f"Pred: {pred}  |  Real: {actual}",
                     color='green' if pred == actual else 'red')
        ax.axis('off')

plt.tight_layout()
plt.show()