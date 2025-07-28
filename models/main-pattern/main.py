import torch
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
from swin_transformer import FingerprintSwinWithAttention
from trainer import Trainer

if __name__ == '__main__':

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_set = datasets.ImageFolder("preprocessed_data/train_set", transform=transform)
    val_set = datasets.ImageFolder("preprocessed_data/val_set", transform=transform)
    test_set = datasets.ImageFolder("preprocessed_data/test_set", transform=transform)

    print(f"Train samples: {len(train_set)}, Val samples: {len(val_set)}, Test samples: {len(test_set)}")
    print(f"Classes: {train_set.classes}")

    train_loader = DataLoader(train_set, batch_size=16, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_set, batch_size=16, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_set, batch_size=16, shuffle=False, num_workers=0)

    model = FingerprintSwinWithAttention(num_classes=3, freeze_base=False)
    trainer = Trainer(model, train_loader, val_loader, test_loader, device=device, lr=1e-4)


    trainer.fit(epochs=20)
    trainer.test()
