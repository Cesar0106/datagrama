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

def makeHead(arquivo, tipo_mensagem):
    """
    b0 = tipo de mensagem
    b1 = tamanho do arquivo
    b2 = Total de pacotes
    b3 = numero do payload atual
    b4 = tamanho do payload atual
    """
    heads = []
    tamanhoBytes = len(arquivo)
    print(f"O arquivo tem {tamanhoBytes} bytes" )
    i = 0
    qtdPayloads = math.ceil(tamanhoBytes/114)
    print(f"Quantidade de Pacotes: {qtdPayloads}")
    x = 0
    while( i < qtdPayloads):
        if tamanhoBytes - (114*i) < 114:
            x = int(tamanhoBytes - (114*i))
        else: 
            x = 114
        heads.append(tipo_mensagem.to_bytes(2, 'big'))
        heads.append(tamanhoBytes.to_bytes(2, 'big'))
        heads.append(qtdPayloads.to_bytes(2, 'big'))
        heads.append(i.to_bytes(2, 'big'))
        heads.append(x.to_bytes(2, 'big'))
        print(heads)
        i += 1
    return heads
    

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

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        hand = 0
        arquivoPrincipal = 1
        arquivoHandshake = [b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00",b"\x00"]
        print("Enviando Handshake")
        handshake = (makePayload(arquivoHandshake, hand))
        print(handshake)
        com1 = enlace(serialName)
        start_time = time.time()
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        if com1.enable() == True:
            print("Comunicação Aberta")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        #Criando e enviando Handshake
        #Tipos:
        print("len",len(handshake))
        com1.sendData(np.asarray(handshake))
        print("Esperando Confirmação")
        inicio = time.time()
        tempo = False
        while com1.rx.getIsEmpty():
                if time.time() - inicio >= 5:
                    resposta = str(input("Servidor inativo, deseja tentar novamente? S/N : "))
                    if resposta.upper() == "S":
                        com1.sendData(np.asarray(handshake))
                        inicio = time.time()
                        pass
                    else:
                        print("-------------------------")
                        print("Comunicação encerrada")
                        print("-------------------------")
                        com1.disable()
                        print("--- {:.4f} seconds ---".format(time.time() - start_time))
                        exit()
        print("Tamanho do Comando", tamComando) 
        tamanhoRecebido = int.from_bytes(tamComando, byteorder="big")
        print("tamanhoRecebido: " , tamanhoRecebido/2)
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print(txBuffer)
        tamanhoLista= (len(txBuffer))
        print("Enviando Tamanho da lista")
        print("A lista tem {0} bytes".format(tamanhoLista.to_bytes(2, 'big')))
        com1.sendData(tamanhoLista.to_bytes(2, 'big'))
        print("Tamanho da lista enviado")

        print("Esperando Confirmação")
        tamComando, nRx = com1.getData(2)
        print("Tamanho do Comando", tamComando) 
        tamanhoRecebido = int.from_bytes(tamComando, byteorder="big")
        print("tamanhoRecebido: " , tamanhoRecebido/2)
        
        
        if tamanhoLista == tamanhoRecebido:
            time.sleep(0.1)
            print("Tamanho Correto Recebido:")
            print("Transmitindo Lista")
            i = 0
            while i < (tamanhoLista):
                com1.sendData(np.asarray(txBuffer[i]))
                time.sleep(0.2)
                com1.sendData(np.asarray(txBuffer[i+1]))
                print(f"Enviado {txBuffer[i+1]}" )
                print(f"Comando: {int((i+1)/2)+1}")
                time.sleep(0.2)
                i += 2
        else:
            print('Tamanho Errado')
            print("Lista não enviada :(  ")
        print(comandofinal)
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

            
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
