#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from ctypes import sizeof
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
def int_1_byte(data):
    entireData = bytearray()
    for i in data:
        intByte = (i).to_bytes(1, byteorder ='big')
        entireData.append(intByte[0])
    return entireData

def handhsake():
    hand = [0, 0, 0, 255, 0, 255, 0, 0, 0, 0]
    handshake = int_1_byte(hand)
    return handshake

def makeHead(arquivo, tipo):
    """Se tipo = 0 é handshake se tipo != 0 é parte do arquivo"""
    tamanhoBytes = len(arquivo)
    print(f"O arquivo tem {tamanhoBytes} bytes" )
    qtdPayloads = math.ceil(tamanhoBytes/114)
    print(f"Quantidade de Pacotes: {qtdPayloads}")
    tamUltimoPacote = tamanhoBytes - 114*(qtdPayloads-1)
    print(f"Tamanho do último pacote: {tamUltimoPacote}")
    pacoteAtual = 0

<<<<<<< HEAD
    heads = [0, tamanhoBytes, qtdPayloads, tamUltimoPacote,pacoteAtual,0, 0, 255, 0, 0]
=======

    
    heads = [tamanhoBytes, package_number, qtdPayloads,last_payload_size,0,0,0,0,0,0]
>>>>>>> d70430db2c3eeaa58021739984b1ccb7a2d57be2

    return heads
    

def makePacote(head,payload,eop):
    pacote = head + payload + eop
    return pacote

eop = [0,255,0,0]

def eopMake():
    EOP = int_1_byte(eop)
    return EOP

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
        print("Confirmação Recbida")
        headHandshake, lenteste = com1.getData(10)
        print(headHandshake)
        payloadHandshake, lenteste  = com1.getData(4)
        print(payloadHandshake)
        eopHandshake, lenteste = com1.getData(4)
        print(eopHandshake)
        print("Handshake recebido: ", (headHandshake+payloadHandshake+eopHandshake))
        #aqui você deverá gerar os imagemBytess a serem transmitidos. 
        #seus imagemBytess a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os imagemBytess a serem enviados.

        if  payloadHandshake == b'\x00\x00\xff\xff':
            print("----------------")
            print("Confirmado")
        else: 
            print("FALHA EM HANDSHAKE")
            quit()
        
        imageR = "./imgs/image.png"

        print("Carregando imagem para transmissão")
        print(".{}".format(imageR))
        print("---------------------------")
        imagem = bytearray(open("./imgs/image.png", "rb").read())
        print("Imagem Transformada em bytes")
        headInt = makeHead(imagem,1)
        print(headInt)
        eopa = eopMake()
        time.sleep(2)
        for i in range(0, headInt[2]):
            payload = imagem[:114]
            del imagem[:114]
            print("Payload feito")
            headInt[1] = len(payload)

            print("-------------------------")
            print("número do pacote: {}".format(headInt[4]))
            time.sleep(0.5)
            if headInt[2] == headInt[4]+1:
                headInt[5] = headInt[3]
            else:
                headInt[5] = 114
            headByte = int_1_byte(headInt)
            print(headInt)
            headInt[4] += 1
            print(headByte)
            pacote = makePacote(headByte, payload, eopa)
            print(pacote)
            com1.sendData(pacote)

            print("-----------------")
            print("Pacote enviado: ", len(pacote))
            print("-----------------")
            
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
