import cv2
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor

PASTA_IMAGENS = "imagens"
PASTA_RESULTADOS = "resultados_agua"
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

# Faixas HSV para tons de azul (comuns em água)
AZUL_BAIXO = np.array([90, 50, 50])
AZUL_ALTO = np.array([130, 255, 255])

def detectar_agua_azul(imagem_path):
    imagem_bgr = cv2.imread(imagem_path)
    if imagem_bgr is None:
        print(f"[ERRO] Imagem inválida: {imagem_path}")
        return 0

    imagem_hsv = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2HSV)

    # Máscara para tons de azul
    mascara_agua = cv2.inRange(imagem_hsv, AZUL_BAIXO, AZUL_ALTO)

    total_agua = cv2.countNonZero(mascara_agua)

    # Destacar as áreas de água
    resultado = cv2.bitwise_and(imagem_bgr, imagem_bgr, mask=mascara_agua)
    nome_arquivo = os.path.basename(imagem_path)
    caminho_saida = os.path.join(PASTA_RESULTADOS, f"agua_{nome_arquivo}")
    cv2.imwrite(caminho_saida, resultado)

    print(f"[INFO] {nome_arquivo}: {total_agua} pixels de água detectados.")
    return total_agua

def main():
    imagens = [
        os.path.join(PASTA_IMAGENS, f)
        for f in os.listdir(PASTA_IMAGENS)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]

    with ProcessPoolExecutor() as executor:
        resultados = list(executor.map(detectar_agua_azul, imagens))

    total_geral = sum(resultados)
    print(f"\n💧 Total geral de áreas com água detectadas (em pixels): {total_geral}")

if __name__ == "__main__":
    main()
