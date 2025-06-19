# trabalho-resolução-de-problemas-programação-paralela
Projeto desenvolvido para identificar automaticamente corpos d'água (como rios, lagos e canais) em imagens de áreas urbanas, utilizando técnicas de processamento de imagem com programação paralela para otimização de desempenho.

 -Introdução:
Este projeto tem como objetivo identificar automaticamente corpos d'água, como rios, lagos e canais, em imagens de áreas urbanas. Utilizando técnicas de processamento de imagens com programação paralela (ThreadPoolExecutor), o sistema busca otimizar o desempenho no processamento de grandes volumes de imagens.

-Descrição do Problema / Justificativa:
Com o aumento da disponibilidade de imagens de satélite e a crescente necessidade de monitoramento urbano, identificar automaticamente áreas com presença de água tornou-se uma tarefa relevante em diversas áreas, como planejamento urbano, gestão de recursos hídricos e análise ambiental.

Entretanto, o processamento sequencial dessas imagens pode levar a tempos de execução muito altos, especialmente com grandes conjuntos de dados. Por isso, este projeto utiliza programação paralela com múltiplas threads, permitindo processar várias imagens simultaneamente e reduzir o tempo total de execução.

O processamento é baseado na segmentação de cor em espaço HSV, aplicando uma faixa de azul que representa corpos d'água nas imagens analisadas.

Gráfico de Tempo Total por Quantidade de Threads
Exemplo de gráfico que você pode gerar no Excel, Google Sheets ou Matplotlib com os dados reais:

Eixo X: Número de Threads
Eixo Y: Tempo Total de Execução (segundos)




-Conclusão:
O uso de programação paralela com múltiplas threads demonstrou ser uma estratégia eficaz para reduzir o tempo total de execução na identificação de corpos d'água em imagens urbanas.

Conforme o número de threads aumentou, observou-se um ganho de desempenho (speedup), principalmente até o ponto em que o número de threads era proporcional ao número de imagens disponíveis.

A análise do speedup e do Eficiência Paralela (Efficiency ou Ffilim) mostrou que a paralelização tem limites práticos, sendo impactada por fatores como overhead de criação de threads, limitação de I/O e quantidade de núcleos reais da máquina..