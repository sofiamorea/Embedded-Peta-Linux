# Embedded-Peta-Linux
Embedded Linux development on Zynq™ using Vivado™

Lista de los comandos utilizados durante el proceso


### Instalación de PetaLinux
 Enlace oficial:
https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html


 Una vez finalizada la instalación, el flujo de trabajo es el siguiente:

### Cargar el entorno de PetaLinux
```console
source ./settings.sh
```

### Crear un nuevo proyecto PetaLinux para Zynq
```
petalinux-create project --template zynq --name /ruta/a/proyecto
```

### Importar la descripción de hardware generada en Vivado (.xsa)
```
petalinux-config --get-hw-description /ruta/al/archivo/XSA
```
### Construcción del sistema
Nota! Este paso puede tardar bastante tiempo
```
petalinux-build
```

### Generación de la imagen de arranque
```
cd ./images/linux
petalinux-package --boot \
  --fsbl zynq_fsbl.elf \
  --u-boot u-boot.elf \
  --fpga system.bit \
  --force
```

### Comprobaciones
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
