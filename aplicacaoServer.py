#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

"""
    Fazer o head, payload e eop atraves de funcoes que separam uma lista inicial de qualquer tamanho em varios payloads de até 124 bytes. 
    Em seguida manipular o head para enviar 10 comandos que vão descrever o pacote, como tamanho e quais bytes ler de qual maneira. Em seguida fazer a parte
    da função que gera o EOP ao final do payload. Assim que completar o diagrama enviar ele para o server e gerar as funções que vao manipular o server.


    Handshake
        Antes do início do envio da mensagem, o client deve enviar uma mensagem para verificar se o server está
        “vivo”, pronto para receber o arquivo a ser enviado. O server então deve responder como uma mensagem
        informando que ele está pronto para receber. Enquanto a mensagem não seja recebida pelo cliente, este não
        começa o envio de nada. Caso o cliente não receba a resposta do servidor dentro de 5 segundos, informando que
        está pronto para receber o arquivo, o usuário recebe uma mensagem: “Servidor inativo. Tentar novamente? S/N”. Se
        o usuário escolher “S”, outra mensagem de verificação é enviada ao server. Caso escolha não. Tudo se encerra.
        Caso o servidor responda ao cliente em menos de 5 segundos, o cliente deve iniciar a transmissão do arquivo.
    Tamanhos(EM BYTES):
        Payload - Até 114
        Head - 10
        EOP - 4 

    Estrutura:
        INICIO - APÓS O HANDSHAKE
        1 - Função que gera o datagrama(pacote)
            a - Função que manipula os bytes do arquivo ao separa-los em pacotes de até 114 com tudo que deve ser enviado e insere esses dados no payload.
            b - Função que gera o Head com os dados já inseridos no payload.
            c - Junta o head com o payload e adiciona os bytes de final de pacote(EOP).
        
        2 - Enviar o datagrama ataves de um sendData
    
        3 - Receber o datagrama no server pelo getData
        
        4 - Função que le o Head e começa a analisar o payload ate chegar no eop. 
        
        5 - Envia os dados recbidos pelo Head de volta para o client para ver se recebeu tudo corretamente

        6 - Client recebe os dados de confirmação do server e, caso esteja certo,  envia o sinal de que esta certo e em seguida envia o pacote seguinte,
        caso esteja errado avisa que está errado. No caso de estar errado envia novamente até enviar o correto.

        7 - Server recebe todos os pacotes e abre, encerrando assim a comunicação

    SEND E GET:
        Client:
        LOOP ENVIANDO PACOTES
            1 - Send - datagrama
            2 - Get - Confirmação de recebimento correto
        Server
        LOOP RECEBENDO PACOTES
            1 - Get - datagrama
            2 - Send - Leitura do Head


"""


from enlace import *
import numpy as np
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "ACM0"  
#                 # Windows(variacao de)
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
serialName = "/dev/ttyACM0"          # Ubuntu (variacao de)
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
    last_payload_size = len(tamanhoBytes) - 114 * (qtdPayloads-1)
    package_number = 0


    x = 0
    while( i < qtdPayloads):
        if tamanhoBytes - (114*i) < 114:
            x = int(tamanhoBytes - (114*i))
        else: 
            x = 114
        i += 1
    
    heads = [tamanhoBytes, package_number, qtdPayloads,last_payload_size,0,0,0,0,0]

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

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        start_time = time.time()
        loop: True
        """ Lembrar de enviar comando por comando"""

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        if com1.enable() == True:
            print("Comunicação Aberta")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        while com1.rx.getIsEmpty():
            print("------------")
            print("Esperando.....")
            time.sleep(0.2)
        clientHandhsake, lenHandshake = com1.getData(13)
        print(clientHandhsake)
        print("-------")
        print("resposta cliente recebida")
        time.sleep(0.2)

        handshakeLoop = handshake()
        eopInicio = eopMake()
        primeiro = handshakeLoop + eopInicio

        if clientHandhsake == primeiro:
            handshakea = "tudo ok"
            handshake_bytes = str.encode(handshakea)
            respostaServer = handshakeLoop + handshake_bytes + eopInicio
            com1.sendData(respostaServer)

        else: 
            erro = "--erro--"
            handshake_bytes = str.encode(erro)
            respostaServer = handshakeLoop + erro + eopInicio
            com1.sendData(respostaServer)

        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!

        
        while loop:
            head, lenHead = com1.getNData(10)
            print("......")
            print("head recebido")
            entire_head = [x for x in head]
            payload, lenPayload = com1.getData(entire_head[0])
            arquivo += payload
            time.sleep(0.3)
            eop, lenEOP = com1.getNData(4)
            



        # Encerra comunicação
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
