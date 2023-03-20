import sys



class ProblemaP1():
    def __init__(self):
        self.readInput()

    """Función que lee los datos de entrada"""
    def readInput(self):
        
        #Primera línea -> Número de casos de prueba a analizar
        numero_casos = int(sys.stdin.readline())

        #Por cada caso de prueba se analiza una línea distinta...
        for __ in range(numero_casos):

            #Segunda línea -> Lista que contiene toda la la información de un caso particular
            case_list = list(map(int, sys.stdin.readline().split()))
            
            #Se obtiene el valor de k (Número de CAD's habilitados)
            k = case_list[0]

            #Se obtiene el número de familias diferentes
            m = case_list[1]            

            #Se obtiene el listado con el número de miembros de cada familia
            f = case_list[2:m+2]

            #Se verifica que la entrada ingresada sea válida
            self.checkValidity(k, m, f)

            #Se soluciona el problema
            self.CADPrepare(k, m, f)


    """Función que determina la validez de la entrada."""
    def checkValidity(self, k: int, m: int, f: list):
        if(k >= 2 and k <= 3 and m >= 2 and m <= 10**4 and all((i >= 1 and i <= 50 ) for i in f)):
            pass
        else:
            raise Exception("La entrada es incorrecta. Vuelva a intentar.")
        
    """Función que prepara los datos usados en el algoritmo de programación dinámica"""
    def CADPrepare(self, k: int, m: int, f: list):
        
        #Se suman todos los elementos para encontrar el número total de personas a organizar
        total_members = sum(f[0:m])

        #Si el número total de personas es divisible por k, siginifica que se pueden formar k grupos con ellos, de lo contrario
        #se retorna False
        if(total_members % 3 != 0):
            print(False)
            return 
        
        #Dividiendo por k la suma total, se encuentra el máximo número de personas que puede haber en cada grupo
        max_per_CAD = total_members // k

        #Se llama el algoritmo de programación dinámica que verfica los grupos
        self.CADAssign(k, m, f, max_per_CAD)

    
    """Función que determina si exise un sub-conjunto de familias cuya suma sea igual a k/3, de existir,
    se sabe existen k sub-conjuntos posibles con este tamaño"""
    def CADAssign(self, k: int, m: int, f:int, equal_sum: int):

        #Se crea el grafo de adyacencias como una matriz de tamaño (equal_sum + 1)*(m + 1)
        cadMatrix = [[False for j in range(equal_sum+1)] for i in range(m + 1)]

        #Se establece un caso de ayuda trivial en la primera columna (True)
        for i in range(m + 1):
            cadMatrix[i][0] = True

        #Se rellena el grafo de ayacencias de izquierda a derecha, fila por fila
        #Donde i -> Número de familias a considerar
        #Donde j -> Número de personas por CAD
        for i in range(m + 1):
            for j in range(equal_sum + 1):
                
                #Si, el número de miembros de una familia es mayor que la suma actual...
                if(f[i - 1] > j):
                    #Entonces ignorar a esa familia
                    cadMatrix[i][j] = cadMatrix[i-1][j]

                #De lo contrario...
                else:
                    #Evaluar si esa familia puede hacer parte del subconjunto o no
                    cadMatrix[i][j] = (cadMatrix[i-1][j] or cadMatrix[i-1][j - f[i - 1]])

        print(cadMatrix[m][equal_sum])


ProblemaP1()