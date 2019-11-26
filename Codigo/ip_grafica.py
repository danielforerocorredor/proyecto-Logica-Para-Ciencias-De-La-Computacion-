import matplotlib
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

# ------------------------------TSEITIN-----------------------------------
def enFNC(A):
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]
    # print('p', p)
    if "-" in A:
        q = A[-1]
        # print('q', q)
        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')

    return B

def Tseitin(A, letrasProposicionalesA):
	letrasProposicionalesB = [chr(x) for x in range(256, 1200)]
	#assert(not bool(set(letrasProposicionalesA) & set(letrasProposicionalesB)))
	L = []
	Pila = [] # Inicializamos pila
	i = -1 # Inicializamos contador de variables nuevas
	s = A[0] # Inicializamos sımbolo de trabajo
	atomos = letrasProposicionalesA + letrasProposicionalesB
	while (len(A) > 0):
		#print('A', A, ' L', L, ' Pila', Pila, ' i', i, ' s', s)
		if s in atomos and len(Pila)>0 and Pila[-1] =='-':
			i += 1
			atomo = letrasProposicionalesB[i]
			Pila = Pila[:-1]
			Pila.append(atomo)
			L.append(atomo + '=' + '-' + s)
			A = A[1:]
			if len(A) > 0:
				s = A[0]

		elif s == ')':
			w = Pila[-1]
			O = Pila[-2]
			v = Pila[-3]
			Pila = Pila[:len(Pila)-4]
			i += 1
			atomo = letrasProposicionalesB[i]
			L.append(atomo +"="+"(" + v + O + w + ")")
			s = atomo

		else:
			Pila.append(s)

			A = A[1:]
			if len(A) > 0:
				s = A[0]
			#print('A', A)

	B = ""
	if i < 0:
		atomo = Pila[-1]
	else:
		atomo = letrasProposicionalesB[i]

	for x in L:
		y = enFNC(x)
		B += "Y" + y

	B = atomo + B
	return B

def Clausula(C):
    L=[]
    while len(C)>0:
        s=C[0]
        if s == "O":
            C=C[1:]
        elif s== "-":
            literal = s + C[1]
            L.append(literal)
            C = C[2:]
        else:
            L.append(s)
            C = C[1:]

    return L

# Algoritmo para obtencion de forma clausal
# Input: A (cadena) en notacion inorder en FNC
# Output: L (lista), lista de listas de literales
def formaClausal(A):
    l = []
    i = 0
    while len(A)> 0:
        if i >= len(A):
            l.append(Clausula(A))
            A = []
        else:
            if A[i] == 'Y':
                l.append(Clausula(A[:i]))
                A = A[i+1:]
                i = 0
            else:
                i+=1
    return l

# --------------------------------DPLL------------------------------------

def r1(S):
    for i in S:
        if len(i) == 1:
            return True
    return False
def r2(S,I):
    l = ""
    temp = ""
    I2 = I.keys()
    for i in S:
        for j in i:
            if len(j) != 1:
                temp = j[1]
            else:
                temp = j
            if temp not in I2:
                l = j
                print(l)
                for x in S:
                    if l in x:
                        print(x)
                        S.remove(x)

                if '-' not in l:
                    I[l] = 1
                    lc = '-' + l
                    for e in S:
                        if lc in e:
                            e.remove(lc)
                if '-' in l:
                    I[l[1]] = 0
                    lc = l[1]
                    for y in S:
                        if lc in y:
                            y.remove(lc)
                break

    return S,I


def unitPropagate(S,I):
    while(r1(S)==True):
        l = ""
        for x in S:
            if len(x) == 1:
                l = x[0]
                #print(l,x)
                S.remove(x)
                break

        if '-' in l:
            I[l[1]] = 0
            lc = l[1]
            for j in S:
                if l in j:
                    S.remove(j)
                if lc in j:
                    j.remove(lc)

        if '-' not in l:
            I[l] = 1
            lc = '-' + l
            for i in S:
                if l in i:
                    S.remove(i)
                if lc in i:
                    i.remove(lc)

        unitPropagate(S,I)


    return S,I


def DPLL(S,I):
    if r1(S):
        unitPropagate(S,I)


    if len(S)==1:
        x = S[0]
        for i in x:
            if i not in I.keys():
                l = i
                if '-' not in l:
                    I[l] = 1
                    S.remove(x)
                    break
                if '-' in l:
                    I[l[1]] = 0
                    S.remove(x)
                    break


    if [] in S:
        return "Insatisfacible", I
    if len(S) == 0:
        return "Satisfacible", I
    else:
        r2(S,I)
    return DPLL(S,I)

# ----------------------REPRESENTACIÓN GRÁFICA---------------------------

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
            ab = AnnotationBbox(imagebox, direcciones[int(l)], frameon = False)
            axes.add_artist(ab)

    for k in c:
        if c[k] != 0:
            if c[k] == x[k]:
                print("imposible ubicar O en la casilla "+ str(k) +" pues ya esta ocupada.")
            else:
                ab2 = AnnotationBbox(imagebox2, direcciones[int(k)], frameon = False)
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


# ------------------------------EJECUCION-----------------------------------

letrasProposicionalesA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r']
conectivos = ['O', 'Y', '>']

# ------------------------------REGLAS-----------------------------------

Regla_disponibilidad = '((((((((((((((((((j>-a)Y(k>-b))Y(l>-c))Y(m>-d))Y(n>-e))Y(o>-f))Y(p>-g))Y(q>-h))Y(r>-i))Y(a>-j))Y(b>-k))Y(c>-l))Y(d>-m))Y(e>-n))Y(f>-o))Y(g>-p))Y(h>-q))Y(i>-r))'
Regla_triqui_horizon = '((((aYb)Y((cY-d)Y((-eY-f)Y((-gY-h)Y-i)))))O((((-aY(-bY-c))Y(dYe))Y(fY-g))Y(-hY-i))O(-aY-bY-cY-dY-eY-fYgYhYi))'
Regla_triqui_vertical = '((((((aY(-bY-c))Y(dY-e))Y(-fYg))Y(-hY-i)))O(((((-aY(bY-c))Y(-dYe))Y(-fY-g))Y(hY-i)))O(((((-aY(-bYc))Y(-dY-e))Y(fY-g))Y(-hYi))))'
Regla_triqui_diagonal = '((((((aY(-bY-c))Y(-dYe))Y(-fY-g))Y(-hYi)))O(((((-aY(-bYc))Y(-dYe))Y(-fYg))Y(-hY-i))))'
Regla_cond_inicial = '(nYl)'

Regla_total = '((' + Regla_disponibilidad + ')Y(' + Regla_triqui_vertical + '))'



x={1:1, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0}
c={1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

tablero_Os(Regla_cond_inicial, c)
dibujar_tablero(x, c,121)

# formula = Tseitin(Regla_triqui_diagonal, letrasProposicionalesA)
# print(formula)
# print('\n')
#
# formula2 = formaClausal(formula)
# print(formula2)

# formula2 = Tseitin(Regla_triqui_vertical, letrasProposicionalesA)
# print(formula2)
# print('\n')
#
# formula3 = Tseitin(Regla_triqui_horizon, letrasProposicionalesA)
# print(formula3)
# print('\n')
#
formula = Tseitin(Regla_triqui_diagonal, letrasProposicionalesA)
print(formula)
print('\n')

formula2 = formaClausal(formula)
print(formula2)
print('\n')

y = {}
formula3 = DPLL(formula2, y)
print(formula3)
print('\n')


# formula_Final = Tseitin(Regla_total, letrasProposicionalesA)
# print(formula_Final)
