#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import numpy as np
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "ACM0"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        start_time = time.time()
        comandos = []
        i = 0


        """ Lembrar de enviar comando por comando"""

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        if com1.enable() == True:
            print("Comunicação Aberta")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        tamComando, nRx = com1.getData(2)
        print("Tamanho do Comando", tamComando) 
        intc = int.from_bytes(tamComando, byteorder="big")
        print("Client enviou ", intc/2)
        com1.sendData(tamComando)
        print(f"Resposta enviada: {tamComando}")
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!

        #acesso aos bytes recebidos
        while i < intc/2:
            comandoSize, nRx = com1.getData(2)
            time.sleep(0.2)
            comandInt = int.from_bytes(comandoSize, byteorder="big")
            rxBuffer, nRx = com1.getData(comandInt)
            print(rxBuffer)
            comandos.append(rxBuffer)
            i += 1
            
        print("recebeu {}" .format(comandos))
        devolvendo = len(comandos)
        print(f"Devolvendo tamanho da lista de {devolvendo}")
        com1.sendData(devolvendo.to_bytes(2, 'big'))
        print("Tamanho da lista enviado")



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
