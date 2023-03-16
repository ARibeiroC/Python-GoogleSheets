from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '17HDpFR6P04QhpXo0vAr8u4eXM805JniEEHUD33Ur0pY'
SAMPLE_RANGE_NAME = 'cadUsuario!A:Z'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        def getValue():
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()        
            return result

        def updateValue(cel, v):
            result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=cel, valueInputOption="USER_ENTERED", body={"values": v}).execute()    
            return result
        
        def dadosUsuario():
            col = input('COLUNA: ')
            row = input('LINHA: ')
            nomeCompleto = input('NOME COMPLETO: ')
            usuario = input('USUÁRIO: ')
            senha = input('SENHA: ')
            confirmarSenha = input('CONFIRMAR SENHA: ')

            return col, row, nomeCompleto, usuario, senha, confirmarSenha

        def cadUsuario(v, i):
            id = i
            r = dadosUsuario()

            while r[4] is r[5]:
                print('As senha não coincidem, digitar novamente')
                r[4] = input('SENHA: ')
                r[5] = input('CONFIRMAR SENHA: ')

            print(r[2])  

            while exit != '0':
                if r[0] == '' or r[1] == '':
                    for i, value in enumerate(getValue()['values']):
                        print(f' {i} | {value[0]} |{value[1]} ')
                    break
                    return print('==============================\n>>>> SISTEMA ENCERRADO!!! <<<<\n==============================')
                else:
                    data = r[0]+r[1]
                    for item in range(len(getValue()['values'])):
                        id +=1
                    v.append([id, r[2], r[3], r[4], r[5]])
                    updateValue(data, v)
                    sair = input('Deseja inserir mais dados? [(1) SIM / (0) NÃO]: ')

                    if sair == '0':
                        for i, value in enumerate(getValue()['values']):
                            print(f'| {value[0]} | {value[1]} | {value[2]} | {value[3]} | {value[4]}')
                        print('==============================\n>>>> SISTEMA ENCERRADO!!! <<<<\n==============================')
                        break
                    else:
                        continue
            

        # def editarUsuario():
        #     while sair != 'n':
        #         dadosUsuario()
        #         if dadosUsuario()[0] == '' or dadosUsuario()[1] == '':
        #             for i, value in enumerate(getValue()['values']):
        #                 print(f' {i} | {value[0]} |{value[1]} ')
        #             print('==============================\n>>>> SISTEMA ENCERRADO!!! <<<<\n==============================')
        #             break
        #         else:
        #             data = dadosUsuario()[0]+dadosUsuario()[1]
        #             id = int(dadosUsuario()[1])-1
        #             addValue.append([id, nomeCompleto, usuario, senha, confirmarSenha])
        #             updateValue(data, addValue)
        #             sair = input('Deseja inserir mais dados? [(y) SIM / (n) NÃO]: ')
        #             if exit == 'n':
        #                 for i, value in enumerate(getValue()['values']):
        #                     print(f'| {value[0]} | {value[1]} | {value[2]} | {value[3]} | {value[4]}')
        #                 print('==============================\n>>>> SISTEMA ENCERRADO!!! <<<<\n==============================')
        #                 break
        #             else:
        #                 nomeCompleto = input('NOME COMPLETO: ')
        #                 usuario = input('USUÁRIO: ')
        #                 senha = input('SENHA: ')
        #                 confirmarSenha = input('CONFIRMAR SENHA: ')

        # def consultarUsuario(id):
        #     for i, value in enumerate(getValue()['values']):
        #         if id == i:
        #             print(f'|{i}| {value[0]} | {value[1]} | {value[2]} | {value[3]} | {value[4]}')            
        #     print('==============================\n>>>> SISTEMA ENCERRADO!!! <<<<\n==============================')

        # def operacao():
        #     op = int(input('O que você deseja fazer? [CADASTRAR = 0/ALTERAR = 1/CONSULTAR = 2]'))
        #     if op == 0:
        #         cadUsuario()
        #     elif op == 1:
        #         editarUsuario()
        #     else:
        #         row = int(input('ID: '))
        #         consultarUsuario(row)
        
        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        addValue = []
        exit = '1'
        id = 0
        print('==============================\n>>>> SISTEMA INICIADO!!! <<<<\n==============================')
        while exit != '0':            
            exit = input('[CADASTRA = 1 / CONSULTAR = 2 / EDITAR = 3 / SAIR = 0]: ')
            if exit == '0':
                print('==============================\n>>>> SISTEMA ENCERRADO!!! <<<<\n==============================')
                break
            elif exit == '1':
                cadUsuario(addValue, id)
            else:
                print('DADOS INVALIDOS, INSIRA UM DOS VALORES [CADASTRA = 1 / CONSULTAR = 2 / EDITAR = 3 / SAIR = 0]: \n')



    
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()