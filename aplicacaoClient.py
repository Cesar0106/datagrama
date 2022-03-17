#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from ctypes import sizeof
from http.cookiejar import MozillaCookieJar
from enlace import *
import numpy as np
import time
import random
import math

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "ACM0"                  # Windows(variacao de)
def transformaInt(data):
    entireData = bytearray()
    for i in data:
        new_data_byte = (i).to_bytes(1, byteorder ='big')
        entireData.append(new_data_byte[0])
    return entireData

def handhsake():
    hand = [0, 0, 0, 255, 0, 255, 0, 0, 0]
    handshake = transformaInt(hand)
    return handshake

def makeHead(arquivo, tipo_mensagem):
    """
    b0 = tipo de mensagem
    b1 = tamanho do arquivo
    b2 = Total de pacotes
    b3 = numero do payload atual
    b4 = tamanho do payload atual
    """
    tamanhoBytes = len(arquivo)
    print(f"O arquivo tem {tamanhoBytes} bytes" )
    i = 0
    qtdPayloads = math.ceil(tamanhoBytes/114)
    print(f"Quantidade de Pacotes: {qtdPayloads}")
    #last_payload_size = len(tamanhoBytes) - 114 * (qtdPayloads-1)
    last_payload_size = 0
    package_number = 0


    
    heads = [tamanhoBytes, package_number, qtdPayloads,last_payload_size,0,0,0,0,0,0]

    return heads
    
def data(arquivo):
    data_a = transformaInt(arquivo)
    return arquivo

def pacote(head,payload,eop):
    pacote = head + payload + eop
    return pacote

eop = [0,255,0,0]

def eopMake():
    EOP = transformaInt(eop)
    return EOP
"""
def makePayload(arquivo, tipo):
    tamanhoBytes = len(arquivo)
    x = 0
    payloads = []
    contador = 0
    eop = b"\xFF"b"\xFF"b"\xFF"b"\xFF"
    heads = makeHead(arquivo, tipo)

    while x < len(heads[3]):
        payload = []
        i = 0
        z = 0
        while z <= 4:
            payload.append(heads[z+(x*4)])
            z +=1
        while i < int.from_bytes(heads[4], byteorder="big"):
            payload.append(arquivo[i])
            i += 1
        payload.append(eop)
        contador += (i - 1)
        payloads.append(payload)
        x += 1
    return payloads
"""

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        start_time = time.time()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        hand = [0, 0, 0, 255, 0, 255, 0, 0, 0]

        arquivoPrincipal = 1
        print("Enviando Handshake")
        handshake1 = handhsake()
        eopInicio = eopMake()
        primeiro = handshake1 + eopInicio
        if com1.enable() == True:
            print("Comunicação Aberta")
        com1.sendData(primeiro)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        #Criando e enviando Handshake
        #Tipos:
        inicio = time.time()
        print("------------------------------")
        print("asdijasidasj")
        tempo = False

        while com1.rx.getIsEmpty():
                if time.time() - inicio >= 5:
                    resposta = str(input("Servidor inativo, deseja tentar novamente? S/N : "))
                    if resposta.upper() == "S":
                        com1.sendData(primeiro)
                        inicio = time.time()
                        pass
                    else:
                        print("-------------------------")
                        print("Comunicação encerrada")
                        
                        print("-------------------------")
                        com1.disable()
                        print("--- {:.4f} seconds ---".format(time.time() - start_time))
                        exit()
        confirmacaoHead, confirmacaoLen = com1.getNData(10)
        check = com1.rx.getNData(7)
        confirmacaoEop, lenEop = com1.getNdata(4)
        checkServer = check.encode()
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        if checkServer == 'tudo ok':
            print("----------------")
            print("Confirmacao: ", checkServer)
        else: 
            print("FALHA EM HANDSHAKE")
            quit()
        
        imageR = "./imgs/image.png"
        imageW = "./imgs/recebidaCopia.png"


        print("Carregando imagem para transmissão")
        print(".{}".format(imageR))
        print("---------------------------")
        with open("./imgs/image.png", "rb") as image:
            txBuffer = image.read()
        dado = np.asarray(txBuffer)

        headDado = makeHead(dado)
        headDadoArray = data(headDado)
        eopa = eopMake()

        for i in range(0, headDadoArray[2]):
            payload = dado[:114]
            del dado[:114]

            headDado[0] = len(payload)

            print("-------------------------")
            print("número do pacote: {}".format(headDado[1]))
            print("tamanho do payload atual: {}".format(headDado[0]))
            time.sleep(1)
            
            headDado[1] += 1
            headDadoArray = data(headDado)
            mensagem = pacote(headDadoArray, payload, eopa)

            com1.sendData(mensagem)

            print("-----------------")
            print("Pacote enviado: ", len(mensagem))
            print("-----------------")
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!


        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna


        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        print("--- {:.4f} seconds ---".format(time.time() - start_time))

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
