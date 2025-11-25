from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

import win32clipboard as cp


def my_copy(driver):

    act = webdriver.ActionChains(driver)
    act.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

    try:

        sleep(2)
        cp.OpenClipboard()
        sleep(2)
        texto = cp.GetClipboardData()
        cp.EmptyClipboard()
        cp.CloseClipboard()

        if texto and texto != ' ' and texto != 'vacio': return texto
        else: return False

    except Exception as e:
        
        mensaje = f"HA OCURRIDO UN ERROR EN LA UTILERIA my_copy. ERROR ENCONTRADO {e}"
        print(mensaje)
        return False