#!/bin/bash

# Obtener la lista de archivos modificados usando git status
files=$(git status --porcelain | awk '{print $2}')

# Array para almacenar los tamaños de los archivos
declare -A file_sizes

# Obtener y almacenar los tamaños de los archivos
for file in $files
do
    size=$(du -h "$file" | cut -f1)
    file_sizes["$file"]=$size
done

# Ordenar archivos por tamaño de mayor a menor
sorted_files=$(for file in "${!file_sizes[@]}"; do echo "${file_sizes[$file]} $file"; done | sort -hr | cut -d' ' -f2-)

# Imprimir los archivos ordenados por tamaño
for file in $sorted_files
do
    echo "${file_sizes[$file]} - $file"
done
