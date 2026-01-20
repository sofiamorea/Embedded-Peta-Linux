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

### Requisitos funcionales y no funcionales
Los requisitos funcionales: 
El sistema debe:
  1. Permitir la captura de vídeo a través de una cámara conectada al puerto USB de la tarjeta PYNQ-Z2.
  2. Realizar la detección facial en tiempo real sobre el vídeo de entrada.
  3. Calcular y mostrar el número de rostros detectados en cada frame procesado.
  4. Retransmitir el vídeo procesado hacia un servidor web para su visualización desde un navegador en la red local.

Por otra parte los no funcionales:
  1. Garantizar un procesamiento y retransmisión del vídeo en tiempo real.
  2. Presentar una interfaz gráfica intuitiva y fácil de usar, accesible desde un navegador web.
  3. Mostrar un código estructurado de forma modular, para facilitar comprensión y futuras ampliaciones.

     
### Arquitectura del sistema:
#### Hardware:
El sistema se basa en la tarjeta PYNQ-Z2, configurada con un entorno de Linux embebido generado mediante PetaLinux. 
La placa recibe la señal de vídeo a través del puerto USB, la procesa internamente y retransmite los resultados mediante la conexión Ethernet hacia la red local. 
Este montaje permite la ejecución de la aplicación sobre Linux embebido, integrando las funciones como la adquisición de vídeo, procesamiento en tiempo real y visualización remota a través de un servidor web.

El conexionado entre ambos se realiza a través del puerto USB, accediendo a la interfaz web mediante Ethernet.
<img width="500" height="624" alt="Screenshot 2026-01-20 132153" src="https://github.com/user-attachments/assets/c5c3357e-f0e7-430f-aec3-dcfe94dbd870" />

#### Software:
La siguiente figura muestra el diagrama de flujo seguido:

<img width="300" height="600" alt="Screenshot 2026-01-20 132424" src="https://github.com/user-attachments/assets/4cd6932a-3b04-4c65-8141-7815174b436d" />

En primer lugar se realiza la inicialización de los controladores e interfaz gráfica así como la obtención de los frames de datos. A continuación se implementa el procesamiento 
de la imagen a traves de los siguientes pasos:
 1. Aplicación de la máscara para detectar el tono de la piel
 2. Detección del contorno.
 3. Filtrado de ruido.
 4. Descartar áreas pequeñas en las que no se pueda encontrar un rostro.
    
Por último se realiza la actualización de la interfaz gráfica encuadrando el rostro y mostrando el contador de detecciones.

### Resultados y conclusión
A través de este proyecto se ha estudiado el flujo de trabajo del desarrollo de aplicaciones de Linux Embebido así como la herramienta Petalinux que facilita la generación de 
imagenes así como la configuración de las mismas. 

### Bibliografía
[1] AMD Tools and Win10 WSL. Trenz Electronic Documentation. URL: https://wiki.trenz-electronic.de/display/PD/AMD+Tools+and+Win10+WSL#AMDToolsandWin10WSL-NotesandHintsandotherstuff

[2] 73296 - PetaLinux: How to install the required packages for the PetaLinux Build Host? AMD Adaptative Support. URL: https://adaptivesupport.amd.com/s/article/73296?language=zh_CN

[3] Installation Steps. AMD Technical Information Portal. URL: https://docs.amd.com/r/2022.1-English/ug1144-petalinux-tools-reference-guide/Installing-the-PetaLinux-Tool

[4] Petalinux Prebuild Images 2020.2 Release. URL: https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1065451521/2020.2+Release

[5] Petalinux BSP installaation. AMD Technical Information Portal. URL: https://docs.amd.com/r/2020.2-English/ug1144-petalinux-tools-reference-guide/PetaLinux-BSP-Installation

[6] AMD Petalinux Tools. AMD. URL: https://www.amd.com/es/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html

[7] Petalinux. Trenz Electronic Documentation.  https://wiki.trenz-electronic.de/display/PD/PetaLinux






