import cv2
import numpy as np
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import matplotlib.pyplot as plt

# Pastas de entrada e saída
PASTA_IMAGENS = "imagens"
PASTA_RESULTADOS = "resultados_agua_vegetacao"
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

# Faixa de cor para água (em HSV)
AZUL_BAIXO = np.array([85, 40, 20])
AZUL_ALTO = np.array([135, 255, 255])

# Faixa de cor para vegetação (verde em HSV)
VERDE_BAIXO = np.array([35, 40, 20])
VERDE_ALTO = np.array([85, 255, 255])

# Limite de pixels por imagem (100 MP)
LIMITE_PIXELS = 10000 * 10000  # 100 milhões de pixels

def detectar_agua_azul_vegetacao(imagem_path):
    inicio_tempo = time.time()

    try:
        imagem_bgr = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
        if imagem_bgr is None:
            raise ValueError("Imagem inválida ou muito grande para ser carregada.")

        altura, largura = imagem_bgr.shape[:2]
        total_pixels = altura * largura

        # Redimensiona se necessário
        if total_pixels > LIMITE_PIXELS:
            escala = (LIMITE_PIXELS / total_pixels) ** 0.5
            nova_largura = int(largura * escala)
            nova_altura = int(altura * escala)
            imagem_bgr = cv2.resize(imagem_bgr, (nova_largura, nova_altura))
            print(f"[⚠️] Redimensionada: {os.path.basename(imagem_path)} -> {nova_largura}x{nova_altura}")

        imagem_hsv = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2HSV)

        # Máscara da água
        mascara_agua = cv2.inRange(imagem_hsv, AZUL_BAIXO, AZUL_ALTO)
        total_agua = cv2.countNonZero(mascara_agua)

        # Máscara da vegetação
        mascara_vegetacao = cv2.inRange(imagem_hsv, VERDE_BAIXO, VERDE_ALTO)
        total_vegetacao = cv2.countNonZero(mascara_vegetacao)

        # Imagens de saída
        resultado_agua = cv2.bitwise_and(imagem_bgr, imagem_bgr, mask=mascara_agua)
        resultado_vegetacao = cv2.bitwise_and(imagem_bgr, imagem_bgr, mask=mascara_vegetacao)

        nome_arquivo = os.path.basename(imagem_path)
        caminho_agua = os.path.join(PASTA_RESULTADOS, f"agua_{nome_arquivo}")
        caminho_vegetacao = os.path.join(PASTA_RESULTADOS, f"vegetacao_{nome_arquivo}")

        cv2.imwrite(caminho_agua, resultado_agua)
        cv2.imwrite(caminho_vegetacao, resultado_vegetacao)

        tempo_execucao = time.time() - inicio_tempo
        return (nome_arquivo, total_agua, total_vegetacao, tempo_execucao)

    except Exception as e:
        print(f"[ERRO] Falha ao processar '{imagem_path}': {str(e)}")
        return (os.path.basename(imagem_path), 0, 0, 0.0)

def gerar_grafico(tempos):
    nomes = [x[0] for x in tempos]
    valores = [x[3] for x in tempos]

    plt.figure(figsize=(12, 6))
    plt.barh(nomes, valores, color='skyblue')
    plt.xlabel("Tempo de processamento (s)")
    plt.title("Tempo por imagem")
    plt.tight_layout()
    plt.savefig("grafico_desempenho.png")
    print("[📊] Gráfico de desempenho salvo como 'grafico_desempenho.png'.")

def main():
    imagens = [
        os.path.join(PASTA_IMAGENS, f)
        for f in os.listdir(PASTA_IMAGENS)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff'))
    ]

    total_imagens = len(imagens)
    if total_imagens == 0:
        print("[AVISO] Nenhuma imagem encontrada na pasta.")
        return

    # Solicita o número de threads ao usuário
    while True:
        try:
            entrada = input(f"[?] Quantas threads deseja usar? (1-{min(64, total_imagens)}): ")
            num_threads = int(entrada)
            if 1 <= num_threads <= min(64, total_imagens):
                break
            else:
                print(f"[ERRO] Digite um número entre 1 e {min(64, total_imagens)}.")
        except ValueError:
            print("[ERRO] Entrada inválida. Digite um número inteiro.")

    print(f"[INFO] Iniciando processamento com {num_threads} threads...\n")

    inicio_total = time.time()

    resultados = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futuros = {executor.submit(detectar_agua_azul_vegetacao, img): img for img in imagens}
        for futuro in tqdm(as_completed(futuros), total=total_imagens, desc="Processando"):
            resultados.append(futuro.result())

    fim_total = time.time()
    tempo_total = fim_total - inicio_total

    total_agua_geral = sum(r[1] for r in resultados)
    total_vegetacao_geral = sum(r[2] for r in resultados)
    tempo_medio = tempo_total / total_imagens if total_imagens else 0

    print("\n===== RELATÓRIO DE DESEMPENHO =====")
    print(f"🧵 Threads utilizadas          : {num_threads}")
    print(f"🖼️  Total de imagens processadas: {total_imagens}")
    print(f"💧 Total de pixels de água      : {total_agua_geral}")
    print(f"🌿 Total de pixels de vegetação : {total_vegetacao_geral}")
    print(f"⏱️  Tempo total de execução     : {tempo_total:.2f} segundos")
    print(f"⏱️  Tempo médio por imagem      : {tempo_medio:.2f} segundos")

    for nome, agua, vegetacao, tempo_img in resultados:
        print(f"📄 {nome:30s} | 💧 {agua:10d} px | 🌿 {vegetacao:10d} px | ⏱️  {tempo_img:.2f} s")

    gerar_grafico(resultados)

if __name__ == "__main__":
    main()