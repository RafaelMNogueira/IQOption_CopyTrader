
**Robo de COPY TRADER criado utilizando a API NÃO OFICIAL** https://github.com/Lu-Yi-Hsun/iqoptionapi

*Eu realizei algumas modificações no código disponibilizado por: **IQ CODING **  (https://www.youtube.com/IQCoding/videos)

**Arquivos Necessários para o Funcionamento do ROBO:**
- Notepad++ : https://notepad-plus-plus.org/downloads/
- Download Python 3.7:https://www.python.org/downloads/
- API Não Oficial: Eu utilizei uma modificação no stable_api.py para o funcionamento do check_win_v3 essa personalização foi disponibilizada pelo **IQ CODING **  (https://www.youtube.com/IQCoding/videos)

**Principais Modificações realizadas no Código:**
- Inclusão do Copy Binário;
- Inclusão de Cores;
- Formação dos textos no Robo;

**Configuração do Robo:**
- Abrir o arquivo "CopyTrader.py" e modificar a linha 17 trocando a palavra "login" e "senha" pelo seu login e senha de acesso a IqOption.
- Na linha 20 informar se e conta de treinamento ou real.
- O arquivo config.txt deverá ser configurado de acordo com a sua estratégia. 

**Explicação do Arquivo Config:**
- paridade: Deverá ser informado o PAR que deseja copiar, lembrando que o robo copia apenas 1 par de moedas;
- valor_entrada: O valor das suas opreação;
- op_binario e op_binario_turbo: Deve estar marcado S para operar em Binário;
- op_digital: Deve estar marcado S para operar em Digital;

*OBS: Caso deixe "S" em op_binario, op_binario_turbo e op_digital o robo vai apresentar erro, deve marcar "S" apenas em op_binario, op_binario_turbo ou op_digital *.

- timeframe: Tempo de Expiração da Vela na Operação;
- martingale: Deve estar marcado S para realizar Martingale;
- sorosgale: Deve estar marcado S para realizar SorosGale;
- niveis: Nivel do Martingale ou SorosGale

*OBS: Caso deixe "S" em martingale e sorosgale o robo vai apresentar erro, deve marcar "S" apenas em martingale ou sorosgale*.

- stop_loss: Valor do Stop Loss
- stop_win: Valor do Stop Win

- valor_minimo: Valor minimo do Trader para o Robo Copiar
- filtro_pais: Caso queira copiar algum País bastar colocar as Iniciais, recomento sempre "todos"
- filtro_top_traders: Nesse opção informa qual a posição do Rank quer copiar, por exemplo: se colocar 100 ele vai copiar os 100 primeiros do rank, caso queira todos, deixe em 0
- filtro_diferenca_sinal: Nessa opção, você colocar o tempo máximo do delay entre a entrada do trader copiada e a sua. (Tempo em Segundos, recomendamos entre 2 e 10)
- seguir_ids: Nessa opção você colocar o ID do trader que quer copiar, caso queira copiar do rank deixe em branco. Se for colocar mais de um ID usar apenas ",". Exemplo: 1234567,89012345

