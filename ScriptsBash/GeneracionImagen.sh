#!/bin/bash
# Descripcion: instrucciones para la instalacion de Petalinux
echo "Inicio de la generacion de la imagen"
    
    #Incluir fichero de settings en bash 
    sudo nano /etc/bash.bashrc

    #Generacion del proyecto
    petalinux-create project --template zynq --name /ruta/a/proyecto

    #Configuracion de la imagen a traves del XSA
    petalinux-config --get-hw-description /ruta/al/archivo/XSA

    #Construccion de la imagen
    petalinux-build

    #Generacion de la imagen
    cd ./images/linux
    petalinux-package --boot \
        --fsbl zynq_fsbl.elf \
        --u-boot u-boot.elf \
        --fpga system.bit \
        --force

echo "Generacion imagen"
