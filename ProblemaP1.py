import sys


class ProblemaP1():
    def __init__(self):

        # Variable global que almacena el resultado de cada prueba
        # (Se reinicia cuando finaliza la prueba)
        self.cad_final = []

        self.readInput()

    """Función que lee los datos de entrada"""
    def readInput(self):

        # Primera línea -> Número de casos de prueba a analizar
        numero_casos = int(sys.stdin.readline())

        # Por cada caso de prueba se analiza una línea distinta...
        for __ in range(numero_casos):

            # Segunda línea -> Lista que contiene toda la la información
            #  de un caso particular
            case_list = list(map(int, sys.stdin.readline().split()))

            # Se obtiene el valor de k (Número de CAD's habilitados)
            k = case_list[0]

            # Se obtiene el número de familias diferentes
            m = case_list[1]           

            # Se obtiene el listado con el número de miembros de cada familia
            f = case_list[2:m+2]

            # Se soluciona el problema
            self.CADPrepare(k, m, f)

            # Se imprime el resultado de la prueba y se resetea dicho campo
            if not self.cad_final:
                print(False)
            else:
                print(True, self.cad_final)
            self.cad_final = []

    """Función que prepara los datos usados en el
        algoritmo de programación dinámica"""
    def CADPrepare(self, k: int, m: int, f: list):

        # Se suman todos los elementos para encontrar el número
        # total de personas a organizar
        total_members = sum(f[0:m])

        # Si el número total de personas es divisible por k, siginifica que se
        # pueden formar k grupos con ellos, de lo contrario se retorna False
        if total_members % k != 0:
            print(False)
            return

        # Dividiendo por k la suma total, se encuentra el máximo número
        # de personas que puede haber en cada grupo
        max_per_CAD = total_members // k

        # Se llama el algoritmo de programación dinámica que verfica los grupos
        self.CADAssign(k, m, f, max_per_CAD)

    """Función que determina si exise un sub-conjunto de familias cuya suma
       sea igual a total_sum/k, de existir,
       se sabe existen k sub-conjuntos posibles con este tamaño"""
    def CADAssign(self, k: int, m: int, f: int, equal_sum: int):

        # Se crea el grafo de adyacencias como una
        # matriz de tamaño (equal_sum + 1)*(m + 1)
        cadMatrix = [[False for j in range(equal_sum+1)] for i in range(m + 1)]

        # Se rellena el grafo de ayacencias de izquierda a derecha:
        # Donde i -> Número de familias a considerar
        # Donde j -> Número de personas por CAD
        for i in range(m + 1):
            for j in range(equal_sum + 1):

                # Caso Base #1: i = 0 (Excepto para i = 0 y j = 0)
                if (i == 0 and j != 0):
                    cadMatrix[i][j] = False

                # Caso Base #2: j = 0
                elif (j == 0):
                    cadMatrix[i][j] = True

                # Si el número de miembros de una familia es mayor que la suma
                elif (f[i - 1] > j):
                    # Entonces ignorar a esa familia
                    cadMatrix[i][j] = cadMatrix[i-1][j]

                # De lo contrario...
                else:
                    # Evaluar si esa familia puede hacer parte del subconjunto
                    cadMatrix[i][j] = (cadMatrix[i-1][j] or
                                       cadMatrix[i-1][j - f[i - 1]])

        self.CADgroups(cadMatrix, m, equal_sum, f, k)

    def CADgroups(self, cadMatrix: list, m: int, equal_sum: int,
                  f: list, k: int):

        # Subgrupos temporales encontrados
        cad_1 = []
        cad_2 = list.copy(f)

        # Variable temporal de búsqueda
        group_sum = equal_sum

        # Se revisa que el algoritmo haya encontrado que
        # efectivamente se pueden formar los grupos
        if (cadMatrix[m][equal_sum]):

            # Se va hacía atrás en la matriz para encontrar el subgrupo
            #  particular encontrado por el algoritmo
            while group_sum > 0:
                if (cadMatrix[m][group_sum - f[m-1]]):
                    cad_1.append(f[m - 1])
                    cad_2.pop(m - 1)
                    group_sum -= f[m - 1]

                m -= 1

            # Se añade el grupo encontrado por el algoritmo
            self.cad_final.append(cad_1)

            # Se revisa si el valor de k es mayor que 2, en dado caso,
            # con la sub-lista cad_2 será necesario ver
            # si esta se puede descomponer
            if k > 2:

                sub_k = k-1  # Pues ya se ha despejado un conjunto
                sub_m = len(cad_2)  # Nueva lista de familias sin asignar
                sub_f = cad_2
                sub_max_per_cad = equal_sum   # La suma debe ser igual

                self.CADAssign(sub_k, sub_m, sub_f, sub_max_per_cad)
            else:
                # Se añade el grupo complementario
                self.cad_final.append(cad_2)

        else:
            # De lo contrario, se determina que el cad_final es falso
            self.cad_final = False


ProblemaP1()
