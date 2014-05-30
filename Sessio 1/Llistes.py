def numElements(llista):
	cont = 0
	for x in llista:
		cont += 1
	return cont

def maxLlista(llista):
	max = llista[0]
	for x in llista:
		if max < x:
			max = x
	return max
def mitjanaLlista(llista):
	suma = 0
	for x in llista:
		suma += x
	print suma
	return float(suma) / numElements(llista)

def aplanarLlista(llista):
	result = []
	for x in llista:
		if hasattr(x, "__iter__") and not isinstance(x, basestring):
			result.extend(aplanarLlista(x))
		else:
			result.append(x)
	return result

def insertElemOrd(llista, val):
	llista.append(val)
	llista.sort()
	return llista

def parellSenar(llista):
	parells = []
	senars = []
	for x in llista:
		if x % 2 == 0:
			parells.append(x)
		else:
			senars.append(x)
	return parells, senars

if __name__ == '__main__':
	print numElements([1,2,3,4,5,62,1, 23456])
	print maxLlista([1,2,3,4,5,62,1, 23456])
	print mitjanaLlista([1,2,3,4,5,62,1, 23456])
	print aplanarLlista([3,[4,[],[5,3]],4,[2,1]])
	print insertElemOrd([1,2,3,4,5,62,1, 23456], 61)
	print parellSenar([1,2,3,4,5,62,1, 23456])