# Embedded-Peta-Linux
Embedded Linux development on Zynq™ using Vivado™

El proyecto se basa en la creación de una aplicación para detección de rostros desde formato video. El material hardware principal es la tarjeta PYNQ-Z2 en la que se incluye una imagen de Linux embebido que permite la ejecución del programa generado en Python. A continuación se mostrará el desarrollo de la misma así como los resultados obtenidos.

Lista de los comandos utilizados durante el proceso

### Instalación de PetaLinux
Para la generación de la imagen de Linux se utilizará la herramienta de AMD Petalinux. Esta herramienta incluye diferentes funcionalidades facilitando así el desarrollo de sistemas embebidos Linux, además del indicado anteriormente esta permite la generación del BPS que posibilita el acceso a los controladores del dispositivo o incluye instrucciones para la gestión del acceso a red.
La versión de Petalinux que se instalará es la 2020.2, igual a la utilizada para el desarrollo de las prácticas a través de Vivado y Vitis. La versión de Ubuntu será la 18.04.6 LTS, indicada en [1] para garantizar que el proceso se realice correctamente. Una vez descargada el archivo de instalación de Petalinux (en el directorio en el que se instalará) los pasos a realizar son:
 1.	Creación del directorio para la instalación en Linux.
 ```
mkdir -p /petalinux/2020.2
```
 3.	Reconfiguración de la consola para la utilización de bash (se debe seleccionar no)
```
sudo dpkg-reconfigure dash
```
 5.	Descarga de los paquetes correspodientes a la arquitectura i386.
```
sudo dpkg --add-architecture i386
```
 7.	Actualización de los paquetes de Ubuntu.
```
sudo apt update
```
 9.	Instalación de las dependencias necesarias para Petalinux, estas se incluyen en el fichero “plnx-env-setup.sh”
```
sudo bash /<ruta-a-script>/plnx-env-setup.sh
```
Este script se ha descargado en https://adaptivesupport.amd.com/s/article/73296?language=zh_CN

 11.	Instalación de Petalinux.
```
bash /<ruta-a-instalador>/petalinux-v2020.2-final-installer.run --dir /ruta-a-directorio/petalinux/2020.2
```

 Una vez finalizada la instalación, el flujo de trabajo para la generación de la imagen es:

1. Cargar el entorno de PetaLinux
```console
source ./settings.sh
```

2. Crear un nuevo proyecto PetaLinux para Zynq
```
petalinux-create project --template zynq --name /ruta/a/proyecto
```

3. Importar la descripción de hardware generada en Vivado (.xsa)
```
petalinux-config --get-hw-description /ruta/al/archivo/XSA
```
4. Construcción del sistema
Nota! Este paso puede tardar bastante tiempo
```
petalinux-build
```

5. Generación de la imagen de arranque
```
cd ./images/linux
petalinux-package --boot \
  --fsbl zynq_fsbl.elf \
  --u-boot u-boot.elf \
  --fpga system.bit \
  --force
```

6. Comprobaciones
Una vez arrancada la placa, desde la consola UART
se puede comprobar la dirección IP con:
```
ifconfig
```
 Con esa IP, es posible conectarse por SSH desde el PC:
 ```
ssh petalinux@ip.de.la.placa
```
 o
```
sudo picocom -b 115200 /dev/ttyUSB1
```

 Desde la máquina principal también se puede verificar la conectividad
 mediante pruebas de ping:
 ```
ping direccion.ip
```

### Troubleshooting
 En caso de errores de tipo "bad address" pueden ser utiles estas referencias
https://support.xilinx.com/s/question/0D52E00006hpTKeSAM/petalinux-201310-can-ping-outside-web-site
 https://support.xilinx.com/s/question/0D52E00006hpRxBSAU/petalinux-build-ethernet-not-working-cannot-ping

 Tanto el proceso de instalación como generación de la imagen se ha automatizado a través de dos scripts.

### Requisitos Funcionales
El sistema debe: 
  1. Permitir la captura de vídeo a través de una cámara conectada al puerto USB de la tarjeta PYNQ-Z2.
  2. Realizar la detección facial en tiempo real sobre el vídeo de entrada.
  3. Calcular y mostrar el número de rostros detectados en cada frame procesado.
  4. Retransmitir el vídeo procesado hacia un servidor web para su visualización desde un navegador en la red local.

### Requisitos No funcionales
El sistema debe:
  1. Garantizar un procesamiento y retransmisión del vídeo en tiempo real.
  2. Presentar una interfaz gráfica intuitiva y fácil de usar, accesible desde un navegador web.
  3. Mostrar un código estructurado de forma modular, para facilitar comprensión y futuras ampliaciones.

     
### Arquitectura del sistema Hardware:
El sistema se basa en la tarjeta PYNQ-Z2, configurada con un entorno de Linux embebido generado mediante PetaLinux. 
La placa recibe la señal de vídeo a través del puerto USB, la procesa internamente y retransmite los resultados mediante la conexión Ethernet hacia la red local. 
Este montaje permite la ejecución de la aplicación sobre Linux embebido, integrando adquisición de vídeo, procesamiento en tiempo real y visualización remota a través de un servidor web.
![HW](https://github.com/user-attachments/assets/f3db1c78-f7e5-4ac9-93cb-8ee759db5b5d)


### Software:
![SW](https://github.com/user-attachments/assets/76c86b6d-81a3-4a0e-acc4-f3c69d1cd3bc)

  1. Funciones principales:
     1.1 Inicialización de los controladores e interfaz gráfica.
     1.2 Obtención de los frames de datos.
  2. Procesamiento de la imagen:
     2.1 Aplicar máscara del tono de la piel.
     2.2 Detección del contorno.
     2.3 Filtrado de ruido.
     2.4 Descartar areas pequeñas.
     2.5 Actualización del frame y contador.
  3. Actualización de la interfaz gráfica.
