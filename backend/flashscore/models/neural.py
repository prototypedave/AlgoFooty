import torch
import os
import numpy as np
import random

# Set seeds for reproducibility
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

 # Define model
class NeuralNet(nn.Module):
    def __init__(self, input_size, num_classes):
        super(NeuralNet, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)  
        )

    def forward(self, x):
        return self.layers(x)
    
 # Plot graphs
def plot_graphs(history, metric):
    plt.plot(history[metric])
    plt.plot(history['val_' + metric])
    plt.title(f'Training and validation {metric}')
    plt.xlabel('Epochs')
    plt.ylabel(metric)
    plt.legend([metric, 'val_' + metric])
    #plt.show()

def neural(df, df_pred, feature_cols, target_col="target", target_class=1, report=False):
    df = df.sort_values("match_time").reset_index(drop=True)
    dataset = df[feature_cols].copy()
    dataset = dataset.dropna().reset_index(drop=True)
    target = df.loc[dataset.index, target_col]

    train_size = int(len(dataset) * 0.8)
    train_ds = dataset.iloc[:train_size]
    train_labels = target.iloc[:train_size]
    test_ds = dataset.iloc[train_size:]
    test_labels = target.iloc[train_size:]

    stdsc = StandardScaler()
    X_train = stdsc.fit_transform(train_ds)
    X_test = stdsc.transform(test_ds)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(train_labels.values, dtype=torch.long)  
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(test_labels.values, dtype=torch.long)

    val_split = 0.2
    val_size = int(len(X_train_tensor) * val_split)
    train_subset_size = len(X_train_tensor) - val_size
    X_train_subset = X_train_tensor[:train_subset_size]
    y_train_subset = y_train_tensor[:train_subset_size]
    X_val = X_train_tensor[train_subset_size:]
    y_val = y_train_tensor[train_subset_size:]

    train_subset_dataset = TensorDataset(X_train_subset, y_train_subset)
    train_loader = DataLoader(train_subset_dataset, batch_size=32, shuffle=True)

    num_classes = len(torch.unique(y_train_tensor))
    model = NeuralNet(input_size=X_train.shape[1], num_classes=num_classes)
   
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.7)

    model.train()
    epochs = 5
    
    # For model evaluation
    history = {'loss': [], 'accuracy': [], 'val_loss': [], 'val_accuracy': [], 'lr': []}
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_loss /= train_subset_size
        train_accuracy = correct / total

        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val)
            val_loss = criterion(val_outputs, y_val).item()
            _, val_pred = torch.max(val_outputs, 1)
            val_accuracy = (val_pred == y_val).sum().item() / len(y_val)

        scheduler.step()

        history['loss'].append(train_loss)
        history['accuracy'].append(train_accuracy)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_accuracy)
        history['lr'].append(optimizer.param_groups[0]['lr'])

    plot_graphs(history, "accuracy")
    plot_graphs(history, "loss")

    model.eval()
    with torch.no_grad():
        outputs = model(X_test_tensor)
        test_loss = criterion(outputs, y_test_tensor).item()
        _, predicted = torch.max(outputs, 1)
        test_accuracy = (predicted == y_test_tensor).sum().item() / len(y_test_tensor)
        probs = torch.softmax(outputs, dim=1).numpy()
        
    if df_pred is not None and not df_pred.empty:
        df_pred = df_pred.copy()
        X_pred = stdsc.transform(df_pred[feature_cols])
        X_pred = X_pred.dropna()
        X_pred_tensor = torch.tensor(X_pred, dtype=torch.float32)

        with torch.no_grad():
            pred_outputs = model(X_pred_tensor)
            pred_probs = torch.softmax(pred_outputs, dim=1)
            _, pred_classes = torch.max(pred_probs, dim=1)

        df_pred["predicted_class"] = pred_classes
        for c in range(pred_probs.shape[1]):
            df_pred[f"class_{c}_prob"] = pred_probs[:, c].numpy()

        df_pred = df_pred.sort_values(by=[f"class_{target_class}_prob"], ascending=False)
    else:
        df_pred = None

    return df_pred