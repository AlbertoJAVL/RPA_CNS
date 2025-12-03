from os import environ, path, remove, listdir
import apiCyberHubOrdenes as api
from login import loginSiebel
from shutil import rmtree
from funcionalidad import *
import socket
import os

def delTemporales():

    temp_folder = environ['TEMP']

    try:

        temp_files = listdir(temp_folder)

        for temp_file in temp_files:
            temp_file_path = path.join(temp_folder, temp_file)

            try:
                if path.isfile(temp_file_path): remove(temp_file_path)
                elif path.isdir(temp_file_path): rmtree(temp_file_path)

            except: pass

        print('Eliminacion temporales OK!')

    except Exception as e: print('Se produjo un error al eliminar los temporales')

def main():

    # Eliminación de Temporales
    delTemporales()

    # Inicio de Sesion
    # try: credenciales = api.get_orden_servicio2()
    # except: return False
        # driver, status_logueo = loginSiebel(credenciales['procesoUser'], credenciales['procesoPassword'])
    driver, status_logueo = loginSiebel('bavila', 'Doctorgarcia@')
    if status_logueo == False: 
        print('→ LOGGIN INCORRECTO ←')
        return False

    while True:
        try: 
            apiResponse = api.get_orden_servicio()
            info = apiResponse[0]
        except: return False
        print(info)
        host = socket.gethostname()
        ip = socket.gethostbyname(host)

        if info != 'SIN INFO':


            if 'CN NORMAL' in info['proceso']:

                solucionPre = " ".join(info['solucion'].upper().split())

                if 'PROMESA DE PAGO' in solucionPre: solucion = 'PAGO COMPLETO'
                elif 'PROMESA CON PROMOCION'  in solucionPre: solucion = 'PAGO CON PROMOCION'
                else: 
                    status = 'No aplica: Solucion Invalida'
                    response = api.ajusteCerrado(
                        info['id'],
                        '-',
                        info['fechaCaptura'],
                        info['fechaCompletado'],
                        status,
                        info['cve_usuario'],
                        ip,
                        info['proceso'],
                        info['cuenta'],
                        info['fechaSubida'],
                        info['categoria'],
                        info['motivo'],
                        info['subMotivo'],
                        info['solucion'],
                        info['saldoIncobrable'],
                        info['promocion'],
                        info['ajuste'],
                        info['fechaGestion'],
                        info['tipo'],
                        info['motivoDelCliente'],
                        info['comentarios'],
                        info['cnConMotivoHeavyUser'])
                    print(response)
                    return False
                
                if solucion == 'PAGO COMPLETO': comentario = f"SALDO INCOBRABLE: {info['saldoIncobrable']}\nFECHA: {info['fechaGestion']}\n{info['tipo']}\nCLIENTE CUENTA CON PROMOCION: ({info['promocion']})"
                else: comentario = f"SALDO INCOBRABLE: {info['saldoIncobrable']}\nPROMOCION: {info['promocion']}\nAJUSTE: {info['ajuste']}\nFECHA: {info['fechaGestion']}\n{info['tipo']}"

                plantilla = {
                    'categoria' : 'COBRANZA',
                    'motivo' : 'GESTORIA DE COBRANZA',
                    'subMotivo' : 'COBRANZA EXTERNA',
                    'solucion' : solucion,
                    'comentario' : comentario,
                    'motivoCliente' : ''
                }

            elif 'CN HEAVY USER' in info['proceso']: 

                if info['cnConMotivoHeavyUser'] == None or info['cnConMotivoHeavyUser'] == '' or info['cnConMotivoHeavyUser'] == ' ':
                    status = 'No aplica: Sin CN Motivo Heavy User'
                    response = api.ajusteCerrado(
                        info['id'],
                        '-',
                        info['fechaCaptura'],
                        info['fechaCompletado'],
                        status,
                        info['cve_usuario'],
                        ip,
                        info['proceso'],
                        info['cuenta'],
                        info['fechaSubida'],
                        info['categoria'],
                        info['motivo'],
                        info['subMotivo'],
                        info['solucion'],
                        info['saldoIncobrable'],
                        info['promocion'],
                        info['ajuste'],
                        info['fechaGestion'],
                        info['tipo'],
                        info['motivoDelCliente'],
                        info['comentarios'],
                        info['cnConMotivoHeavyUser'])
                    print(response)
                    return False

                plantilla = {
                    'categoria' : 'SOLICITUD DE CANCELACION',
                    'motivo' : 'ECONOMICO',
                    'subMotivo' : 'NO PUEDE SEGUIR PAGANDO NR',
                    'solucion' : 'NO RETENIDO',
                    'comentario' : f"DX POR HEAVY USER\nVIOLACION PUA INTERNET\nCN {info['cnConMotivoHeavyUser']}",
                    'motivoCliente' : 'FOLIO DE CANCELACION'
                }

            elif 'CN AGENCIAS EXTERNAS' in info['proceso']: 

                if 'COBRANZA EXTERNA' not in info['subMotivo'] and 'RECONEXION' not in info['subMotivo']:
                    status = 'No aplica: Sub Motivo Invalido'
                    response = api.ajusteCerrado(
                        info['id'],
                        '-',
                        info['fechaCaptura'],
                        info['fechaCompletado'],
                        status,
                        info['cve_usuario'],
                        ip,
                        info['proceso'],
                        info['cuenta'],
                        info['fechaSubida'],
                        info['categoria'],
                        info['motivo'],
                        info['subMotivo'],
                        info['solucion'],
                        info['saldoIncobrable'],
                        info['promocion'],
                        info['ajuste'],
                        info['fechaGestion'],
                        info['tipo'],
                        info['motivoDelCliente'],
                        info['comentarios'],
                        info['cnConMotivoHeavyUser'])
                    print(response)
                    return False

                listadoMotivosCliente = ['IZZI 80 RET', 'IZZI 100 RET', 'IZZI 150 RET', 'IZZI 80 + IZZITV HD RET', 'IZZI 100 + IZZITV HD RET', 'IZZI 150 + IZZITV HD RET']
                
                motivoClienteOK = False
                for mC in listadoMotivosCliente:
                    if mC in info['motivoDelCliente']:
                        motivoClienteOK = True
                        break

                if motivoClienteOK == False: 
                    status = 'No aplica: Motivo Cliente NO Valido'
                    response = api.ajusteCerrado(
                        info['id'],
                        '-',
                        info['fechaCaptura'],
                        info['fechaCompletado'],
                        status,
                        info['cve_usuario'],
                        ip,
                        info['proceso'],
                        info['cuenta'],
                        info['fechaSubida'],
                        info['categoria'],
                        info['motivo'],
                        info['subMotivo'],
                        info['solucion'],
                        info['saldoIncobrable'],
                        info['promocion'],
                        info['ajuste'],
                        info['fechaGestion'],
                        info['tipo'],
                        info['motivoDelCliente'],
                        info['comentarios'],
                        info['cnConMotivoHeavyUser'])
                    print(response)
                    return False

                plantilla = {
                    'categoria' : 'COBRANZA',
                    'motivo' : 'GESTORIA DE COBRANZA',
                    'subMotivo' : info['subMotivo'].strip(),
                    'solucion' : 'RX MIGRACIÓN DE PAQUETE',
                    'comentario' : f"{info['promocion']}\n{info['ajuste']}\n{info['fechaGestion']}\n{info['tipo']}",
                    'motivoCliente' : info['motivoDelCliente'].strip()
                }

                if 'RECONEXION' in info['subMotivo']: plantilla['solucion'] = 'RX MIGRACION DE PAQUETE'

            else:
                status = 'No aplica: Tipo CN NO Detectado'
                response = api.ajusteCerrado(
                    info['id'],
                    '-',
                    info['fechaCaptura'],
                    info['fechaCompletado'],
                    status,
                    info['cve_usuario'],
                    ip,
                    info['proceso'],
                    info['cuenta'],
                    info['fechaSubida'],
                    info['categoria'],
                    info['motivo'],
                    info['subMotivo'],
                    info['solucion'],
                    info['saldoIncobrable'],
                    info['promocion'],
                    info['ajuste'],
                    info['fechaGestion'],
                    info['tipo'],
                    info['motivoDelCliente'],
                    info['comentarios'],
                    info['cnConMotivoHeavyUser'])
                print(response)
                return False

            
            plantilla['comentario'] = plantilla['comentario'].replace('/', ' ').replace('%', ' ').replace('.', ' ').replace('$', ' ').replace('_', ' ').replace('-', ' ').replace(',', ' ')
            # comentario = comentario.replace('/', ' ').replace('%', ' ').replace('.', ' ').replace('$', ' ').replace('_', ' ').replace('-', ' ').replace(',', ' ')



            resultado, valEstado, numeroCN = inicio(driver, info['cuenta'], plantilla, info['proceso'])
            print(f'→ Resultado: {str(resultado)}')
            print(f'→ Estado Generado: {valEstado}')
            print(f'→ Numero CN Generado: {numeroCN}')

            status = valEstado
            response = api.ajusteCerrado(
                    info['id'],
                    numeroCN,
                    info['fechaCaptura'],
                    info['fechaCompletado'],
                    status,
                    info['cve_usuario'],
                    ip,
                    info['proceso'],
                    info['cuenta'],
                    info['fechaSubida'],
                    info['categoria'],
                    info['motivo'],
                    info['subMotivo'],
                    info['solucion'],
                    info['saldoIncobrable'],
                    info['promocion'],
                    info['ajuste'],
                    info['fechaGestion'],
                    info['tipo'],
                    info['motivoDelCliente'],
                    info['comentarios'],
                    info['cnConMotivoHeavyUser'])
            print(response)
            if resultado == False: return False
                

        else:
            try:
                os.system('cls')
                print('Esperando mas CN')
                sleep(15)
                print('Regreso a HOME')
                home(driver)
                print('##############\n FIN DE CICLO COMPLETO \n##############')

            except Exception: return False


while True == True:
    conteo_errores = 0
    try:
        os.system(f'taskkill /f /im chrome.exe')
        os.system(f'taskkill /f /im chrome.exe')
        os.system(f'taskkill /f /im chrome.exe')

    except Exception as e: pass

    delTemporales()

    error_main = main()
    if error_main == False:
        conteo_errores = conteo_errores + 1
        print(f'conteo_errores::: {str(conteo_errores)}')
        if conteo_errores >= 5:
            delTemporales()
            os.system(f'taskkill /f /im chrome.exe')
            error_main = main()
            print('##################\n ERROR CRITICO \n##################')
            sleep(1)
