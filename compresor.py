import sys
import bitarray as bit
import struct
freq = {}

if len(sys.argv) == 1 :
    print("El programa no tiene argumentos")
else:
    print("Primer Argumento:", sys.argv[1])
    file = open(sys.argv[1], "r")
    content = file.read()
    #print(content)
    file.close()

for i in range(len(content)):
    if content[i] in freq:
        freq[content[i]] += 1
    else:
        freq[content[i]] = 1

minmaxing = dict(sorted(freq.items(), key=lambda item: item[1])) #https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
print(minmaxing)
listakeys = list(minmaxing.keys())
listavalues = list(minmaxing.values())
#arbolmaker
def arbolmaker(dic):
    arbol = [(freq, value, []) for value, freq in dic.items()]
    while len(arbol) > 1:
        arbol.sort(key=lambda item: item[0])
        izq = arbol.pop(0)
        der = arbol.pop(0) if arbol else None
        comb = izq[0] + (der[0] if der else 0)
        arbol.append((comb, izq, der))  # Hacerlo en tuplas
    return arbol[0]  

arbol = arbolmaker(minmaxing)
#print(arbol)

def caminainador(arbol, result=''): #caminainador
    if not arbol:
        return result
    if len(arbol) < 2 or len(arbol) > 3:  #si es una hojita
        result = result[:-1] #por alguna razon tenia un 0 de mas lol
        if arbol == '\n':
            return "ln" + ":" + result + "\n"
        else:
            return arbol + ":" + result + "\n"
    if len(arbol) > 1 and arbol[1]:
        caminoizq = caminainador(arbol[1], result + '0')
    else:
        caminoizq = ''
    if len(arbol) > 2 and arbol[2]:
        caminoder = caminainador(arbol[2],result + '1') 
    else:
        caminoder = ''
    return (caminoizq + caminoder)

owo = caminainador(arbol)
with open(f"{sys.argv[1]}.table", "w") as file:
    file.write(owo)

paths = {}
routes = owo.strip().split("\n")
routes = [route.split(":") for route in routes]
while [''] in routes:
    routes.remove([''])
print(routes)
for char, path in routes:
    if char == 'ln':
        paths['\n'] = path
    paths[char] = path

bits = bit.bitarray()
for char in content:
    bits.extend(paths[char])

with open(f"{sys.argv[1]}.huff", "wb") as file:
    file.write(struct.pack('I', len(bits)))
    bits.tofile(file)

def tree_height(tree):
    if not tree:
        return 0
    if isinstance(tree, str):
        return 0
    left_height = tree_height(tree[1]) if len(tree) > 1 else 0
    right_height = tree_height(tree[2]) if len(tree) > 2 else 0
    return 1 + max(left_height, right_height) 

def recorrer_level(node, level, levels):
    if isinstance(node, tuple):  
        levels[level].append(node[0])
        if node[1]:
            recorrer_level(node[1], level + 1, levels)
        if len(node) > 2 and node[2]:
            recorrer_level(node[2], level + 1, levels)

def anchuraMax(T):
    if not T:
        return 0

    height = tree_height(T)
    levels = [[] for _ in range(height + 1)]

    recorrer_level(T, 0, levels)  # Start traversal from the root

    max_width = max(len(level) for level in levels) 

    minecraft = ""
    minecraft += f"Altura: {height}\n"
    minecraft += f"Anchura: {max_width}\n"
    for i, level in enumerate(levels):
        minecraft += f"Nivel {i}: - Cantidad de nodos {len(level)}\n"
    minecraft += "===== Frecuencias =====\n"
    for key, value in minmaxing.items():
        if key == '\n':
            minecraft += f"Caracter: \\n - Frecuencia: {value}\n"
            continue
        minecraft += f"Caracter: {key} - Frecuencia: {value}\n"
    return minecraft

#write a file with the stats
with open(f"{sys.argv[1]}.stats", "w") as file:
    file.write(anchuraMax(arbol))
