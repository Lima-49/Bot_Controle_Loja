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
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'profile', 'wpp')}")
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
   
driver = create_driver(download_dir=None, headless=False)
driver.get('http://web.whatsapp.com/')

#Tempo de espera para ler o qr code
while len(driver.find_element(By.ID, "side").text) < 1:
    time.sleep(1)


