# Trabalho 2 de IAR

Esta pasta contém os algoritmos referentes ao Trabalho 2 de IAR

## Instruções de Execução

Estes experimentos foram desenvolvidos na linguagem Python, versão `3.8.10`, logo, é necessário ter no mínimo essa versão instalada para poder reproduzir os experimentos.
Para verificar a versão do python, execute o comando:
```
python3 --version
```

É necessário ter o gerenciador de pacotes do Python instalado, para instalá-lo, execute os seguintes comandos:
```
sudo apt-get update
sudo apt-get install python3-pip
```

Para verificar se o pip foi instalado corretamente, execute o comando:
```
pip3 --version
```

Seu output deveria ser algo parecido com:
```
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
```

Após, é necessário instalar a biblioteca `pygame`, isso pode ser feito pelo comando:
```
pip3 install pygame
```

É necessário que haja um arquivo chamado `mapa.txt` na pasta `inputs` para poder executar a simulação. Este arquivo deve ter 42 linhas, cada uma com 42 números de 0 até 9 separados por espaços, cada número representa uma célula no mapa da simulação.

Inicialmente, esse arquivo já está na pasta e pode ser alterado livremente.

Para executar a simulação, basta executar o comando:
```
python3 Main.py
```

Os seguintes argumentos de linha de comando podem ser fornecidos:

    -h Printa um menu de ajuda explicando os argumentos e não executa o programa

    -r Lê posição do robô por arquivo
    -R Pula a leitura da posição do robô (arquivo e usuário)

    -r Lê posição da fábrica por arquivo
    -F Pula a leitura da posição das fábricas (arquivo e usuário)

    -o Lê posição dos obstáculos
    -O Não insere obstáculo

    -W N define que N operações inúteis são feitas entre passos do algoritmo, usado para desacelerar a execução

As flags (-r, -R), (-f -F) e (-o, -O) são mutuamente exclusivas, tentar executar o programa com as duas causará erro. Assim como, tentar executar o programa com a flag -h e qualquer outra não executará nada, pois a flag -h não executa o programa.

Para executar a simulação com algum argumento de linha de comando, basta executar o seguinte comando:
```
python3 Main.py -flag1 -flag2 ...
```

Por exemplo:
```
python3 Main.py -R -F -O -W 0
```