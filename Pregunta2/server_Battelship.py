import socket
import threading
import random
import time

SOCK_BUFFER = 4
NUM_PLAYERS = 2
NUM_BARCOS = 3
def client_handler(client_socket, address):
    try:
        while True:
            # print(f"Conexion de {address}")
            mensaje=("Ingrese su opción de tablero = opción “1” de 5 x5, “2” de 8 x 8 y “3 de 10 x 10: ")
            client_socket.sendall(mensaje.encode())
            data = client_socket.recv(SOCK_BUFFER)
            if data:
                print(f"recibi {data}")
            else:
                break
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        print("Cliente cerro la conexion")
        client_socket.close()

def handle_data(client_socket, mensaje):
    client_socket.sendall(mensaje.encode())
    return client_socket.recv(1024).decode()

def create_room(client_socket, address):
    # print(f"Conexion de {address}")
    player_number = "1"
    client_socket.sendall(player_number.encode())
    data = handle_data(client_socket,"Ingrese el nombre de la sala: ")
    # print(f"Se ha creado la sala {data}")
    return data

def ask_room_name(client_socket, address):
    # print(f"Conexion de {address}")
    player_number = "2"
    client_socket.sendall(player_number.encode())
    data = handle_data(client_socket,"Ingrese el nombre de la sala: ")
    return data

def get_size(client_socket):
    opcion = handle_data(client_socket,"Ingrese su opción de tablero = opción “1” de 5 x5, “2” de 8 x 8 y “3 de 10 x 10: ")
    if opcion == "1":
        board_size = 5
    elif opcion == "2":
        board_size = 8
    elif opcion == "3":
        board_size = 10
    return board_size
    
def init_board(board_size):
    board = []
    for i in range(board_size):
        row = ["0"] * board_size
        board.append(row)
    return board

def gen_coordenadas_barco(board_size):
    x = random.randint(0, board_size-1)
    y = random.randint(0, board_size-1)
    return x, y

def init_board_player(board_size):
    board = init_board(board_size)#creamos una copia de la lista
    barcos = []
    for _ in range(NUM_BARCOS):
        x, y = gen_coordenadas_barco(board_size)
        barcos.append([x, y])
        board[x][y] = "B"
    return board, barcos

def mostrar_tablero(tablero):
    tablero_str = ""
    for fila in tablero:
        tablero_str += ''.join(fila)
        tablero_str += '\n'

    print(tablero_str)

def enviar_tablero(client_socket,tablero):
    tablero_str = ""
    for fila in tablero:
        tablero_str += ''.join(fila)
        tablero_str += '\n'
    client_socket.sendall(tablero_str.encode())

def captura_valor(eje,client_socket,TAM_TABLERO):
    while True:
        if eje == 0:
            mensaje=f"Por favor ingrese el valor de fila (0-{TAM_TABLERO-1}) y pulse ENTER: "
            client_socket.sendall(mensaje.encode())
            val=client_socket.recv(1024).decode()
        else:
            mensaje=f"Por favor ingrese el valor de fila (0-{TAM_TABLERO-1}) y pulse ENTER: "
            client_socket.sendall(mensaje.encode())
            val=client_socket.recv(1024).decode()
            # print(type(val),val)
        if val.isnumeric():
            if int(val) < TAM_TABLERO:
                break
            else:
                mensaje="Valor ingresado excede el tamaño del tablero"
                client_socket.sendall(mensaje.encode())

        else:
            mensaje="Valor ingresado no es un numero"
            client_socket.sendall(mensaje.encode())

    return int(val) 

def ingresa_coordenadas(client_socket,board_size):
   x = captura_valor(0,client_socket,board_size)
   y = captura_valor(1,client_socket,board_size)
   

   return x, y
def evalua_coordenadas(x, y ,barcos):
    idx = 0
    for barco in barcos:
        if barco[0] == x and barco[1] == y:
            return idx
    return -1
def modificar_tablero(x, y, valor, tablero):
    tablero[x][y] = valor

    return tablero
lista_conexiones=[]
turno_thread1=0
def funcion_threading_1(conn,client_address):
    global room_name
    global board_size
    global lista_conexiones
    global bracos_hundidos1
    global bracos_hundidos2
    global board2
    global board1
    global turno_thread1
    global barcos1
    # global barcos_hundidos1
    # print(turno_thread1)
    try:
        
         
        room_name = create_room(conn, client_address)
        board_size = get_size(conn)
        board1, barcos1 = init_board_player(board_size)
        enviar_tablero(conn, board1)
        if turno_thread1==0:
            mensaje="Tu turno\n"
            conn.sendall(mensaje.encode())
            while len(barcos_hundidos2) < NUM_BARCOS :
                x, y = ingresa_coordenadas(conn,board_size)
                resultado = evalua_coordenadas(x, y)
                if resultado == -1:
                    board2 = modificar_tablero(x, y, "F", board2)
                else:
                    barcos_hundidos2.append(barcos2[resultado])
                    mensaje=f"Disparo acertado, quedan {NUM_BARCOS - len(barcos_hundidos2)} barcos"
                    board2 = modificar_tablero(x, y, "X", board2)
                    enviar_tablero(board2)
            turno_thread1=turno_thread1+1    
        else:
            mensaje="Espera un momento\n"
            conn.sendall(mensaje.encode())
            turno_thread1=turno_thread1-1
            
    except Exception as e:
        print(f"Ocurrio un error:{e}")
    finally:
        print("Cliente cerro la conexio")
        conn.close()
def funcion_threading_2(conn,client_address):
    global barcos2
    global barcos1
    global board1
    global board2
    global turno_thread1
    global lista_conexiones
    global room_name
    global barcos_hundidos2
    global bracos_hundidos1
    try:
        room_name_recv = ask_room_name(conn, client_address)
        if room_name_recv == room_name:
            mensaje = "Usted ha ingresado a la sala\n"
            conn.sendall(mensaje.encode())
            board2, barcos2 = init_board_player(board_size)
            enviar_tablero(conn, board2)
            if turno_thread1==0:
                mensaje="Tu turno\n"
                conn.sendall(mensaje.encode())
                while len(barcos_hundidos1) < NUM_BARCOS :
                    x, y = ingresa_coordenadas(conn,board_size)
                    resultado = evalua_coordenadas(x, y)
                    if resultado == -1:
                        board1 = modificar_tablero(x, y, "F", board1)
                    else:
                        barcos_hundidos1.append(barcos1[resultado])
                        mensaje=f"Disparo acertado, quedan {NUM_BARCOS - len(barcos_hundidos2)} barcos"
                        board1 = modificar_tablero(x, y, "X", board1)
                        enviar_tablero(board2)
                turno_thread1=turno_thread1+1 
            else:
                mensaje="Espera un momento\n"
                conn.sendall(mensaje.encode())
                turno_thread1=turno_thread1-1
        
        else:
            mensaje = "No existe la sala ingresada"
            conn.sendall(mensaje.encode())
            
    except Exception as e:
        print(f"Ocurrio un error:{e}")
    finally:
        print("Cliente cerro la conexio")
        conn.close()
                    
            

if __name__ == "__main__":
    global n
    n=2
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Valor de SOCK BUFFER: {SOCK_BUFFER}")

    server_address = ("0.0.0.0", 5050)
    sock.bind(server_address)
    sock.listen(NUM_PLAYERS)
    
    barcos_hundidos1=[]
    barcos_hundidos2=[] 

while True:
    print("Esperando conexiones")
    conn1, client_address = sock.accept()
    t = threading.Thread(target=funcion_threading_1, args=(conn1, client_address))
    lista_conexiones.append(conn1)
    conn2, client_address = sock.accept()
    n = threading.Thread(target=funcion_threading_2, args=(conn2, client_address))
    lista_conexiones.append(conn2)
    conn1=conn2
    conn=lista_conexiones[-1:]
    
    t.start()
    n.start()
    

