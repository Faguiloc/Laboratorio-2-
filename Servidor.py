import socket
import sys
import random
import pyDes
import struct
import time
# Servidor (Bob)


def DesencriptadoDES(mensaje):
    llave= pyDes.des("abcdefgh",padmode=pyDes.PAD_PKCS5)            #Se desencripta el mensaje
    textoDecrypted=llave.decrypt(mensaje)

    return textoDecrypted

def Guardado(mensaje):
    salida=open("mensajerecibido.txt","wb")                         #Se guarda el mensaje desencriptado en un archivo .txt
    salida.write(mensaje)
    salida.close()
    print("Mensaje Guardado con exito")
    time.sleep(3)

#Valores publicos y creación del valor b
PrimoPublico=29 #p
BasePublico=5   #g
b = random.randint(1, PrimoPublico - 1) #llave privada del servidor

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

sock.listen(1)

while True:

    print('Esperando conexión...')
    time.sleep(2)
    connection, client_address = sock.accept()
    try:
        print("Conexión exitosa a", client_address)
        Aclient=int(connection.recv(16))                    #recibe el valor de A del servidor
        print("El servidor recibio A del cliente:", Aclient)

        if Aclient:
            B=str((BasePublico**b) % PrimoPublico)          #Calcula B y K del servidor
            Kserver=str((Aclient**b)% PrimoPublico)

            datos=B+" "+Kserver                             #Se prepara la cadena de datos de B y K Se coloca un
            datos=bytes(datos,'utf-8')                      #espacio entre ambos valores para separarlos en el cliente
            connection.sendall(datos)

            MensajeRecibido=b""
            envio=True
            while envio:
                 MensajeCliente=connection.recv(16)                          #Se comienza a recibir el mensaje cuando
                 print("El mensaje del cliente es: ", MensajeCliente)        #se confirma que la conexion es segura
                 time.sleep(1)
                 if MensajeCliente==b"":        #Si el paquete viene vacio, indica que se acabo el mensaje
                     envio=False
                 else:
                     MensajeRecibido+=MensajeCliente[0:len(MensajeCliente)]


            MensajeDecifrado=DesencriptadoDES(MensajeRecibido)          #Cifra y luego guarda el mensaje
            Guardado(MensajeDecifrado)

    finally:
        print("Se ha perdido la conexion")              #Se termina la transmicion y se cierra el socket
        connection.close()


