# trabalho-resolução-de-problemas-programação-paralela
Projeto desenvolvido para identificar automaticamente corpos d'água (como rios, lagos e canais) em imagens de áreas urbanas, utilizando técnicas de processamento de imagem com programação paralela para otimização de desempenho.


Introdução

O presente projeto tem como objetivo identificar automaticamente corpos d'água (como rios, lagos e canais) em imagens de áreas urbanas, utilizando técnicas de processamento de imagem combinadas com programação paralela para otimização de desempenho.

Foram utilizadas 305 imagens de alta resolução (em média entre 50MB e 60MB cada), processadas por meio de detecção de faixas de cor em HSV (Hue, Saturation, Value), com enfoque na faixa de tons azuis para água.

💡Descrição do Problema / Justificativa
Devido ao grande volume de dados (cerca de 18GB de imagens no total), o processamento sequencial (monothread) mostrou-se ineficiente, levando mais de 20 minutos para processar o conjunto completo de imagens. Isso motivou a implementação de um modelo de paralelização com múltiplas threads, utilizando a biblioteca concurrent.futures.ThreadPoolExecutor em Python.

O foco central foi analisar o ganho de desempenho (speedup) e a eficiência ao aumentar o número de threads utilizadas no processamento paralelo.

Resultados


Tabela de Speedup e Eficiência (%)

| Threads | Tempo Total (s) | Speedup | Eficiência (%) |
| ------- | --------------- | ------- | -------------- |
| 1       | 900.0           | 1.00    | 100.0          |
| 2       | 490.0           | 1.84    | 92.0           |
| 4       | 275.0           | 3.27    | 81.8           |
| 6       | 205.0           | 4.39    | 73.2           |
| 8       | 180.0           | 5.00    | 62.5           |
| 10      | 165.0           | 5.45    | 54.5           |



✅ Conclusão
O projeto demonstrou a viabilidade de identificar automaticamente corpos d'água em imagens de satélite urbanas de alta resolução, reduzindo significativamente o tempo de processamento total por meio da programação paralela.

Em execução sequencial (1 thread), o processamento de 305 imagens levou cerca de 900 segundos. Usando 10 threads, o tempo caiu para aproximadamente 165 segundos, com um speedup de 5.45x e eficiência de 54.5%.

Os resultados mostram que a paralelização traz ganhos substanciais, embora não lineares, devido a overheads naturais de I/O, sincronização de threads e limites do hardware. Ainda assim, o desempenho obtido é satisfatório para aplicações práticas, permitindo análises mais rápidas em grandes volumes de dados.

Esses ganhos comprovam a importância de explorar o paralelismo em tarefas de processamento de imagens em larga escala para aplicações urbanas e ambientais.


Bibliotecas Utilizadas:
cv2 (OpenCV) → Para leitura, processamento e manipulação das imagens.

numpy → Para criação e manipulação de arrays (usado principalmente na definição das faixas de cores em HSV).

os → Para manipulação de diretórios e caminhos de arquivos.

time → Para medir os tempos de execução.

concurrent.futures (ThreadPoolExecutor, as_completed) → Para implementação da programação paralela com múltiplas threads.

tqdm → Para exibir a barra de progresso durante o processamento das imagens.

matplotlib.pyplot → Para geração dos gráficos de desempenho (tempo, speedup e eficiência).

