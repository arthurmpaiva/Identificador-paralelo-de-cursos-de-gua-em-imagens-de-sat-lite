import torch
import torchvision.transforms as T
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Carregar imagem de satélite
image_path = "imagem_satelite.jpeg"  # troque pelo seu arquivo
image = Image.open(image_path).convert("RGB")

# Pré-processamento
transform = T.Compose([
    T.Resize(520),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

input_tensor = transform(image).unsqueeze(0)

# Carregar modelo DeepLabv3 pré-treinado
model = torch.hub.load('pytorch/vision:v0.14.0', 'deeplabv3_resnet101', pretrained=True)
model.eval()

# Segmentar imagem
with torch.no_grad():
    output = model(input_tensor)['out'][0]
output_predictions = output.argmax(0).byte().cpu().numpy()

# Classe 'água' é normalmente 21 no COCO-Stuff (podemos ajustar se necessário)
WATER_CLASS_INDEX = 21

# Criar máscara binária para água
mask = output_predictions == WATER_CLASS_INDEX

# Converter para imagem colorida com destaque azul
image_np = np.array(image)
highlight = image_np.copy()
highlight[~mask] = 0  # Zera tudo que não for água

# Mostrar resultados
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Imagem Original")
plt.imshow(image_np)

plt.subplot(1, 2, 2)
plt.title("Água Detectada (DeepLabv3)")
plt.imshow(highlight)
plt.show()

