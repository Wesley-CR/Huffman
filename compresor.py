import sys
import bitarray as bit
import struct

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as file:
        return file.read()

def calcular_freq(content):
    freq = {}
    for i in range(len(content)):
        if content[i] in freq:
            freq[content[i]] += 1
        else:
            freq[content[i]] = 1
    return freq

def ordenar_por_frecuencia(freq):
    return dict(sorted(freq.items(), key=lambda item: item[1]))  # https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/

def arbol_maker(dic):
    arbol = [(freq, value, []) for value, freq in dic.items()]
    while len(arbol) > 1:
        arbol.sort(key=lambda item: item[0])
        izq = arbol.pop(0)
        der = arbol.pop(0) if arbol else None
        comb = izq[0] + (der[0] if der else 0)
        arbol.append((comb, izq, der))  # Hacerlo en tuplas
    return arbol[0]

def caminainador(arbol, result=''):  # caminainador
    if not arbol:
        return result
    if len(arbol) < 2 or len(arbol) > 3:  # si es una hojita
        result = result[:-1]  # por alguna razon tenia un 0 de mas lol
        if arbol == '\n':
            return "ln" + ":" + result + "\n"
        else:
            return arbol + ":" + result + "\n"
    if len(arbol) > 1 and arbol[1]:
        caminoizq = caminainador(arbol[1], result + '0')
    else:
        caminoizq = ''
    if len(arbol) > 2 and arbol[2]:
        caminoder = caminainador(arbol[2], result + '1')
    else:
        caminoder = ''
    return (caminoizq + caminoder)

def escribir_tabla(camino, nombre_archivo):
    with open(f"{nombre_archivo}.table", "w") as file:
        file.write(camino)

def generar_paths(camino):
    paths = {}
    routes = camino.strip().split("\n")
    routes = [route.split(":") for route in routes]
    while [''] in routes:
        routes.remove([''])
    for char, path in routes:
        if char == 'ln':
            paths['\n'] = path
        paths[char] = path
    return paths

def comprimir_contenido(content, paths, nombre_archivo):
    bits = bit.bitarray()
    for char in content:
        bits.extend(paths[char])
    with open(f"{nombre_archivo}.huff", "wb") as file:
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

def anchura_max(T, minmaxing):
    if not T:
        return 0
    height = tree_height(T)
    levels = [[] for _ in range(height + 1)]
    recorrer_level(T, 0, levels)
    max_width = max(len(level) for level in levels)

    stats = ""
    stats += f"Altura: {height}\n"
    stats += f"Anchura: {max_width}\n"
    for i, level in enumerate(levels):
        stats += f"Nivel {i}: - Cantidad de nodos {len(level)}\n"
    stats += "===== Frecuencias =====\n"
    for key, value in minmaxing.items():
        if key == '\n':
            stats += f"Caracter: \\n - Frecuencia: {value}\n"
            continue
        stats += f"Caracter: {key} - Frecuencia: {value}\n"
    return stats

def escribir_estadisticas(arbol, minmaxing, nombre_archivo):
    with open(f"{nombre_archivo}.stats", "w") as file:
        file.write(anchura_max(arbol, minmaxing))
    print("Archivo comprimido.")

def main():
    if len(sys.argv) == 1:
        print("El programa no tiene argumentos")
        sys.exit()
    nombre_archivo = sys.argv[1]
    content = leer_archivo(nombre_archivo)
    freq = calcular_freq(content)
    minmaxing = ordenar_por_frecuencia(freq)

    arbol = arbol_maker(minmaxing)
    camino = caminainador(arbol)
    escribir_tabla(camino, nombre_archivo)
    paths = generar_paths(camino)
    comprimir_contenido(content, paths, nombre_archivo)
    escribir_estadisticas(arbol, minmaxing, nombre_archivo)

main()
