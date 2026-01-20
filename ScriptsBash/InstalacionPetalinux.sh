#!/bin/bash
# Descripcion: instrucciones para la instalacion de Petalinux
echo "Inicio de la instalacion de Petalinux"
    #Creacion del directorio
    mkdir -p /petalinux/2020.2
    
    #Reconfiguracion de la consola para utilizacion de bash
    sudo dpkg-reconfigure dash

    #Descarga de los paquetes de la arquitectura i386
    sudo dpkg --add-architecture i386

    #Actualizacion de los paquetes de Ubuntu
    sudo apt update

    #Instalacion de las dependencias
    sudo bash /<ruta-a-script>/plnx-env-setup.sh

    #Instalacion de Petalinux
    bash /<ruta-a-instalador>/petalinux-v2020.2-final-installer.run --dir /home/maria/petalinux/2020.2

echo "Instalacion completada"
