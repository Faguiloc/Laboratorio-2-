import socket
import sys
import random
import pyDes
from time import sleep
#cliente(Marley)


#**********************IMPORTANTE***********************#
#  Es necesario instalar la libreria pyDes para que el  #
#             Codigo funcione sin problemas.            #
#*******************************************************#


def EncriptadoDES():
    texto= open('mensajeentrada.txt',"r")
    llave= pyDes.des("abcdefgh",padmode=pyDes.PAD_PKCS5)    #Se asigna la clave y se activa el modo de padding para rellenar cualquier caracter faltante
    textoEncripted=llave.encrypt(texto.read())
    texto.close()
    return textoEncripted

#Valores publicos y creación del valor a
PrimoPublico=29 #p
BasePublico=5   #g
a = random.randint(1, PrimoPublico - 1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexion al servidor
server_address = ('localhost', 10000)
print('Conectando a {} en el puerto {}'.format(*server_address))
sock.connect(server_address)
sleep(2)


A=str((BasePublico**a) % PrimoPublico) #Calculo de A

#Comienza el envio de A y recepcion de B y K por parte del servidor
sock.sendall(bytes(A,"utf-8"))
datos=sock.recv(16)
datos=datos.split()

Bserver=datos[0].decode("utf-8")
Kserver=datos[1].decode("utf-8")
Kclient= (int(Bserver)**a) % PrimoPublico #Se calcula K del cliente

print("El cliente recibio B y K del servidor. B:",Bserver)
sleep(1)
print("La K del cliente es:", Kclient)
sleep(1)
print("La K del servidor es:", Kserver)
sleep(1)

if int(Kserver) == int(Kclient):
    input("La conexión es segura, presione Enter para transmitir el mensaje...")
    sleep(1)

    encriptado=EncriptadoDES()
    LargoMensaje= len(encriptado)       #Se calcula el largo del mensaje
    MensajeEnviado=0                    #y se crea una variable para llevar el conteo de la cantidad de bytes enviados

    enviando=True
    while enviando:
         if MensajeEnviado==LargoMensaje:
             enviando=False

         elif MensajeEnviado+16>=LargoMensaje:
             Final=LargoMensaje-MensajeEnviado                              #Si no alcanzan los 16 bytes, se envia el resto del mensaje faltante
             sock.sendall(encriptado[MensajeEnviado:MensajeEnviado+Final])
             MensajeEnviado+=Final

         elif MensajeEnviado + 16 < LargoMensaje:                           #Se mandan paquetes de 16 bytes por cada envío
             sock.sendall(encriptado[MensajeEnviado:MensajeEnviado + 16])
             MensajeEnviado += 16

    print("Mensaje enviado con éxito")
    sleep(2)


else:
    print("La conexión con el servidor no es segura. Cortando la comunicación")
    sleep(3)
    sys.exit()

