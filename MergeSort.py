def main():

	arr = [12, 11, 13, 5, 6, 7] 
	n = len(arr)
 
	print ("O vetor original ") 
	for i in range(n): 
    		print ("%d" %arr[i]), 
  
	mergeSort(arr,0,n-1) 

	print ("\n\nO vetor ordenado ") 
	for i in range(n): 
    		print ("%d" %arr[i])


def merge(arr, e, m, d):
	
	n1 = m - e + 1 #tamanho do array temporário esquerdo
	n2 = d - m #tamanho do array temporário direito

	#Criação dos arrays temporários
	arr_Temp_Esq = [0] * (round(n1))
	arr_Temp_Dir = [0] * (round(n2))


	#Copia as metades de arr para arrays temporários
	for i in range(0, n1):
		arr_Temp_Esq[i] = arr[e + i]
	
	for j in range(0, n2):
		arr_Temp_Dir[j] = arr[(m + 1) + j]

	i = 0
	j = 0
	k = e

	while i < n1 and j < n2: #primeiro preenchimento com comparação entre os arrays temporários
	
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
		
		m = (e + (d-1)) // 2 # o operador // faz com que a divisão resulte em um número inteiro

		mergeSort(arr, e, m)
		mergeSort(arr, m+1, d)
		merge(arr, e, m, d)


main()

	
	
