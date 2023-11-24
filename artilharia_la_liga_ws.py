from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import json
from unidecode import unidecode


#---------------------------------------------------------
#config_default
url = 'https://pt.besoccer.com/competicao/rankings/la_liga/2024/maiores-artilheiros'
navegador = webdriver.Chrome()
navegador.set_window_size(1200, 1000)


#---------------------------------------------------------
#filtro das informações
navegador.get(url)
sleep(2)

#--------------------------------------------
artilheiros = {}

print("Iniciando artilharia_la_liga_ws..")

def capture_artilheiros():

    sleep(2)
    # Encontrar o número total de artilheiros
    total_artilheiros = len(navegador.find_elements(By.XPATH, '//*[@id="ranking_table"]/tr'))




    list_name_artilheiros = []
    list_time_artilheiro = []
    list_gols_artilheiro = []
    # Iterar sobre todos os artilheiros
    for i in range(1, total_artilheiros + 1):
        xpath_artilheiro = f'//*[@id="ranking_table"]/tr[{i}]/td[2]/a/p/b'                      
        xpath_time = f'//*[@id="ranking_table"]/tr[{i}]/td[2]/a/span'
        xpath_gols = f'//*[@id="ranking_table"]/tr[{i}]/td[3]/b'

        nome_artilheiro = navegador.find_element(By.XPATH, xpath_artilheiro).text
        nome_time = navegador.find_element(By.XPATH, xpath_time).text
        qtd_gols = navegador.find_element(By.XPATH, xpath_gols).text

        list_name_artilheiros.append(nome_artilheiro)
        list_time_artilheiro.append(nome_time)
        list_gols_artilheiro.append(qtd_gols)


    sleep(2)
    for i in range(total_artilheiros):
       
        artilheiros[f'{i+1}'] = {
            "jogador" : list_name_artilheiros[i],
            "time" : list_time_artilheiro[i],
            "gols" : list_gols_artilheiro[i]
        }
    print("Artilheiros la_liga capturados com sucesso!")

def close_pop_up():
    btn_proxima = navegador.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
    print('pop up fechado')


def save_json():


    artilharia = "save\\artilharia_la_liga.json"

    with open(artilharia, "w") as arquivo_json:
        json.dump(artilheiros, arquivo_json)

    print('Artilharia la_liga salva no arquivo json!')


close_pop_up()
capture_artilheiros()
save_json()