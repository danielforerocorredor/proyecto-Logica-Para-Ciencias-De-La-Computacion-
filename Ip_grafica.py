import matplotlib
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

###########################Reglas######################################
Regla_disponibilidad = '(j=-a)Y(k=-b)Y(l=-c)Y(m=-d)Y(n=-e)Y(o=-f)Y(p=-g)Y(q=-h)Y(r=-i)Y(a=-j)Y(b=-k)Y(c=-l)Y(d=-m)Y(e=-n)Y(f=-o)Y(g=-p)Y(h=-q)Y(i=-r)'
Regla_triqui_horizon = '(aYbYcY-dY-eY-fY-gY-hY-i)Y(-aY-bY-cYdYeYfY-gY-hY-i)Y(-aY-bY-cY-dY-eY-fYgYhYi)'
Regla_triqui_vertical = '(aY-bY-cYdY-eY-fYgY-hY-i)Y(-aYbY-cY-dYeY-fY-gYhY-i)Y(-aY-bYcY-dY-eYfY-gY-hYi)'
Regla_triqui_diagonal = '(aY-bY-cY-dYeY-fY-gY-hYi)Y(-aY-bYcY-dYeY-fYgY-hY-i)'
Regla_cond_inicial = '(nYl)'

Regla_total = Regla_disponibilidad + 'Y' + Regla_triqui_horizon + 'Y' + Regla_triqui_vertical + 'Y' + Regla_triqui_diagonal + 'Y' + Regla_cond_inicial



###########################Dibujar_Tablero######################################

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
    
def tablero_Os(regla, tab):
    for c in regla:
        if c == 'j':
            tab[1] = 1
        elif c == 'k':
            tab[2] = 1 
        elif c == 'l':
            tab[3] = 1 
        elif c == 'm':
            tab[4] = 1
        elif c == 'n':
            tab[5] = 1 
        elif c == 'o':
            tab[6] = 1
        elif c == 'p':
            tab[7] = 1
        elif c == 'q':
            tab[8] = 1
        elif c == 'r':
            tab[9] = 1 
    return tab

x={1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0}
c={1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

tablero_Os(Regla_cond_inicial, c)

dibujar_tablero(x, c,121)
