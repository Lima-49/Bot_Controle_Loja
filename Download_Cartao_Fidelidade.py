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

## Funtions ##
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
    
## Main ##
driver = create_driver()

#Login
usr = 'Alineliel'
psw = 'Vitor*06'

driver.get('https://phibo.space')

clicking(element='Passando o usuario', path="/html/body/div[1]/form/div/div/input[1]").send_keys(usr)
clicking(element="Passando a senha", path='/html/body/div[1]/form/div/div/input[2]').send_keys(psw)
clicking(element='Clicando em acessar', path='/html/body/div[1]/form/div/div/button').click()

try:
    clicking(element='Tentando fechar um pop up', path='/html/body/div[1]/div[3]/div[3]/div/form/div[1]/button/span[2]').click()
except:
    pass

try:
    clicking(element='Clicando em vendas', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/a/span[2]').click()
    clicking(element='Selecionado Consulta Vendas', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/ul/li[7]/a').click()
    clicking(element='Selecionando Listar Cartão Fidelidade', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/ul/li[7]/ul/li[4]/a/span[2]').click()
except:
    
    try:
        clicking(element='Clicando em vendas', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/a/span[2]').click()
        clicking(element='Selecionado Consulta Vendas', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/ul/li[7]/a').click()
        clicking(element='Selecionando Listar Cartão Fidelidade', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/ul/li[7]/ul/li[4]/a/span[2]').click()
    except:
        clicking(element='Clicando em vendas', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/a/span[2]').click()
        clicking(element='Selecionado Consulta Vendas', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/ul/li[7]/a').click()
        clicking(element='Selecionando Listar Cartão Fidelidade', path='/html/body/div[1]/div[2]/div[1]/div[2]/form/table/tbody/tr/td[1]/div/ul/li[3]/ul/li[7]/ul/li[4]/a/span[2]').click()

df_fidelidade = pd.read_html(driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[3]/form/div[2]/div[2]/table").get_attribute('outerHTML'))[0]