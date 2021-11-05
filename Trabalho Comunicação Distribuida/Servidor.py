import socket
import threading
import configparser
import sys

#Armazenar todas as mensagens neste vetor para depois identicar
#se o servidor ja recebeu
vetorMsgs = []

def workerThread(s):
    while True:
        msg = s.recv(1024)
        if not msg: break

        if len(vetorMsgs) == 0:
            print('O cliente enviou: ', msg.decode())
            cliente(obterVizinhoDireita(), str(msg), False)
            cliente(obterVizinhoEsquerda(), str(msg), False)
        else:
            print('O cliente ja recebeu esta mensagem')

        try:
            s.send(msg)
        except:
            print('Erro ao responder.')

    s.close()

def mensagemThread():
    msg = input('Digite a mensagem: ')
    #A variavel boleana serve para identificar se a mensagem esta sendo enviada
    #por este servidor, para a mensagem não ser armazenada no vetor deste servidor
    #e para este servidor receber a menagem de outro depois
    cliente(obterVizinhoDireita(), msg, True)
    cliente(obterVizinhoEsquerda(), msg, True)

def obterVizinhoDireita():
    config = configparser.RawConfigParser()
    config.read(sys.argv[1])
    return int(config.get('config', 'port_vizinho_direita'))

def obterVizinhoEsquerda():
    config = configparser.RawConfigParser()
    config.read(sys.argv[1])
    return int(config.get('config', 'port_vizinho_esquerda'))

def cliente(porta, texto, opcao):
    host = '127.0.0.1'
    port = porta
    msg = texto
    #Caso esteja recebendo a mensagem de outro servidro armazena senão não
    if opcao == False:
        vetorMsgs.append(msg)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (host, port)
    client_socket.settimeout(5)
    client_socket.connect(dest)
    client_socket.send(msg.encode('ascii'))
    try:
        resposta, servidor = client_socket.recvfrom(1024)
        #print('Resposta do Servidor: ', resposta.decode())

    except:
        print('Ocorreu um erro...')
    client_socket.close() #Fecha a conexão com o servidor

def Main():
    #Parte arquivo de config
    config = configparser.RawConfigParser()
    config.read(sys.argv[1])

    #Parte servidor
    host = ""
    port = int(config.get('config', 'port'))#Obter a porta do arquivo .properties

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Servidor inicializado na porta " + str(port))

    t = threading.Thread(target=mensagemThread)
    t.start()

    while True:
        s, addr = server_socket.accept()

        if len(vetorMsgs) == 0:
            print('Cliente Conectado:', addr[0], ':', addr[1])
            tw = threading.Thread(target=workerThread, args=[s])
            tw.start()

if __name__ == '__main__':
    Main()
