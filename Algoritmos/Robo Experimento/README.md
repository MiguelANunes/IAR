# Experimentos do Trabalho 2 de IAR

Esta pasta contém os algoritmos referentes ao experimento do trabalho 2 de IAR, assim como os resultados obtidos

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

Após, é necessário dar permissão de execução para os arquivos `auto_tester.sh` e `clean.sh`, isso pode ser feito pelos comandos:
```
chmod +x auto_tester.sh
chmod +x clean.sh
```

É necessário que haja um arquivo chamado `mapa.txt` na pasta `inputs` para poder executar a simulação. Este arquivo deve ter 42 linhas, cada uma com 42 números de 0 até 9 separados por espaços, cada número representa uma célula no mapa da simulação.

Inicialmente, esse arquivo já está na pasta e pode ser alterado livremente.

Para executar a simulação, basta executar o comando:
```
./auto_tester.sh
```

Isso irá gerar um novo conjunto de dados para a simulação e irá executar a simulação com os algoritmos A*, Dijkstra e Greedy Best-First Search, nessa ordem. Após executar os 3, irá criar um novo conjunto de dados e recomeçara a simulação.

**Aviso**: Ao começar uma nova rodada de testes, os resultados da última execução serão deletados.

## Resultados dos Experimentos:

Os resultado da última execução do experimento se encontram na pasta `outputs`, essa pasta contém arquivos .txt cujo nome é do formato `algoritmo_numeroExecução` que contém os resultados da execução número `numeroExecução` do algoritmo `algoritmo`.

Ademais, na pasta `Imagens` há prints do estado inicial do mapa para cada execução, assim como um print do estado final do mapa após a execução de um dado algoritmo. Seu esquema de nomes segue o mesmo padrão descrito acima.
