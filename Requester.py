import requests

i = 10

while(i > 0):

	resp = requests.get("http://localhost:5000/").json()
	if resp['problema'] == 'ordenacao':
		print('Problema de ordenação')

	elif resp['problema'] == 'multiplicacao_matrizes':
		print('Problema de multiplicação')

	else:
		print('Problema de grafo')

	i -= 1
