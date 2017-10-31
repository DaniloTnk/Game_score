# GameScore

### Problema

Dado o seguinte log de um jogo de tiro em primeira pessoa:
```
23/04/2013 15:34:22 - New match 11348965 has started
23/04/2013 15:36:04 - Roman killed Nick using M16
23/04/2013 15:36:33 - <WORLD> killed Nick by DROWN
23/04/2013 15:39:22 - Match 11348965 has ended
```

### Resultado esperado

A partir de um input de um arquivo de log do formato acima, montar o ranking de cada partida, com a quantidade assassinatos e a quantidade de mortes de cada jogador;

### Premissas do Problema
* Assassinatos realizados pelo <WORLD> devem ser desconsiderados, no entanto, as mortes causadas pelo <WORLD> devem ser consideradas para o jogador que foi morto.

### Premissas da Solução

* A solução ira gerar um ranking por log. Sendo que o arquivo de log deve estar no formato acima sendo desconsiderado caso não esteja.
* O log deve conter todas entradas na mesma data.
* O horário deve estar de forma crescente, sendo aceita mais da uma ação no mesmo horário.
* Id's da partida (_New match_ e _match ended_) devem ser iguais para o log ser válido.
* O ranking será ordenado em ordem decrescente por quantidade de jogadores mortos (_Kills_), em caso de empate será levado em consideração o jogador que morreu menos (_Deaths_).
* Nome de jogador não tem limite de catactere, no entanto para o "_print_" final são exibidos apenas 7 caracteres.


## Execução do Script
O arquivo _game_score.py_ na pasta services contêm um método _main_ que executa a solução com base no arquivo de log _test/complete\_match.log_. Pode alterar essa configuração atravéz do arquivo _config.py_ na variável _FILE_PATH_

O código principal foi criado como um serviço, mas é possivel descomentar a classe main para executar o script.
Há um arquivo de configuração (config.py) com algumas variáveis globais utilizadas pelo código. Lá é possível alterar o caminho do arquivo de log que desejar utilizar. Nesse arquivo também estão configuradas mensagens de erro padrão.

## Testes

O código está com uma cobertura de testes de 94%. Sendo que os 6% não cobertos são exeções de erro.
O arquivo de testes /test/test.py utiliza por padrão os logs que estão na sua pasta.
