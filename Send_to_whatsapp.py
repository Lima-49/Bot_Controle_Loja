from genericpath import isdir
from selenium import webdriver
from selenium.webdriver.common import actions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd 
import os 
import sys
from datetime import date, datetime
import chromedriver_autoinstaller
import time
import base64
import configparser
from pathlib import Path

## Paths ##
session_path = os.path.join(os.path.expanduser('~'), 'wpp_session')
path = os.path.join(os.getcwd(), 'Download')
path_download = os.path.join(path, "Lista Cartão Fidelidade.xlsx")
output_path = Path(__file__).parent
asseths_path = output_path / Path("./config.txt")

## Functions ##
def clicking(path, element='elemento selecionado', refresh=False, by=By.XPATH, limit=3):
    """
    * path: caminho do elemento que será encontrado na página. Pode ser um xpath, um ID, um name e etc;
    * element: nome do elemento que será encontrado na página. Esse parâmetro tem como finalidade unicamente para melhor depuração. Pode ser omitido;
    * refresh: default False - tem como objetivo atualizar a página para tentar clicar no elemento. Utilizado para clicar em arquivos em listas de query;
    * by: default XPATH - método utilizado para localizar o elemento, como XPATH, ID, NAME, CSS_SELECTOR e etc;
    * limit: default 3 - quantidade de vezes que a função irá tentar clicar no elemento. Por padrão, cada tentativa leva 20 segundos. Se o elemento não for encontrado, retornará None;
    """


    if limit == 0:
        return None


    elif refresh:
        driver.refresh()

    try:
        object = driver.find_element(by, path)
        actions = ActionChains(driver)
        actions.move_to_element(object).perform()
        
        found_element = driver.find_element(by, path)
        print(f">>>Sucesso {element}>>>")

    except:
        print(f"<<<Erro ao {element}, tentando novamente>>>")
        found_element = clicking(element=element, path=path, refresh=refresh, by=by, limit=limit - 1)


    return found_element

def create_driver(download_dir=None, headless=False):
    chrome_options = Options()

    if headless:
        chrome_options.headless=True

    if download_dir is not None:
        download_dir=str(download_dir)

    preferences = {"download.default_directory": download_dir,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True}
                   
    #chrome_options.add_argument("user-data-dir=C:\\Users\\vitor\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument(f"user-data-dir={session_path}")
    chrome_options.add_experimental_option("prefs", preferences)
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(20)

    return driver

def error(e):
    print("Apresentou erro, gravando o erro")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    path_erro = r'\\branas06av3-nrd\LAR_BRA_DIGITAL_F\Facens\Logs'
    #path_erro = r"C:\Users\IWX1057086\Documents\Programas\TIM RPA\log"
    today = date.today()
    name = str(fname) + '_' + str(today) + '.txt'
    arquivo = open(path_erro + '\\' + name, 'w')
    arquivo.write(str(fname) + "\n")
    arquivo.write(str(e) + "\n")
    arquivo.write(str(exc_type) + "\n")
    arquivo.write(str(exc_tb.tb_lineno) + "\n")
    arquivo.close()
   
def decodeLogin(path):
    
    #Abrindo o arquivo de configurações
    arq = configparser.RawConfigParser()
    arq.read(path)

    #Pegando os dados do arquivo
    num = arq.get('RECEIVER', 'number')
    num = base64.b64decode(num)
    
    return str(num, 'utf-8')

#Acces the whatsapp page
driver = create_driver(download_dir=None, headless=False)
driver.get('http://web.whatsapp.com/')

#If session folder doesn't exist, 
if not os.path.exists(session_path):
    
    #Wait the user read the QR code
    while len(driver.find_element(By.ID, 'side').text) < 1:
        time.sleep(1)

#Decode the receiver number 
receiver_number = decodeLogin(asseths_path)

#Go directly to the receiver chat
driver.get(f'http://web.whatsapp.com/send?phone={receiver_number}')

#Send the downloaded file to te right receiver
clicking(element='Click at the attached button', path="//div[@title='Anexar']").click()
clicking(element='Send the downloaded file', path="//input[@type='file']").send_keys(path_download)
clicking(element='Click at send file', path="//div[@aria-label='Enviar']").click()

print("File sended with success")
driver.quit()