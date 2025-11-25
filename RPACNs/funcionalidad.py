from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.keys import Keys
from datetime import datetime, date, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from rutas import *

import  pyautogui  as pg
import autoit as it

def obtencionColumna(driver, nombreColumna, path, path2 = False):

    buscandoColumna = True
    contador = 0

    while buscandoColumna:

        try:
            contador += 1
            nameColumna2 = 'False'
            pathF = path.replace('{contador}', str(contador))

            try:
                nameColumna = driver.find_element(By.XPATH, pathF)
                nameColumna = driver.execute_script("return arguments[0].textContent;", nameColumna)
                print(f'paht1: {nameColumna}')
            except: nameColumna = 'False'

            if path2 != False:
                try:
                    pathF2 = path2.replace('{contador}', str(contador))
                    nameColumna2 = driver.find_element(By.XPATH, pathF2)
                    nameColumna2 = driver.execute_script("return arguments[0].textContent;", nameColumna2)
                except: nameColumna2 = 'False'
                print(f'path2: {nameColumna2}')

            if nombreColumna in nameColumna or nombreColumna in nameColumna2: return str(contador)
            else: 
                if contador == 100: return False
        
        except Exception as e : print(str(e)); return False

def cargandoElemento(driver, elemento, atributo, valorAtributo, path = False):

    cargando = True
    contador = 0

    while cargando:

        sleep(1)
        try: 
            print('Esperando a que el elemento cargue')
            if path == False: 
                driver.find_element(By.XPATH, f"//{elemento}[@{atributo}='{valorAtributo}']").click()
                return True, ''
            else:
                driver.find_element(By.XPATH, path).click()
                return True, ''
        
        except:

            try:
                print('Validando posible warning')
                contador += 1
                sleep(1)
                alert = Alert(driver)
                alert_txt = alert.text
                print(f'♦ {alert_txt} ♦')
                if 'Cuenta en cobertura FTTH' in alert_txt: 
                    alert.accept()
                    print('aqui')
                    return True, ''
                else: return False, f'Inconsistencia Siebel: {alert_txt}'
            except:
                print('Pantalla Cargando')
                if contador == 60: return False, 'elemento no carga'

def home(driver): driver.find_element(By.XPATH, "//a[@title='Pantalla Única de Consulta']").click()


# Función de apertura para generar validaciones
def inicio(driver, cuenta, solucionVal, comentarioVal):

    try:

        pathEstadoCN = '/html/body/div[1]/div/div[5]/div/div[8]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/form/div/span/div[3]/div/div/table/tbody/tr[4]/td[5]'
        pathPickListEstadoCN = '/html/body/div[1]/div/div[5]/div/div[8]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/form/div/span/div[3]/div/div/table/tbody/tr[4]/td[5]/div/span'
        pathOpcCerradoCN = '/html/body/div[1]/div/div[5]/div/div[8]/ul[16]/li[7]/div'

        
        print('→ Buscando Cuenta')

        # Pantalla Consulta (Click)
        lupa_busqueda_cuenta, resultado = cargandoElemento(driver, 'a', 'title', 'Pantalla Única de Consulta')
        if lupa_busqueda_cuenta == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'

        # Buscando Elemento
        lupa_busqueda_cuenta, resultado = cargandoElemento(driver, 'button', 'title', 'Pantalla Única de Consulta Applet de formulario:Consulta')
        if lupa_busqueda_cuenta == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        lupa_busqueda_cn, resultado = cargandoElemento(driver, 'input', 'aria-label', 'Numero Cuenta')
        if lupa_busqueda_cn == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'

        # Ingreso Cuenta
        input_busqueda_cuenta = driver.find_element(By.XPATH, "//input[@aria-label='Numero Cuenta']")
        input_busqueda_cuenta.send_keys(cuenta)
        input_busqueda_cuenta.send_keys(Keys.RETURN)
        print('♦ Cuenta Ingresada ♦')

        # Cargando Cuenta
        cargaPantalla, resultado = cargandoElemento(driver, '', '', '', path= "//*[contains(@aria-label,'SALDO VENCIDO')]")
        if cargaPantalla == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        print('♥ Cuenta OK! ♥')

        # Inicio de Generacion CN
        # Buscando Creacion CN
        lupa_busqueda_cuenta, resultado = cargandoElemento(driver, 'button', 'title', 'Casos de Negocio Applet de lista:Nuevo')
        if lupa_busqueda_cuenta == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        sleep(5)


        # Llenado de CN
        # Buscando Categoria
        elementoActivo, resultado = cargandoElemento(driver, 'input', 'aria-label', 'Categoria')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        categoria = driver.find_element(By.XPATH, "//input[@aria-label='Categoria']")
        categoria.send_keys('COBRANZA')
        categoria.send_keys(Keys.RETURN)

        # Buscando Motivo
        elementoActivo, resultado = cargandoElemento(driver, 'input', 'aria-label', 'Motivo')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        motivo = driver.find_element(By.XPATH, "//input[@aria-label='Motivo']")
        motivo.send_keys('GESTORIA DE COBRANZA')
        motivo.send_keys(Keys.RETURN)

        # Buscando Sub Motivo
        elementoActivo, resultado = cargandoElemento(driver, 'input', 'aria-label', 'Submotivo')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        subMotivo = driver.find_element(By.XPATH, "//input[@aria-label='Submotivo']")
        subMotivo.send_keys('COBRANZA EXTERNA')
        subMotivo.send_keys(Keys.RETURN)

        # Buscando Solucion
        elementoActivo, resultado = cargandoElemento(driver, 'input', 'aria-label', 'Solución')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        solucion = driver.find_element(By.XPATH, "//input[@aria-label='Solución']")
        solucion.send_keys(solucionVal)
        solucion.send_keys(Keys.RETURN)

        # PAGO CON PROMOCION
        # PAGO COMPLETO

        # Buscando Comentario
        elementoActivo, resultado = cargandoElemento(driver, 'textarea', 'aria-label', 'Comentarios')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        comentarios = driver.find_element(By.XPATH, "//textarea[@aria-label='Comentarios']")
        comentarios.send_keys(comentarioVal)

        # Buscando Motivo Cierre
        elementoActivo, resultado = cargandoElemento(driver, 'input', 'aria-label', 'Motivo del Cierre')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'
        
        motivoCierre = driver.find_element(By.XPATH, "//input[@aria-label='Motivo del Cierre']")
        motivoCierre.send_keys('RAC INFORMA Y SOLUCIONA')
        motivoCierre.send_keys(Keys.RETURN)

        # Obtencion de CN Generado
        cnGenerado = driver.find_element(By.XPATH, "//a[@name='SRNumber']")
        cnGenerado = driver.execute_script("return arguments[0].textContent;", cnGenerado)
        print(f'→ CN Generado: {cnGenerado}')

        # Buscando Estado CN

        try:

            driver.find_element(By.XPATH, pathEstadoCN).click()
            sleep(2)
            
            driver.find_element(By.XPATH, pathPickListEstadoCN).click()
            sleep(5)
            
            pathestadoCNOpc = '/html/body/div[1]/div/div[5]/div/div[8]/ul[17]/li[{contador}]/div'
            posicion = obtencionColumna(driver, 'Cerrado', pathestadoCNOpc)
            if posicion == False: return False, 'Inconsistencia Siebel: Elemento Estado', '-'

            driver.find_element(By.XPATH, pathestadoCNOpc.replace('{contador}', posicion)).click()
            sleep(5)
        
        except: return False, 'Inconsistencia Siebel: Elemento Estado', '-'

        # Guardar CN
        elementoActivo, resultado = cargandoElemento(driver, 'button', 'aria-label', 'Casos de negocio Applet de formulario:Guardar')
        if elementoActivo == False: 
            if resultado == 'elemento no carga': resultado = 'Registro Pendiente'
            return False, resultado, '-'

        print('→ Fin Creacion CN')
        sleep(10)


        return True, 'Completado', cnGenerado

    except Exception as e: print(e); return False, 'Error FI', '-'
