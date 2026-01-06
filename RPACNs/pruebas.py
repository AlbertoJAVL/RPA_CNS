from funcionalidad import *
from login import *
from datetime import datetime, timedelta, date
import autoit as it
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import apiCyberHubOrdenes as api




from os import system
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")
# system("taskkill /f /im chrome.exe")


p = 'IZZI 150 con IZZITV HD RET'
listadoMotivosCliente = ['IZZI 80 RET', 'IZZI 100 RET', 'IZZI 150 RET', 'IZZI 80 CON IZZITV HD RET', 'IZZI 100 CON IZZITV HD RET', 'IZZI 150 CON IZZITV HD RET']
                
motivoClienteOK = False
for mC in listadoMotivosCliente:
    if mC in p.upper().strip().replace('+', 'CON'):
        print('Encontrado')