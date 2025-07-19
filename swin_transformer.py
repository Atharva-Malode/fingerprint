import torch
import torch.nn as nn
from torchvision.models.swin_transformer import swin_t, Swin_T_Weights

class SEBlock(nn.Module):
    """Squeeze-and-Excitation attention block"""
    def __init__(self, in_channels, reduction=16):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // reduction, in_channels),
            nn.Sigmoid()
        )

    def forward(self, x):
        B, C, H, W = x.shape
        scale = self.pool(x).view(B, C)
        scale = self.fc(scale).view(B, C, 1, 1)
        return x * scale

class FingerprintSwinWithAttention(nn.Module):
    def __init__(self, num_classes=3, freeze_base=True):
        super().__init__()
        

        self.backbone = swin_t(weights=Swin_T_Weights.IMAGENET1K_V1)
        

        if freeze_base:
            for param in self.backbone.parameters():
                param.requires_grad = False

        self.backbone.head = nn.Identity()

        feature_dim = 768

        self.attention = SEBlock(in_channels=feature_dim)

        self.classifier = nn.Sequential(
            nn.Linear(feature_dim, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        
    def forward(self, x):
        features = self.backbone.features(x) 
        features = features.permute(0, 3, 1, 2)
        features = self.attention(features)
        features = torch.mean(features, dim=[2, 3])    
        output = self.classifier(features)        
        return output
