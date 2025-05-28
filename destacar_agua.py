import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu

# Carregar a imagem
imagem = cv2.imread(r"C:\Users\Arthur\Downloads\projeto_destacar_rios\imagem_satelite.jpeg")

imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

# Converter para tons de cinza
gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplicar filtro de suavização
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Realçar os rios com threshold adaptativo
thresh_val = threshold_otsu(blur)
mascara = blur < thresh_val  # regiões mais escuras (rios)

# Criar máscara colorida azul
mascara_colorida = np.zeros_like(imagem_rgb)
mascara_colorida[mascara] = [0, 255, 255]  # ciano

# Combinar com imagem original
imagem_destacada = cv2.addWeighted(imagem_rgb, 1, mascara_colorida, 0.7, 0)

# Exibir
plt.figure(figsize=(10, 6))
plt.imshow(imagem_destacada)
plt.title("Rios destacados em azul sobre imagem original")
plt.axis('off')
plt.show()
