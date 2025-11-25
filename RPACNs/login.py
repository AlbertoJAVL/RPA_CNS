from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from utileria import *
from os import system

import pyautogui as pg

def loginSiebel(username, password):

    try:

        # Cerrado de otros Chrome
        # system("taskkill /f /im chrome.exe")
        # system("taskkill /f /im chrome.exe")
        # system("taskkill /f /im chrome.exe")

        # URL de acceso 
        url = 'https://crm.izzi.mx/siebel/app/ecommunications/esn?SWECmd=Start'

        
        # Configuracion para no descargar web driver (Solo funciona con windows 10)
        opciones = webdriver.ChromeOptions()
        opciones.add_experimental_option('excludeSwitches', ['enable-logging'])
        opciones.add_experimental_option("excludeSwitches", ['enable-automation'])
        opciones.add_argument('--disable-gpu') 
        opciones.add_argument('--ignore-certificate-errors') 
        opciones.add_argument('--window-size=1024,768') 


        # Inicializacion del driver
        driver = webdriver.Chrome(options=opciones)
        driver.maximize_window()
        try: driver.get(url)
        except: print('#######################\n ERROR EJECUCION DRIVER \n#######################'); driver.close()


        act = webdriver.ActionChains(driver)

        # Espera de carga
        contador = 0
        while True:

            sleep(1)
            page_title = driver.title
            if 'Siebel Communications' in page_title: sleep(5); break
            elif 'PRIVACY' in page_title.upper() or 'PRIVACIDAD' in page_title.upper():

                print('♀ Error de Privacidad')
                sleep(3)
                driver.find_element(By.ID, "details-button").click()
                sleep(2)
                act.key_down(Keys.TAB)
                sleep(2)
                driver.find_element(By.ID, "proceed-link").click()
                print('♀ Error de Privacidad CERRADO')

            else:
                contador += 1
                if contador == 30: return driver, False

        
        try:
            
            # Usuario
            inputUsuario = driver.find_element(By.XPATH, "//input[@title='ID de usuario']")
            inputUsuario.click()
            sleep(1.5)
            inputUsuario.send_keys(username)

            # Contraseña
            inputPassword = driver.find_element(By.XPATH, "//input[@title='Contraseña']")
            inputPassword.click()
            sleep(1.5)
            inputPassword.send_keys(password)

            # LogIn (Click)
            driver.find_element(By.XPATH, "//a[@un='LoginButton']").click()
            # sleep(1000)

            # Validación de acceso correcto
            try:

                status_bar = driver.find_element(By.ID, "statusBar")
                
                act.click(status_bar)
                act.double_click(status_bar).perform()
                
                texto = my_copy(driver)
                if 'incorrecta' in texto:
                    print('CLAVES INVALIDAS')
                    driver.close()
                    return driver, False
                
            except: 
                print(f'→ Inicio de Sesion Exitoso: {username} ←')
                sleep(10)
                return driver, True

        except: 
            print('♀ Error Ingreso Credenciales')
            return driver, False
        
    except Exception as e:
        print(e)
        print('♀ Error Funcion Login')
        return False, False