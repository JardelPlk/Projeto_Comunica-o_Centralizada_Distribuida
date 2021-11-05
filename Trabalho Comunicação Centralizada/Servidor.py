import socket
import threading


def workerThread(s):
    while True:
        msg = s.recv(1024)
        if not msg: break
        msg_test = msg.decode()
        print('O cliente enviou: ', msg_test)

        # ANTES DE SEPARAR VOCÊ TEM QUE ENTCONTRAR A LINHA QUE DE FATO TEM O USUARIO E A SENHA
        # A LINHA QUE VOCE QUER VEM DEPOIS DE UM \N\N
        msgs = msg_test.split("usuario")  # Separar o usuario e senha
        msgs_2 = msgs[1].split("&")  # Separar usuario da senha
        usuario = msgs_2[0]
        usuario = usuario[1:]
        senha = msgs_2[1]
        senha = senha[9:]

        if usuario == 'jardel' and senha == '123':  # VALIDAR COM ALGO UM USUARIO E SENHA QUALQUER.. AQUI SE COLOCAR QUALQUER COISA DA CERTO
            cabecalho = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nConnection: Keep-Alive\r\n' \
                        'Content-Encoding: gzip, deflate, br\r\nContent-Type: text/html; charset=utf-8\r\n' \
                        'Keep-Alive: timeout=5, max=999\r\nContent-Length: 200\r\n\r\n'
            html = '<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n<meta ' \
                   'charset="utf-8">\n<title>Resposta</title>\n</head>' \
                   '\n<body>\n<h1>200 OK!</h1>\n</body>\n</html>'
            resposta = cabecalho + html
            # A RESPOSTA TEM QUE SER CRIADA AQUI DENTRO: CRIAR UM ATRIBUTO CABEÇALHO QUE VAI CONTER O CABEÇALHO DO HTTP COM A PRIMEIRA LINHA SENDO HTTP/1.1 200 OK
            # LEMBRE-SE DE COLOCAR O CONTENT-LENGHT (O VALOR É O TAMANHO DO ATRIBUTO HTML), CONTENT-TYPE E OUTROS QUE EXPLICO NO EXERCICIO
            # CRIAR OUTRO ATRIBUTO COM O HTML QUE VAI SER ENVIADO
            # CRIAR UM ATRIBUTO RESPOSTA QUE CONCATENE O CABEÇALHO E O HTML SEPARADOS POR /N/N
        else:
            cabecalho = 'HTTP/1.1 401 UNAUTHORIZED\r\nAccess-Control-Allow-Origin: *\r\nConnection: Keep-Alive\r\n' \
                        'Content-Encoding: gzip, deflate, br\r\nContent-Type: text/html; charset=utf-8\r\n' \
                        'Keep-Alive: timeout=5, max=999\r\nContent-Length: 200\r\n\r\n'
            html = '<!DOCTYPE html>\n<html lang="pt-br">\n<head>\n<meta ' \
                   'charset="utf-8">\n<title>Resposta</title>\n</head>' \
                   '\n<body>\n<h1>401 UNAUTHORIZED!</h1>\n</body>\n</html>'
            resposta = cabecalho + html
        resposta = resposta.encode('utf-8')
            # A RESPOSTA TEM QUE SER CRIADA AQUI DENTRO: CRIAR UM ATRIBUTO CABEÇALHO QUE VAI CONTER O CABEÇALHO DO HTTP COM A PRIMEIRA LINHA SENDO HTTP/1.1 401 UNAUTHORIZED
            # LEMBRE-SE DE COLOCAR O CONTENT-LENGHT (O VALOR É O TAMANHO DO ATRIBUTO HTML), CONTENT-TYPE E OUTROS QUE EXPLICO NO EXERCICIO
            # CRIAR OUTRO ATRIBUTO COM O HTML QUE VAI SER ENVIADO
            # CRIAR UM ATRIBUTO RESPOSTA QUE CONCATENE O CABEÇALHO E O HTML SEPARADOS POR /N/N

        # TALVEZ ENVIAR COMO BYTE NÃO É NECESSÁRIO... COLOQUE O ATRIBUTO RESPOSTA.ENCODE() QUE DEVE SER SUFICIENTE
        #msg = (bytes('HTTP/1.1 200 OK\r\n', encoding='utf8') + msg)
        # msg = msg[::-1] #Inverte a String

        try:
            s.send(resposta)
        except:
            print('Erro ao responder.')
    s.close()


def Main():
    host = ""
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Servidor inicializado na porta " + str(port))

    while True:
        s, addr = server_socket.accept()
        print('Cliente Conectado:', addr[0], ':', addr[1])
        tw = threading.Thread(target=workerThread, args=[s])
        tw.start()


if __name__ == '__main__':
    Main()
