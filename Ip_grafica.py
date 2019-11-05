import matplotlib
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

def dibujar_tablero(x, c, n):
    # Visualiza un tablero dada una formula f
    # Input:
    #   - f, una lista de literales
    #   - n, un numero de identificacion del archivo
    # Output:
    #   - archivo de imagen tablero_n.png
    # Inicializo el plano que contiene la figura
    fig, axes = plt.subplots()
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)

    # Dibujo el tablero
    step = 1./3
    tangulos = []
    # Creo los cuadrados en el tablero
    tangulos.append(patches.Rectangle(\
                                    (0, step), \
                                    step, \
                                    step,\
                                    facecolor='turquoise')\
                                    )
    tangulos.append(patches.Rectangle(*[(step, 0), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(2 * step, step), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(step, 2 * step), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(2 * step, 2 * step), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(0, 2 * step), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(2 * step, 0), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(step, step), step, step],\
            facecolor='turquoise'))
    tangulos.append(patches.Rectangle(*[(0, 0), step, step],\
            facecolor='turquoise'))

    # Creo las líneas del tablero
    for j in range(3):
        locacion = j * step
        # Crea linea horizontal en el rectangulo
        tangulos.append(patches.Rectangle(*[(0, step + locacion), 1, 0.015],\
                facecolor='teal'))
        # Crea linea vertical en el rectangulo
        tangulos.append(patches.Rectangle(*[(step + locacion, 0), 0.015, 1],\
                facecolor='teal'))

    for t in tangulos:
        axes.add_patch(t)

    # Cargando imagen
    arr_img = plt.imread("X.png", format='png')
    imagebox = OffsetImage(arr_img, zoom=0.1)
    imagebox.image.axes = axes

    arr_img2 = plt.imread("C.png", format='png')
    imagebox2 = OffsetImage(arr_img2, zoom=0.1)
    imagebox2.image.axes = axes

    # Creando las direcciones en la imagen de acuerdo a literal
    direcciones = {}
    direcciones[1] = [0.165, 0.835]
    direcciones[2] = [0.5, 0.835]
    direcciones[3] = [0.835, 0.835]
    direcciones[4] = [0.165, 0.5]
    direcciones[5] = [0.5, 0.5]
    direcciones[6] = [0.835, 0.5]
    direcciones[7] = [0.165, 0.165]
    direcciones[8] = [0.5, 0.165]
    direcciones[9] = [0.835, 0.165]

    for l in x:
        if x[l] != 0:
            ab = AnnotationBbox(imagebox, direcciones[int(l)], frameon=False)
            axes.add_artist(ab)

    for k in c:
        if c[k] != 0:
            if c[k] == x[k]:
                print("imposible ubicar O en la casilla "+ str(k) +" pues ya esta ocupada.")
            else:
                ab2 = AnnotationBbox(imagebox2, direcciones[int(k)], frameon=False)
                axes.add_artist(ab2)



    #plt.show()
    fig.savefig("tablero_" + str(n) + ".png")


x={1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0}
c={1:1, 2:1, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

dibujar_tablero(x, c,121)
