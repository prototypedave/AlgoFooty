import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from sklearn.metrics import accuracy_score
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

class DeepNN(nn.Module):
    def __init__(self):
        super(DeepNN, self).__init__()
        self.form_branch = nn.Sequential(
            nn.Conv1d(in_channels=2, out_channels=32, kernel_size=2),
            nn.ReLU(),
            nn.AdaptiveMaxPool1d(1)
        )

        self.h2h_branch = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=32, kernel_size=2),
            nn.ReLU(),
            nn.AdaptiveMaxPool1d(1)
        )

        self.odds_branch = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU()
        )

        self.context_branch = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU()
        )

        self.combined = nn.Sequential(
            nn.Linear(32 + 32 + 16 + 32, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, h2h, form, odds, context):
        form = form.permute(0, 2, 1)  
        h2h = h2h.permute(0, 2, 1)   

        form_out = self.form_branch(form).squeeze(-1)
        h2h_out = self.h2h_branch(h2h).squeeze(-1)
        odds_out = self.odds_branch(odds)
        context_out = self.context_branch(context)

        merged = torch.cat([h2h_out, form_out, odds_out, context_out], dim=1)
        out = self.combined(merged)
        return out


def train_model(train_features, train_labels, test_features, test_labels,
                h2h_train, h2h_test, odds_train, odds_test, perf_train, perf_test,
                epochs=30, batch_size=16, lr=1e-3, patience=5):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    def to_tensor(x): return torch.tensor(x, dtype=torch.float32)
    train_data = TensorDataset(
        to_tensor(train_features),
        to_tensor(h2h_train),
        to_tensor(odds_train),
        to_tensor(perf_train),
        to_tensor(train_labels).unsqueeze(1)
    )
    test_data = TensorDataset(
        to_tensor(test_features),
        to_tensor(h2h_test),
        to_tensor(odds_test),
        to_tensor(perf_test),
        to_tensor(test_labels).unsqueeze(1)
    )

    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=batch_size)
    model = DeepNN().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=3)
    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for form, h2h, odds, perf, y in train_loader:
            form, h2h, odds, perf, y = form.to(device), h2h.to(device), odds.to(device), perf.to(device), y.to(device)
            optimizer.zero_grad()
            preds = model(h2h, form, odds, perf)
            loss = criterion(preds, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        model.eval()
        val_loss = 0
        val_preds, val_true = [], []
        with torch.no_grad():
            for form, h2h, odds, perf, y in test_loader:
                form, h2h, odds, perf, y = form.to(device), h2h.to(device), odds.to(device), perf.to(device), y.to(device)
                preds = model(h2h, form, odds, perf)
                loss = criterion(preds, y)
                val_loss += loss.item()
                val_preds.extend(preds.cpu().numpy())
                val_true.extend(y.cpu().numpy())

        val_loss /= len(test_loader)
        scheduler.step(val_loss)

        val_acc = accuracy_score((np.array(val_true) > 0.5).astype(int),
                                 (np.array(val_preds) > 0.5).astype(int))
        #print(f"Epoch {epoch+1}/{epochs} - Train Loss: {total_loss/len(train_loader):.4f} "
        #      f"- Val Loss: {val_loss:.4f} - Val Acc: {val_acc:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_model_state = model.state_dict()
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping triggered.")
                break

    model.load_state_dict(best_model_state)
    return model
