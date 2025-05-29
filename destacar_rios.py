import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Caminho da imagem
image_path = "imagem_rios.png"
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"Imagem não carregada: {os.path.abspath(image_path)}")

# Converter para HSV para trabalhar melhor com tons escuros
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Ajustar faixa para tons escuros / azuis típicos de rios
# Vamos tentar restringir também a saturação para evitar áreas muito cinzas/pretas
lower_dark = np.array([90, 30, 0])    # tom azulado, saturação média/baixa, brilho baixo
upper_dark = np.array([140, 255, 100])  # tom azul claro, saturação alta, brilho moderado

mask = cv2.inRange(hsv, lower_dark, upper_dark)

# Limpeza da máscara com operações morfológicas
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)  # preenche buracos
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN, kernel, iterations=2)  # remove ruídos

# Encontrar contornos nas regiões escuras
contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Função para detectar formato alongado (típico de rios)
def is_elongated(cnt, min_area=500, min_aspect_ratio=3.0):
    area = cv2.contourArea(cnt)
    if area < min_area:
        return False
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = max(w / h, h / w)  # maior lado dividido pelo menor
    return aspect_ratio >= min_aspect_ratio

# Criar imagem com rios destacados em azul
result = image.copy()
for cnt in contours:
    if is_elongated(cnt):
        cv2.drawContours(result, [cnt], -1, (255, 0, 0), thickness=cv2.FILLED)  # azul (BGR)

# Salvar a imagem final
output_path = "rios_destacados.png"
cv2.imwrite(output_path, result)
print(f"Imagem final salva como: {output_path}")

# Mostrar imagem original e com rios destacados
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.title("Imagem Original")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Rios Destacados (refinados por forma)")
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.tight_layout()
plt.show()
