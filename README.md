# trabalho-resolução-de-problemas-programação-paralela
Projeto desenvolvido para identificar automaticamente corpos d'água (como rios, lagos e canais) em imagens de áreas urbanas, utilizando técnicas de processamento de imagem com programação paralela para otimização de desempenho.


Introdução
O presente projeto tem como objetivo identificar automaticamente corpos d'água (como rios, lagos e canais) em imagens de áreas urbanas, utilizando técnicas de processamento de imagem combinadas com programação paralela para otimização de desempenho.

Foram utilizadas 305 imagens de alta resolução (em média entre 50MB e 60MB cada), processadas por meio de detecção de faixas de cor em HSV (Hue, Saturation, Value), com enfoque na faixa de tons azuis para água.

Descrição do Problema / Justificativa
Devido ao grande volume de dados (cerca de 18GB de imagens no total), o processamento sequencial (monothread) mostrou-se ineficiente, levando mais de 20 minutos para processar o conjunto completo de imagens. Isso motivou a implementação de um modelo de paralelização com múltiplas threads, utilizando a biblioteca concurrent.futures.ThreadPoolExecutor em Python.

O foco central foi analisar o ganho de desempenho (speedup) e a eficiência ao aumentar o número de threads utilizadas no processamento paralelo.

Resultados

Tempo Total de Execução (Segundos)
| Número de Threads | Tempo Total (s) |
| ----------------- | --------------- |
| 1                 | 1281.73         |
| 2                 | 772.48          |
| 4                 | 646.50          |
| 6                 | 576.75          |
| 8                 | 532.00          |
| 10                | 386.06          |

Tabela de Speedup e Eficiência (%)
| Número de Threads | Tempo (s) | Speedup | Eficiência (%) |
| ----------------- | --------- | ------- | -------------- |
| 1                 | 1281.73   | 1.00    | 100.0          |
| 2                 | 772.48    | 1.66    | 83.7           |
| 4                 | 646.50    | 1.98    | 49.5           |
| 6                 | 576.75    | 2.22    | 37.0           |
| 8                 | 532.00    | 2.41    | 30.2           |
| 10                | 386.06    | 3.32    | 33.2           |





Conclusão
A paralelização do processamento apresentou ganhos consideráveis em desempenho, especialmente até o uso de 10 threads. Foi observado:

Uma redução de mais de 3x no tempo total de execução ao passar de 1 para 10 threads.

Um speedup crescente, porém com queda gradual na eficiência conforme mais threads foram adicionadas (devido a overheads de gerenciamento de threads e limitações de I/O e CPU).

O projeto demonstra, na prática, os benefícios da programação paralela na área de processamento de imagens, especialmente ao lidar com grandes volumes de dados.


Bibliotecas Utilizadas:
cv2 (OpenCV) → Para leitura, processamento e manipulação das imagens.

numpy → Para criação e manipulação de arrays (usado principalmente na definição das faixas de cores em HSV).

os → Para manipulação de diretórios e caminhos de arquivos.

time → Para medir os tempos de execução.

concurrent.futures (ThreadPoolExecutor, as_completed) → Para implementação da programação paralela com múltiplas threads.

tqdm → Para exibir a barra de progresso durante o processamento das imagens.

matplotlib.pyplot → Para geração dos gráficos de desempenho (tempo, speedup e eficiência).

