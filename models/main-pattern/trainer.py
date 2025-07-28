import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import json
from pathlib import Path
from datetime import datetime

class Trainer:
    def __init__(self, model, train_loader, val_loader, test_loader=None, device='cpu', lr=1e-4):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.device = device
        
        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(self.model.parameters(), lr=lr, weight_decay=0.01)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=10, gamma=0.5)
        
        self.best_val_acc = 0
        
        # Create folders for saving models and logs
        self.weights_folder = Path("model_weights")
        self.weights_folder.mkdir(exist_ok=True)
        
        self.logs_folder = Path("training_logs")
        self.logs_folder.mkdir(exist_ok=True)
        
        # Create run-specific folder
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_folder = self.logs_folder / f"run_{self.run_id}"
        self.run_folder.mkdir()
        
        # File paths
        self.log_file = self.run_folder / "training_metrics.json"
        self.best_model_path = self.weights_folder / f"best_model_{self.run_id}.pth"
        self.final_model_path = self.weights_folder / f"final_model_{self.run_id}.pth"
        
        # Metrics tracking
        self.metrics = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
            "learning_rates": [],
            "test_acc": None,
            "best_epoch": 0
        }
        
        print(f"✅ Trainer initialized")
        print(f"📁 Models will be saved in: {self.weights_folder}")
        print(f"📊 Logs will be saved in: {self.run_folder}")

    def train_epoch(self):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        progress_bar = tqdm(self.train_loader, desc="Training", leave=False)
        for batch_idx, (images, labels) in enumerate(progress_bar):
            images, labels = images.to(self.device), labels.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)
            
            # Update progress bar
            current_acc = 100. * correct / total
            progress_bar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{current_acc:.2f}%'
            })
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100. * correct / total
        return epoch_loss, epoch_acc

    def validate_epoch(self):
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in tqdm(self.val_loader, desc="Validating", leave=False):
                images, labels = images.to(self.device), labels.to(self.device)
                
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                running_loss += loss.item()
                _, predicted = outputs.max(1)
                correct += predicted.eq(labels).sum().item()
                total += labels.size(0)
        
        val_loss = running_loss / len(self.val_loader)
        val_acc = 100. * correct / total
        return val_loss, val_acc

    def fit(self, epochs=20):
        print(f"\n🚀 Starting training for {epochs} epochs...")
        
        for epoch in range(1, epochs + 1):
            print(f"\n📊 Epoch {epoch}/{epochs}")
            
            # Training
            train_loss, train_acc = self.train_epoch()
            
            # Validation
            val_loss, val_acc = self.validate_epoch()
            
            # Learning rate step
            current_lr = self.optimizer.param_groups[0]['lr']
            self.scheduler.step()
            
            # Log metrics
            self.metrics["train_loss"].append(train_loss)
            self.metrics["train_acc"].append(train_acc)
            self.metrics["val_loss"].append(val_loss)
            self.metrics["val_acc"].append(val_acc)
            self.metrics["learning_rates"].append(current_lr)
            
            # Print epoch results
            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            print(f"Learning Rate: {current_lr:.6f}")
            
            # Save best model
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                self.metrics["best_epoch"] = epoch
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'val_acc': val_acc,
                    'train_acc': train_acc
                }, self.best_model_path)
                print(f"✅ New best model saved! Val Acc: {val_acc:.2f}%")
            
            # Save metrics after each epoch
            self._save_metrics()
        
        # Save final model
        torch.save({
            'epoch': epochs,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'final_val_acc': val_acc,
            'best_val_acc': self.best_val_acc
        }, self.final_model_path)
        
        print(f"\n🎯 Training completed!")
        print(f"📈 Best validation accuracy: {self.best_val_acc:.2f}% (Epoch {self.metrics['best_epoch']})")
        print(f"💾 Best model saved at: {self.best_model_path}")
        print(f"💾 Final model saved at: {self.final_model_path}")

    def test(self):
        if self.test_loader is None:
            print("⚠️ No test loader provided.")
            return None
        
        # Load best model for testing
        checkpoint = torch.load(self.best_model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        print(f"\n🧪 Testing with best model (Epoch {checkpoint['epoch']})...")
        
        self.model.eval()
        correct = 0
        total = 0
        class_correct = {}
        class_total = {}
        
        with torch.no_grad():
            for images, labels in tqdm(self.test_loader, desc="Testing"):
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                _, predicted = outputs.max(1)
                
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
                
                # Per-class accuracy
                for label, pred in zip(labels, predicted):
                    label_item = label.item()
                    if label_item not in class_correct:
                        class_correct[label_item] = 0
                        class_total[label_item] = 0
                    
                    class_total[label_item] += 1
                    if label_item == pred.item():
                        class_correct[label_item] += 1
        
        test_acc = 100. * correct / total
        self.metrics["test_acc"] = test_acc
        
        # Print results
        print(f"\n🎯 Test Results:")
        print(f"Overall Test Accuracy: {test_acc:.2f}%")
        
        # Per-class results
        for class_idx in sorted(class_correct.keys()):
            class_acc = 100. * class_correct[class_idx] / class_total[class_idx]
            print(f"Class {class_idx} Accuracy: {class_acc:.2f}% ({class_correct[class_idx]}/{class_total[class_idx]})")
        
        self._save_metrics()
        return test_acc

    def _save_metrics(self):
        """Save metrics to JSON file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.metrics, f, indent=4)
