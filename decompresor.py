import sys
import struct
import bitarray as bit

# Clase para el arbol
class Node:
    def __init__(self, value = None):
        self.value = value
        self.left = None
        self.right = None

# Ver si pasaron los argumentos necesarios
if len(sys.argv) < 4:
    print("Insuficientes Argumentos")
    sys.exit()

readbits = bit.bitarray()
with open(sys.argv[1], "rb") as file:
    # Con el struct se lee el tamaño del bitarray para evitar bits extras
    bit_length = struct.unpack('I', file.read(4))[0]
    readbits.fromfile(file)
    # Se recorta el bitarray al tamaño original
    readbits = readbits[:bit_length]
    compressed = readbits.to01()

with open(sys.argv[2], "r") as file:
    table = file.read()

#print(compressed)
#print(table)

# Procesar la tabla para tener las rutas por separado
routes = table.strip().split("\n")
routes = [route.split(":") for route in routes]

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

# Descomprimir el texto
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

#print("=====================================")
print(decompressedText)
#poner en un archivo el texto
with open(sys.argv[3], "w") as file:
    file.write(decompressedText)
