import sys
import struct
import bitarray as bit

# Clase para el arbol
class Node:
    def __init__(self, value = None):
        self.value = value
        self.left = None
        self.right = None

def read_compressed_file(file_path):
    readbits = bit.bitarray()
    with open(file_path, "rb") as file:
        # Con el struct se lee el tamaño del bitarray para evitar bits extras
        bit_length = struct.unpack('I', file.read(4))[0]
        readbits.fromfile(file)
        # Se recorta el bitarray al tamaño original
        readbits = readbits[:bit_length]
        compressed = readbits.to01()
    return compressed

def read_table_file(file_path):
    with open(file_path, "r") as file:
        table = file.read()
    return table

def create_tree(routes):
    # Re-crear el arbol con las rutas
    tree = Node()
    for char, path in routes:
        current = tree
        for bit in path:
            if bit == "0":
                if current.left is None:
                    current.left = Node()
                current = current.left
            else:
                if current.right is None:
                    current.right = Node()
                current = current.right
        current.value = char if char != "ln" else "\n"
    return tree

# Descomprimir el texto
def decompress_text(tree, compressed):
    decompressedText = ""
    current = tree
    for bit in compressed:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.value is not None:
            decompressedText += current.value
            current = tree
    return decompressedText

def main():
    if len(sys.argv) < 4:
        print("Sin suficientes argumentos")
        sys.exit()

    # Leer los 2 archivos
    compressed = read_compressed_file(sys.argv[1])
    table = read_table_file(sys.argv[2])

    # Procesar la tabla para tener las rutas por separado
    routes = table.strip().split("\n")
    routes = [route.split(":") for route in routes]

    # Crear el arbol con las rutas
    tree = create_tree(routes)

    # Descomprimir el texto
    decompressedText = decompress_text(tree, compressed)

    # Poner el texto descomprimido en un archivo
    with open(sys.argv[3], "w") as file:
        file.write(decompressedText)
        print("Archivo descomprimido.")

main()
