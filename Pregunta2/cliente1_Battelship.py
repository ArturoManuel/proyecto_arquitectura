import socket
import time
import threading

MSG_NUM = 1
SOCK_BUFFER = 1024
SLEEP_TIME = 2

def get_player_number(sock):
    data = sock.recv(2)
    player_number = data.decode("utf-8")
    return player_number

def handle_data(sock):
    data = sock.recv(SOCK_BUFFER).decode("utf-8")
    print(f"{data}", end="")
    room_name = input()
    sock.sendall(room_name.encode())

def mostrar_tablero(sock):
    tablero = sock.recv(SOCK_BUFFER).decode("utf-8")
    print(f"{tablero}")


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.1.4", 5050)
    
    
    try:
        sock.connect(server_address)
        # Obtenemos el numero de jugador
        player_number = get_player_number(sock)
        print(f"Usted es el jugador {player_number}")
        handle_data(sock) #recibimos el nombre de la sala

        if player_number == "1":
            # print(sock)
            handle_data(sock)# recibimos la opcion del tablero
            mostrar_tablero(sock)
        
        else:
            # print(sock) # else: player_number== "2": #jugador2
            data = sock.recv(SOCK_BUFFER).decode("utf-8")
            print(f"{data}")
            if data == "Usted ha ingresado a la sala\n":
                mostrar_tablero(sock)
            
        # while True:
        #     if player_number == "1":
        #         data = sock.recv(SOCK_BUFFER).decode("utf-8")
        #         if data=="Tu turno\n":
        #             print(f"{data}")
        #             handle_data(sock)# recibimos la componente x
        #             handle_data(sock)# recibimos la componente y
        #         else:
        #             print(f"{data}")
        #     else:
        #         if data=="Tu turno\n":
        #             print(f"{data}")
        #             handle_data(sock)# recibimos la componente x
        #             handle_data(sock)# recibimos la componente y
        #         else:
        #             print(f"{data}")
        #     break
                
    except KeyboardInterrupt:
        print("Usuario cerro abruptamente el programa")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cierro conexion")
        sock.close()









# if __name__ == '__main__':
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ("192.168.1.4", 5050)
#     sock.connect(server_address)

#     try:
#         # Obtenemos el numero de jugador
#         player_number = get_player_number(sock)
#         print(f"Usted es el jugador {player_number}")
#         handle_data(sock) #recibimos el nombre de la sala

#         if player_number == "1":
#             handle_data(sock)# recibimos la opcion del tablero
#             mostrar_tablero(sock)
#             data=sock.recv(SOCK_BUFFER).decode("utf-8")
#             # if data=="Escribe un mensaje al socket1\n":
#             #     mensaje=input()
#             #     sock.sendall(mensaje.encode())
#             # else:
#             #     print(data)
#         else: #player_number == "2"
#             # recibimos mensaje de confirmacion de sala
#             data = sock.recv(SOCK_BUFFER).decode("utf-8")
#             print(f"{data}")

#             if data == "Usted ha ingresado a la sala\n":
#                 mostrar_tablero(sock)
#             # data=sock.recv(SOCK_BUFFER).decode("utf-8")
#             # if data=="Escribe un mensaje al socket1\n":
#             #     mensaje=input()
#             #     sock.sendall(mensaje.encode())
#             # else:
#             #     print(data)

            
#         while True:
#             # data = sock.recv(SOCK_BUFFER).decode("utf-8")
#             # print(f"{data}")
#             pass
                 
#     except KeyboardInterrupt:
#         print("Usuario cerro abruptamente el programa")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         print("Cierro conexion")
#         sock.close()


    # if player_number== "1":
            #     data=sock.recv(SOCK_BUFFER).decode("utf-8")
            #     if data == "Es tu turno para ingresar coordenadas\n":
            #         print(f"{data}")#EL mensaje de data
            #         mensaje=sock.recv(SOCK_BUFFER).decode("utf-8")
            #         if mensaje!="Valor ingresado excede el tamaño del tablero" or mensaje!="Valor ingresado no es un numero":
            #             print(f"{mensaje}")
            #         else:
                        
            #             coordenada_X=input()
            #             sock.sendall(coordenada_X.encode())
            #             handle_data(sock)
            #     else:
            #         data = sock.recv(SOCK_BUFFER).decode("utf-8")
            #         print(f"{data}")#Recibimos el mensaje de espera de turno
                    
            # else:
            #     data=sock.recv(SOCK_BUFFER).decode("utf-8")
            #     if data == "Es tu turno para ingresar coordenadas\n":
            #         mensaje=sock.recv(SOCK_BUFFER).decode("utf-8")
            #         if mensaje!="Valor ingresado excede el tamaño del tablero" or mensaje!="Valor ingresado no es un numero":
            #             print(f"{mensaje}")
            #         else:
            #             coordenada_X=input()
            #             sock.sendall(coordenada_X.encode())
            #             handle_data(sock)
            #     else:
            #         data = sock.recv(SOCK_BUFFER).decode("utf-8")
            #         print(f"{data}")#Recibimos el mensaje de espera de turno