from iqoptionapi.stable_api import IQ_Option
from colorama import init, Fore, Back
import time, json, logging, configparser
from datetime import datetime, date, timedelta
from dateutil import tz
import sys

def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')  
        
    return {'inverter_sinal': arquivo.get('GERAL', 'inverter_sinal'),'op_binario_turbo': arquivo.get('GERAL', 'op_binario_turbo'),'op_digital': arquivo.get('GERAL', 'op_digital'),'op_binario': arquivo.get('GERAL', 'op_binario'),'seguir_ids': arquivo.get('GERAL', 'seguir_ids'),'stop_win': arquivo.get('GERAL', 'stop_win'), 'stop_loss': arquivo.get('GERAL', 'stop_loss'), 'payout': 0, 'banca_inicial': banca(), 'filtro_diferenca_sinal': arquivo.get('GERAL', 'filtro_diferenca_sinal'), 'martingale': arquivo.get('GERAL', 'martingale'), 'sorosgale': arquivo.get('GERAL', 'sorosgale'), 'niveis': arquivo.get('GERAL', 'niveis'), 'filtro_pais': arquivo.get('GERAL', 'filtro_pais'), 'filtro_top_traders': arquivo.get('GERAL', 'filtro_top_traders'), 'valor_minimo': arquivo.get('GERAL', 'valor_minimo'), 'paridade': arquivo.get('GERAL', 'paridade'), 'valor_entrada': arquivo.get('GERAL', 'valor_entrada'), 'timeframe': arquivo.get('GERAL', 'timeframe')}

logging.disable(level=(logging.DEBUG))
init(convert=True, autoreset=True)

API = IQ_Option('login','senha')
API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL
 
print(Fore.GREEN + '\nRobo Copy Modificado por Rafael Nogueira')
print(Fore.GREEN + 'Versão: 1.5')
 
while True: # Responsável pela conexão com a IQOPTION
    if API.check_connect() == False:
        print(Fore.RED + 'Falha ao se Conectar....')
        
        API.connect()
    else:
        print(Fore.GREEN + '\nConectado com Sucesso')
        break
    
    time.sleep(1)
        
  
def perfil(): # Exibindo os dados do Perfil
   perfil = json.loads(json.dumps(API.get_profile_ansyc()))
   return perfil

x = perfil()      

def timestamp_converter(x, retorno = 1): # Função para converter timestamp para o Horario de SP
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))
    
    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6] if retorno == 1 else hora.astimezone(tz.gettz('America/Sao Paulo'))

def banca():
    return API.get_balance()

def payout(par, tipo, timeframe = 1):
    if tipo == 'turbo':
        a = API.get_all_profit()
        return int(100 * a[par]['turbo'])
        
    elif tipo == 'digital':
    
        API.subscribe_strike_list(par, timeframe)
        while True:
            d = API.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, timeframe)
        return d


# Carrega as configuracoes
config = configuracao()

# Exibindo os dados iniciais
print(Fore.YELLOW +'\n --> Seus Dados')
print('Nome:', x['name']) 
TConta = API.get_balance_mode()
if TConta == 'PRACTICE':
    print('Conta de Treinamento')
if TConta == 'REAL':
    print('Conta Real')
moeda = API.get_currency() 
banca2 = API.get_balance()
if moeda == 'USD':
    print('Banca:','$',banca2)    
else:
    print('Banca:','R$',banca2)    

print(Fore.YELLOW +'\n --> Dados das Operações')
print('Paridade Selecionada:', str(config['paridade']))
if config['op_digital'] == 'S' and config['op_binario'] == 'N':
    print('Operar em: Digital')
elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
     print('Operar em: Binário')
print('TimeFrame:', str(config['timeframe']),'M')
if moeda == 'USD':
    print('Valor de Entrada:','$', str(config['valor_entrada']))   
else:
    print('Valor de Entrada:','R$', str(config['valor_entrada'])) 
print('Aplicar Martingale:', str(config['martingale']))
print('Aplicar SorosGale:', str(config['sorosgale']))
print('Niveis Martingale/SorosGale:', str(config['niveis']))

print(Fore.YELLOW +'\n --> Filtros Aplicados')
print('Valor Mínimo para Copy:','$', str(config['valor_minimo']))   
print('Delay Máximo:', str(config['filtro_diferenca_sinal']))
print('País Selecionados:', str(config['filtro_pais']))
print('Seguir Ranking:', str(config['filtro_top_traders']))
print('Seguir Ids:', str(config['seguir_ids']))
if config['inverter_sinal'] == 'S':
    print(Fore.GREEN +'Inverter Entradas: SIM')  
elif config['inverter_sinal'] == 'N':
    print(Fore.GREEN + 'Inverter Entradas: NÃO') 
print(Fore.YELLOW +'\n --> Gerenciamento')
print('Stop Win:', str(config['stop_win']))
print('Stop Loss:', str(config['stop_loss']))
print('\n')
corretos = input("Os dados acima estão corretos? [s] Sim | [n] Não:")

if corretos == 's':
    print('\n')
    print('=============================================================================================')
    print('                                    Buscando Operações')
    print('=============================================================================================')
else:
    print('\n')
    print(Fore.RED + 'COMO OS DADOS NÃO ESTÃO CORRETOS, FAVOR CORRIGIR A CONFIGURAÇÃO E REINICIAR O ROBO')
    exit()
    
def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')  
        
    return {'login': arquivo.get('GERAL', 'login'),'senha': arquivo.get('GERAL', 'senha'),'tipo_conta': arquivo.get('GERAL', 'tipo_conta'),'seguir_ids': arquivo.get('GERAL', 'seguir_ids'),'stop_win': arquivo.get('GERAL', 'stop_win'), 'stop_loss': arquivo.get('GERAL', 'stop_loss'), 'payout': 0, 'banca_inicial': banca(), 'filtro_diferenca_sinal': arquivo.get('GERAL', 'filtro_diferenca_sinal'), 'martingale': arquivo.get('GERAL', 'martingale'), 'sorosgale': arquivo.get('GERAL', 'sorosgale'), 'niveis': arquivo.get('GERAL', 'niveis'), 'filtro_pais': arquivo.get('GERAL', 'filtro_pais'), 'filtro_top_traders': arquivo.get('GERAL', 'filtro_top_traders'), 'valor_minimo': arquivo.get('GERAL', 'valor_minimo'), 'paridade': arquivo.get('GERAL', 'paridade'), 'valor_entrada': arquivo.get('GERAL', 'valor_entrada'), 'timeframe': arquivo.get('GERAL', 'timeframe')}

        
def martingale(tipo, valor, payout):
    if tipo == 'simples':
        return valor * 2.2
    else:
    
        lucro_esperado = float(valor) * float(payout)
        perca = valor
        while True:
            if round(float(valor) * float(payout), 2) > round(float(abs(perca)) + float(lucro_esperado), 2):
                return round(valor, 2)
                break
            valor += 0.01        


def entradas(config, entrada, direcao, timeframe):
    if config['op_digital'] == 'S' and config['op_binario'] == 'N': # ENTRADAS DIGITAL
        status,id = API.buy_digital_spot(config['paridade'], entrada, direcao, timeframe)
    
    elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
        status,id = API.buy(int(config['valor_entrada']), config['paridade'], direcao, int(config['timeframe']))
        
    if status:
        # STOP WIN/STOP LOSS
        banca_att = banca()
        stop_loss = False
        stop_win = False

        if round((banca_att - float(config['banca_inicial'])), 2) <= (abs(float(config['stop_loss'])) * -1.0):
            stop_loss = True
            
        if round((banca_att - float(config['banca_inicial'])) + (float(entrada) * float(config['payout'])) + float(entrada), 2) >= abs(float(config['stop_win'])):
            stop_win = True
        
        while True:
            if config['op_digital'] == 'S' and config['op_binario'] == 'N': # ENTRADAS DIGITAL
                status,lucro = API.check_win_digital_v2(id)
            elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
                status,lucro = API.check_win_v3(id)
            if status:
                if lucro > 0:       
                    return 'win',round(lucro, 2),stop_win
                else:               
                    return 'loss',(entrada),stop_loss
                break
        
        
    else:
        return 'error',' Erro ao Realizar a Entrada',False


# Carrega as configuracoes
config['banca_inicial'] = banca()


# Filtros
# 1? Filtro por valor da entrada copiada
# 2? Filtro para copiar entrada dos top X 
# 3? Filtro Pais

# Captura os dados necessarios do ranking
def filtro_ranking(config): # Filtro de Rank e Pais
    
    user_id = []
    
    try:
        ranking = API.get_leader_board('Worldwide' if config['filtro_pais'] == 'todos' else config['filtro_pais'].upper() , 1, int(config['filtro_top_traders']), 0)
    
        if int(config['filtro_top_traders']) != 0:
            for n in ranking['result']['positional']:
                id = ranking['result']['positional'][n]['user_id']
                user_id.append(id)              
    except:
        pass
        
    return user_id

filtro_top_traders = filtro_ranking(config)

if config['seguir_ids'] != '':
    if ',' in config['seguir_ids']:
        x = config['seguir_ids'].split(',')
        for old in x:
            filtro_top_traders.append(int(old))
    else:
        filtro_top_traders.append(int(config['seguir_ids']))

# Condição para Buscar Digital ou Binaria
if config['op_digital'] == 'S' and config['op_binario'] == 'N':
    tipo = 'live-deal-digital-option' # live-deal-binary-option-placed / live-deal-digital-option
    timeframe = 'PT'+config['timeframe']+'M' # PT5M / PT15M
    old = 0
elif config['op_binario'] == 'S' and config['op_digital'] == 'N' and config['op_binario_turbo'] == 'S': # BINARIO
    tipo = 'live-deal-binary-option-placed' # live-deal-binary-option-placed / live-deal-digital-option
    timeframe = 'turbo' # turbo / binary
    old = 0

elif config['op_binario'] == 'S' and config['op_digital'] == 'N' and config['op_binario_turbo'] == 'N': # BINARIO
    tipo = 'live-deal-binary-option-placed' # live-deal-binary-option-placed / live-deal-digital-option
    timeframe = 'binary' # turbo / binary
    old = 0   
    

# Captura o Payout
if config['op_digital'] == 'S' and config['op_binario'] == 'N':
    config['payout'] = float(payout(config['paridade'], 'digital', int(config['timeframe'])) / 100)
elif config['op_binario'] == 'S' and config['op_digital'] == 'N' and config['op_binario_turbo'] == 'S': # BINARIO
    config['payout'] = float(payout(config['paridade'], 'turbo', int(config['timeframe'])) / 100)
elif config['op_binario'] == 'S' and config['op_digital'] == 'N' and config['op_binario_turbo'] == 'N': # BINARIO
    config['payout'] = float(payout(config['paridade'], 'binary', int(config['timeframe'])) / 100)


API.subscribe_live_deal(tipo, config['paridade'], timeframe, 10)

while True: #CONFIG DA COPY
    trades = API.get_live_deal(tipo, config['paridade'], timeframe)
    
    if len(trades) > 0 and old != trades[0]['user_id'] and trades[0]['amount_enrolled'] >= float(config['valor_minimo']):
        ok = True
        
        # Correcao de bug em relacao ao retorno de datas errado
        res = round( time.time() - datetime.timestamp( timestamp_converter(trades[0]['created_at'] / 1000, 2) ), 2)
        ok = True if res <= int(config['filtro_diferenca_sinal']) else False
        
        if len(filtro_top_traders) > 0:
            if trades[0]['user_id'] not in filtro_top_traders:
                ok = False
        
        if ok:
            # Dados sinal
            print('\n')
            print('ID Trader:',trades[0]['user_id'])
            print('Nome/Pais:',trades[0]['name'],'[',trades[0]['flag'],']')
            print('Data da Operação:', timestamp_converter(trades[0]['created_at'] / 1000) )  
            print('Paridade:', config['paridade'])
            if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                print('Direcao:', trades[0]['instrument_dir'])
            elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO    
                print('Direcao:', trades[0]['direction'])    
            print('Valor Entrada:',trades[0]['amount_enrolled'])
            print('\n')
            print('Aguardando Resultado |' , Fore.GREEN + 'Sua Entrada:', Fore.GREEN + (config['valor_entrada']), Fore.YELLOW + '| Paridade:', Fore.YELLOW + (config['paridade']), Fore.YELLOW + '|', end='')
         

        # Configuração Primeira Entrada
        if config['inverter_sinal'] == 'S': # INVERTER SINAL
            
            if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                if trades[0]['instrument_dir'] == 'put':
                    inverter = 'call'
                elif trades[0]['instrument_dir'] == 'call':
                    inverter = 'put'
                resultado,lucro,stop = entradas(config, config['valor_entrada'], inverter, int(config['timeframe']))
            elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
                if trades[0]['direction'] == 'put':
                    inverter = 'call'
                elif trades[0]['direction'] == 'call':
                    inverter = 'put'    
                resultado,lucro,stop = entradas(config, config['valor_entrada'], inverter, int(config['timeframe']))
            if resultado == 'win':
                    print(Fore.GREEN + ' Resultado: WIN |', Fore.GREEN + 'Lucro:', Fore.GREEN + str(lucro))
                    print('=============================================================================================')
                    print(Fore.GREEN + '                               Stop Win:', Fore.GREEN + str(config['stop_win']) ,'  |  ', Fore.RED + 'Stop Loss:' , Fore.RED + str(config['stop_loss']))
                    print('=============================================================================================')
            elif resultado == 'loss':
                    print(Fore.RED + ' Resultado: LOSS |', Fore.RED + 'Lucro: -', Fore.RED + str(lucro))
                    print('=============================================================================================')
                    print(Fore.GREEN + '                               Stop Win:', Fore.GREEN + str(config['stop_win']) ,'  |  ', Fore.RED + 'Stop Loss:' , Fore.RED + str(config['stop_loss']))
                    print('=============================================================================================')
            else:
                    print(Fore.YELLOW + 'ERRO AO REALIZAR A ENTRADA')
                    print('=============================================================================================')
                    print(Fore.GREEN + '                               Stop Win:', Fore.GREEN + str(config['stop_win']) ,'  |  ', Fore.RED + 'Stop Loss:' , Fore.RED + str(config['stop_loss']))
                    print('=============================================================================================')
            if stop:
                if resultado == 'win':
                    print(Fore.GREEN + 'Stop WIN Batido!')
                else:
                    print(Fore.RED + 'Stop LOSS Batido!')
                sys.exit()
              
        
            
            # Configuração Martingale
            if resultado == 'loss' and config['martingale'] == 'S':
                valor_entrada = martingale('auto', float(config['valor_entrada']), float(config['payout']))
                for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):
                    
                    print('   MARTINGALE NIVEL '+str(i+1)+'..', end='')
                    if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                        if trades[0]['instrument_dir'] == 'put':
                            inverter = 'call'
                        elif trades[0]['instrument_dir'] == 'call':
                            inverter = 'put'
                        resultado,lucro,stop = entradas(config, valor_entrada, inverter, int(config['timeframe']))
                    elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO    
                        if trades[0]['direction'] == 'put':
                            inverter = 'call'
                        elif trades[0]['direction'] == 'call':
                            inverter = 'put'    
                        resultado,lucro,stop = entradas(config, valor_entrada, inverter, int(config['timeframe']))
                    if resultado == 'win':
                        print(Fore.GREEN + ' Resultado: WIN | ', Fore.GREEN + 'Lucro:', Fore.GREEN + str(lucro))
                        print('=======================================================================================================')
                    if resultado == 'loss':
                        print(Fore.RED + ' Resultado: LOSS | ', Fore.RED + 'Lucro: - ', Fore.RED + str(lucro))
                        print('=======================================================================================================')
                    if stop:
                        if resultado.upper() == 'win':
                            print(Fore.GREEN + 'Stop WIN Batido!')
                        else:
                            print(Fore.RED + 'Stop Loss Batido!')
                        sys.exit()
                    
                    if resultado == 'win':
                        break
                    else:
                        valor_entrada = martingale('auto', float(valor_entrada), float(config['payout']))
                        
            elif resultado == 'loss' and config['sorosgale'] == 'S': # Configuração SorosGale
                
                if float(config['valor_entrada']) > 5:
                    
                    lucro_total = 0
                    lucro = 0
                    perca = float(config['valor_entrada']) 
                    # Nivel
                    for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):
                        
                        # Mao
                        for i2 in range(2):
                        
                            if lucro_total >= perca:
                                break
                        
                            print('   SOROSGALE NIVEL '+str(i+1)+' | MAO '+str(i2+1)+' | ', end='')
                            
                            # Entrada
                            if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                                if trades[0]['instrument_dir'] == 'put':
                                    inverter = 'call'
                                elif trades[0]['instrument_dir'] == 'call':
                                    inverter = 'put'
                                resultado,lucro,stop = entradas(config, (perca / 2)+lucro, inverter, int(config['timeframe'])) 
                            elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
                                if trades[0]['direction'] == 'put':
                                    inverter = 'call'
                                elif trades[0]['direction'] == 'call':
                                    inverter = 'put'    
                                resultado,lucro,stop = entradas(config, (perca / 2)+lucro, inverter, int(config['timeframe'])) 
                            if resultado == 'win':
                                print(Fore.GREEN + ' Resultado: WIN | ', Fore.GREEN + 'Lucro:', Fore.GREEN + str(lucro))
                                print('=======================================================================================================')
                            else:
                                print(Fore.RED + ' Resultado: LOSS | ', Fore.RED + 'Lucro: - ', Fore.RED + str(lucro))
                                print('=======================================================================================================')
                            if stop:
                                if resultado.upper() == 'win':
                                    print(Fore.GREEN + 'Stop WIN Batido!')
                                else:
                                    print(Fore.RED + 'Stop Loss Batido!')
                                sys.exit()
                            
                            if resultado == 'win':          
                                lucro_total += lucro
                            else:
                                lucro_total = 0
                                perca += perca / 2                              
                                break                       
            
        elif config['inverter_sinal'] == 'N': # NÃO INVERTER SINAL    
            if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                resultado,lucro,stop = entradas(config, config['valor_entrada'], trades[0]['instrument_dir'], int(config['timeframe']))
            elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
                resultado,lucro,stop = entradas(config, config['valor_entrada'], trades[0]['direction'], int(config['timeframe']))
            if resultado == 'win':
                    print(Fore.GREEN + ' Resultado: WIN |', Fore.GREEN + 'Lucro:', Fore.GREEN + str(lucro))
                    print('=============================================================================================')
                    print(Fore.GREEN + '                               Stop Win:', Fore.GREEN + str(config['stop_win']) ,'  |  ', Fore.RED + 'Stop Loss:' , Fore.RED + str(config['stop_loss']))
                    print('=============================================================================================')
            elif resultado == 'loss':
                    print(Fore.RED + ' Resultado: LOSS |', Fore.RED + 'Lucro: -', Fore.RED + str(lucro))
                    print('=============================================================================================')
                    print(Fore.GREEN + '                               Stop Win:', Fore.GREEN + str(config['stop_win']) ,'  |  ', Fore.RED + 'Stop Loss:' , Fore.RED + str(config['stop_loss']))
                    print('=============================================================================================')
            else:
                    print(Fore.YELLOW + 'ERRO AO REALIZAR A ENTRADA')
                    print('=============================================================================================')
                    print(Fore.GREEN + '                               Stop Win:', Fore.GREEN + str(config['stop_win']) ,'  |  ', Fore.RED + 'Stop Loss:' , Fore.RED + str(config['stop_loss']))
                    print('=============================================================================================')
            if stop:
                if resultado == 'win':
                    print(Fore.GREEN + 'Stop WIN Batido!')
                else:
                    print(Fore.RED + 'Stop LOSS Batido!')
                sys.exit()
              
        
            
            # Configuração Martingale
            if resultado == 'loss' and config['martingale'] == 'S':
                valor_entrada = martingale('auto', float(config['valor_entrada']), float(config['payout']))
                for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):
                    
                    print('   MARTINGALE NIVEL '+str(i+1)+'..', end='')
                    if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                        resultado,lucro,stop = entradas(config, valor_entrada, trades[0]['instrument_dir'], int(config['timeframe']))
                    elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO    
                        resultado,lucro,stop = entradas(config, valor_entrada, trades[0]['direction'], int(config['timeframe']))
                    if resultado == 'win':
                        print(Fore.GREEN + ' Resultado: WIN | ', Fore.GREEN + 'Lucro:', Fore.GREEN + str(lucro))
                        print('=======================================================================================================')
                    if resultado == 'loss':
                        print(Fore.RED + ' Resultado: LOSS | ', Fore.RED + 'Lucro: - ', Fore.RED + str(lucro))
                        print('=======================================================================================================')
                    if stop:
                        if resultado.upper() == 'win':
                            print(Fore.GREEN + 'Stop WIN Batido!')
                        else:
                            print(Fore.RED + 'Stop Loss Batido!')
                        sys.exit()
                    
                    if resultado == 'win':
                        break
                    else:
                        valor_entrada = martingale('auto', float(valor_entrada), float(config['payout']))
                        
            elif resultado == 'loss' and config['sorosgale'] == 'S': # Configuração SorosGale
                
                if float(config['valor_entrada']) > 5:
                    
                    lucro_total = 0
                    lucro = 0
                    perca = float(config['valor_entrada']) 
                    # Nivel
                    for i in range(int(config['niveis']) if int(config['niveis']) > 0 else 1):
                        
                        # Mao
                        for i2 in range(2):
                        
                            if lucro_total >= perca:
                                break
                        
                            print('   SOROSGALE NIVEL '+str(i+1)+' | MAO '+str(i2+1)+' | ', end='')
                            
                            # Entrada
                            if config['op_digital'] == 'S' and config['op_binario'] == 'N':
                                resultado,lucro,stop = entradas(config, (perca / 2)+lucro, trades[0]['instrument_dir'], int(config['timeframe'])) 
                            elif config['op_binario'] == 'S' and config['op_digital'] == 'N': # BINARIO
                                resultado,lucro,stop = entradas(config, (perca / 2)+lucro, trades[0]['direction'], int(config['timeframe'])) 
                            if resultado == 'win':
                                print(Fore.GREEN + ' Resultado: WIN | ', Fore.GREEN + 'Lucro:', Fore.GREEN + str(lucro))
                                print('=======================================================================================================')
                            else:
                                print(Fore.RED + ' Resultado: LOSS | ', Fore.RED + 'Lucro: - ', Fore.RED + str(lucro))
                                print('=======================================================================================================')
                            if stop:
                                if resultado.upper() == 'win':
                                    print(Fore.GREEN + 'Stop WIN Batido!')
                                else:
                                    print(Fore.RED + 'Stop Loss Batido!')
                                sys.exit()
                            
                            if resultado == 'win':          
                                lucro_total += lucro
                            else:
                                lucro_total = 0
                                perca += perca / 2                              
                                break                   
            

        old = trades[0]['user_id']
    time.sleep(0.2)

API.unscribe_live_deal(tipo, config['paridade'], timeframe)

            