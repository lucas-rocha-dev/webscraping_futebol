from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import json
import re
from unidecode import unidecode


print('Iniciando full_premier_ws.py')
#---------------------------------------------------------
#config_default
url = 'https://ge.globo.com/futebol/futebol-internacional/futebol-ingles/'
navegador = webdriver.Chrome()
navegador.set_window_size(1200, 1000)
#---------------------------------------------------------
#capturar info do site
navegador.get(url)
elem_equipes = navegador.find_elements(By.CSS_SELECTOR, "strong.classificacao__equipes.classificacao__equipes--nome")
elem_linhas = navegador.find_elements(By.CSS_SELECTOR, "tr.classificacao__tabela--linha")
sleep(3)

#---------------------------------------------------------
#Tratamento de dados
elemento_linhas = []
elemento_linhas_indice = []
elemento_equipes = []
indice_pesonalizado = ['P', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', '%']

cont = 0
for text_linhas in elem_linhas:

  if(cont >19):
       elemento_linhas.append(text_linhas.text.split())
  
  cont = cont +1

for linha in elemento_linhas:
    # Inicialize um dicionário vazio para cada linha
    linha_com_indices = {}
    
    # Use um loop for interno para percorrer cada elemento da linha e adicionar o índice correspondente
    for indice, elemento in zip(indice_pesonalizado, linha):
        linha_com_indices[indice] = elemento
    
    # Adicione a linha com índices personalizados à lista de resultados
    elemento_linhas_indice.append(linha_com_indices)
 

for text_equipes in elem_equipes:
   elemento_equipes.append(text_equipes.text)

#------------------------------------------------------
tabela_campeonato = {}
for time, resultado_individual in zip(elemento_equipes, elemento_linhas_indice):
    tabela_campeonato[time] = resultado_individual


#-----------------------------------------------------
#SALVAR O ARQUIVO EM JSON
campeonato_json = "save\\classificacao_premier.json"

with open(campeonato_json, "w") as arquivo_json:
    json.dump(tabela_campeonato, arquivo_json)

print('classificacao_premier.json salvo com sucesso!')


#---------------------------------------

#---- ARTILHARIA WS, SEGUNDO SCRIPT ---

#---------------------------------------
artilheiros = {}

print("Iniciando artilharia_premier ws..")

def capture_artilheiros():
    sleep(2)
    seach_player_name = navegador.find_elements(By.CSS_SELECTOR, "div.jogador-nome")
    seach_player_time = navegador.find_elements(By.CSS_SELECTOR, "div.jogador-escudo")
    seach_player_points = navegador.find_elements(By.CSS_SELECTOR, "div.jogador-gols")
    sleep(2)
    filter_time = []

    for player_time in seach_player_time:
        filter_time.append(player_time.find_element(By.TAG_NAME, "img").get_attribute("alt"))


    sleep(2)
    for i in range(22):
       
        artilheiros[f'{i+1}'] = {
            "jogador" : seach_player_name[i].text,
            "time" : filter_time[i],
            "gols" : seach_player_points[i].text
        }
    print("artilharia_premier_ws.py capturados com sucesso!")

def save_json():


    artilharia = "save\\artilharia_premier.json"

    with open(artilharia, "w") as arquivo_json:
        json.dump(artilheiros, arquivo_json)

    print('artilharia_premier.json salvo com sucesso')


capture_artilheiros()
save_json()



#--------------------------------------------------------

#----WS RODADA ATUAL, TODAS RODADAS, TERCEIRA PARTE------

#---------------------------------------------------------

rodadas = {}
rodada_atual = {}
def inicio_tabela():
    for _  in range(42):
     btn_voltar = navegador.find_element(By.XPATH, '//*[@id="classificacao__wrapper"]/section/nav/span[1]').click()
     sleep(0.2)
     

def prox_tabela():
   btn_proxima = navegador.find_element(By.XPATH, '//*[@id="classificacao__wrapper"]/section/nav/span[3]').click()
   
def capture_dados():
 #capturar os elementos: Numero da Rodada, Informações(Local do jogo, data, dia da semana, hora), Time1, Time2, Gols_Time1, Gols_Time2
   numero_rodada_simplificado = 1
   for _ in range(38):
      sleep(2) 
      rodada_number = navegador.find_element(By.CSS_SELECTOR, "span.lista-jogos__navegacao--rodada").text
      
      info_local = navegador.find_elements(By.CSS_SELECTOR, "div.jogo__informacoes")  

      times = navegador.find_elements(By.CSS_SELECTOR, "span.equipes__sigla")
      
      time_1_placar = navegador.find_elements(By.CSS_SELECTOR, "span.placar-box__valor.placar-box__valor--mandante")

      time_2_placar = navegador.find_elements(By.CSS_SELECTOR, "span.placar-box__valor.placar-box__valor--visitante")
      
      jogos_rodada = []
      n_variante = 0
      
      for i in range(10):
         info_local_edit = adicionar_espacamento(info_local[i].text)

         time_a = times[i + n_variante].text
         time_b = times[i + 1 + n_variante].text
         gols_a = time_1_placar[i].text
         gols_b = time_2_placar[i].text
         data_local = info_local_edit
         
         resultado = {
            'data_local': data_local,
            'Time_A' : time_a,
            'Gols_A' : gols_a,
            'Time_B' : time_b,
            'Gols_B' : gols_b     
         }
        
         jogos_rodada.append(resultado)
         n_variante = n_variante + 1
      
      rodadas[numero_rodada_simplificado] = jogos_rodada
      numero_rodada_simplificado = numero_rodada_simplificado + 1
      prox_tabela()
     

def capture_rodada_atual():
   seach_odada_atual = navegador.find_element(By.CSS_SELECTOR, "span.lista-jogos__navegacao--rodada")
   rodada_atual_string = str(seach_odada_atual.text)

   #conversao
   texto = rodada_atual_string
   numeros = re.findall(r'\d+', texto)
   # Se houver números encontrados, pegue o primeiro número e converta para inteiro
   if numeros:
      rodada_atual['rodada_atual'] = str(numeros[0])

      print(rodada_atual)
   else:
      print("Nenhum número encontrado na string.")

def save_json():
    jogos_rodada_json = "save\\jogos_rodada_premier.json"
    with open(jogos_rodada_json, "w") as arquivo_json:
        json.dump(rodadas, arquivo_json)

    print('arquivo rodadas primier salvo com sucesso!')    
   
def save_rodada_atual():
   rodada_atual_end = "save\\rodada_atual_premier.json"
   with open(rodada_atual_end, "w") as arquivo_json:
        json.dump(rodada_atual, arquivo_json)

   print('Rodada_premier Atual salva!')    

def adicionar_espacamento(s):
   s = unidecode(s)
   padrao = r"(\d+)([a-zA-Z]+)|([a-zA-Z]+)(\d+)"
   resultado = re.sub(padrao, r"\1 \2\3 \4", s)
   return resultado


capture_rodada_atual()
save_rodada_atual()
inicio_tabela()
capture_dados()
save_json()

