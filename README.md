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
