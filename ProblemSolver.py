import requests
import json

#=========================================================================


def merge(arr, e, m, d):

    n1 = m - e + 1  # tamanho do array temporario esquerdo
    n2 = d - m  # tamanho do array temporario direito

    # Criacao dos arrays temporarios
    arr_Temp_Esq = [0] * (n1)
    arr_Temp_Dir = [0] * (n2)

    # Copia as metades de arr para arrays temporarios
    for i in range(0, n1):
        arr_Temp_Esq[i] = arr[e + i]

    for j in range(0, n2):
        arr_Temp_Dir[j] = arr[(m + 1) + j]

    i = 0
    j = 0
    k = e

    while i < n1 and j < n2:  # primeiro preenchimento com comparacao entre os arrays temporarios

        if arr_Temp_Esq[i] <= arr_Temp_Dir[j]:

            arr[k] = arr_Temp_Esq[i]
            i += 1

        else:

            arr[k] = arr_Temp_Dir[j]
            j += 1

        k += 1

    while i < n1:
        arr[k] = arr_Temp_Esq[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = arr_Temp_Dir[j]
        j += 1
        k += 1


def mergeSort(arr, e, d):

    if e < d:

        # o operador // faz com que a divisao resulte em um numero inteiro
        m = (e + (d - 1)) // 2

        mergeSort(arr, e, m)
        mergeSort(arr, m + 1, d)
        merge(arr, e, m, d)


#=========================================================================

def melhor_ordem(lista_matrizes):
    """Calcula a matriz com melhor forma de multiplicar."""
    if len(lista_matrizes) > 2:
        dim = []
        for index in range(0, len(lista_matrizes)):
            # Gera a lista com as dimensoes das matrizes
            if index == 0:
                dim.append(lista_matrizes[index]['linhas'])
                dim.append(lista_matrizes[index]['colunas'])
            else:
                dim.append(lista_matrizes[index]['colunas'])

        n_dim = len(dim)
        matriz_temp = []
        matriz_saida = []

        for i in range(0, n_dim):
            matriz_saida.append([0 for _ in range(0, n_dim)])
            matriz_temp.append([0 for _ in range(0, n_dim)])

        # Calcula a matriz saida
        for d in range(1, n_dim):
            for i in range(1, n_dim - d):
                j = i + d
                for k in range(i, j):
                    q = matriz_temp[i][k] + matriz_temp[k + 1][j] +\
                        dim[i - 1] * dim[k] * dim[j]
                    if matriz_temp[i][j] == 0 or q < matriz_temp[i][j]:
                        matriz_temp[i][j] = q
                        matriz_saida[i][j] = k
        return matriz_saida

    return None


def array_ordem_mult(i, j, mo, saida):
    """
    Converte a matriz saida em um array informando o indice
    das matrizes na ordem que serao multiplicadas.
    """
    if i == j:
        return i - 1
    else:
        s1 = array_ordem_mult(mo[i][j] + 1, j, mo, saida)
        s2 = array_ordem_mult(i, mo[i][j], mo, saida)
        saida.append(s1)
        saida.append(s2)


def prodMatriz(matrizA, matrizB):
    """Multiplica duas matrizes."""
    if isinstance(matrizA, dict):
        matrizA = matrizA['matriz']
    if isinstance(matrizB, dict):
        matrizB = matrizB['matriz']

    sizeLA = len(matrizA)
    sizeCA = len(matrizA[0])
    sizeCB = len(matrizB[0])
    matrizR = []

    for i in range(sizeLA):
        matrizR.append([])
        for j in range(sizeCB):
            val = 0
            for k in range(sizeCA):
                val += matrizA[i][k] * matrizB[k][j]
            matrizR[i].append(val)
    return matrizR


def executarOrdem(ordem, matrizes):
    """Executa a multiplicacao na ordem calculada."""
    if ordem[0] < ordem[1] and\
            matrizes[ordem[0]]['colunas'] == matrizes[ordem[1]]['linhas']:
        resultante = prodMatriz(matrizes[ordem[0]], matrizes[ordem[1]])
    else:
        resultante = prodMatriz(matrizes[ordem[1]], matrizes[ordem[0]])

    for index in range(2, len(ordem)):
        if len(resultante[0]) == matrizes[ordem[index]]['linhas'] and\
                len(resultante) == matrizes[ordem[index]]['colunas']:
            r1 = (len(resultante), matrizes[ordem[index]]['colunas'])
            r2 = (matrizes[ordem[index]]['linhas'], len(resultante[0]))

            if index + 1 == len(ordem):
                aux = index
            else:
                aux = index + 1

            if r1[1] in (matrizes[ordem[aux]]['linhas'],
                         matrizes[ordem[aux]]['colunas']):
                resultante = prodMatriz(resultante, matrizes[ordem[index]])
            else:
                resultante = prodMatriz(matrizes[ordem[index]], resultante)

        elif len(resultante[0]) == matrizes[ordem[index]]['linhas']:
            resultante = prodMatriz(resultante, matrizes[ordem[index]])
        else:
            resultante = prodMatriz(matrizes[ordem[index]], resultante)

    return resultante


def multiplicar_matrizes(matrizes):
    """Inicia a multiplicacao das matrizes."""
    mo = melhor_ordem(matrizes)

    if mo is not None:
        out = []
        array_ordem_mult(1, len(mo) - 1, mo, out)
        mo = filter(lambda x: x is not None, out)
    else:
        mo = [0, 1]

    return executarOrdem(mo, matrizes)


#=========================================================================

def main():

    while(True):

        resp = requests.get('http://localhost:5000/').json()

        if resp['problema']['tipo'] == 'ordenacao':

            mergeSort(
                resp['problema']['elementos'], 0, resp['problema']['n'] - 1)
            json_resp = json.dumps(resp)  # parser para JSON

            requests.post('http://localhost:5000/solucao',
                          data=json_resp)  # retorna

        elif resp['problema']['tipo'] == 'multiplicacao_matrizes':
            resp['problema']['solucao'] = multiplicar_matrizes(
                resp['problema']['matrizes'])

            requests.post('http://localhost:5000/solucao',
                          data=json.dumps(resp))

        else:

            print('Problema de grafo')


#=========================================================================

main()
