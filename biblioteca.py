from grafo import Grafo
from tdas import Cola, Pila
from heapq import heapify, heappush, heappop #Heappush encola, heappop desencola del heap
import random

INFINITO = float("inf")

def centralidad_biblioteca(grafo):
	cent = {}
	for v in grafo:
		cent[v] = 0
	for v in grafo:
		distancias, padres = dijkstra(grafo, v, None, 2, True)
		cent_aux = {}
		for w in grafo:
			cent_aux[w] = 0
		vertices_ordenados = sorted(distancias, key=lambda i: distancias[i]) #Ordeno el diccionario de distancias por valores
		vertices_ordenados.reverse() 
		for w in vertices_ordenados:
			if not padres[w]:
				continue
			cent_aux[padres[w]] += 1 + cent_aux[w]
		for w in grafo:
			if w == v:
				continue
			cent[w] += cent_aux[w]
	return cent

def ciclo_vacaciones(grafo, origen, v, visitados, n, corte):
	print(visitados)
	if corte > n:
		return False
	if v in visitados:
		return False
	visitados.append(v)
	if corte == n :
		return True
	for w in grafo.adyacentes(v):
		if w not in visitados:
			if corte == n - 1:
				if origen not in grafo.adyacentes(w):
					break
			corte += 1
			if ciclo_vacaciones(grafo, origen, w, visitados, n, corte):
				return True
	visitados.remove(v)
	return False

def _random_walk(grafo, n, i, recorrido, origen):
	if i >= n:
		return
	recorrido.append(origen)
	proximo = random.choice(grafo.adyacentes(origen))
	_random_walk(grafo, n, i + 1, recorrido, proximo)

def random_walk(grafo, n):
	origen = grafo.vertice_random()
	recorrido = []
	_random_walk(grafo, n, 0, recorrido, origen)
	return recorrido

def mst_prim(grafo):
	"""Recibe un grafo y devuelve un arbol de tendido minimo"""
	v = grafo.vertice_random()
	visitados = set()
	visitados.add(v)
	q = []
	mst = Grafo(True)
	for u in grafo:
		mst.agregar_vertice(u)
	for w in grafo.adyacentes(v):
		heappush(q, ((grafo.peso(v, w))[1], v, w))
	while len(q) > 0:
		peso, v, w = heappop(q)
		if w in visitados:
			continue
		mst.agregar_arista(v, w, grafo.peso(v, w))
		visitados.add(w)
		for x in grafo.adyacentes(w):
			if x not in visitados:
				heappush(q, ((grafo.peso(w, x))[1], w, x))
	return mst

def pila_a_lista(pila):
	lista = []
	while not pila.esta_vacia():
		elemento = pila.desapilar()
		lista.append(elemento)
	return lista

def orden_topologico_dfs(grafo, v, pila, visitados):
	visitados.add(v)
	for w in grafo.adyacentes(v):
		if w not in visitados:
			orden_topologico_dfs(grafo, w, pila, visitados)
	pila.apilar(v)

def orden_topologico(grafo):
	visitados = set()
	pila = Pila()
	for v in grafo:
		if v not in visitados:
			orden_topologico_dfs(grafo, v, pila, visitados)
	return pila_a_lista(pila)

def bfs(grafo, origen, destino):
	visitados = set()
	padres = {}
	orden = {}
	cola = Cola()
	visitados.add(origen)
	padres[origen] = None
	orden[origen] = 0
	cola.encolar(origen)
	while not cola.esta_vacia():
		v = cola.desencolar()
		if destino:
			if v == destino:
				break
		for w in grafo.adyacentes(v):
			if w not in visitados:
				visitados.add(w)
				padres[w] = v
				orden[w] = orden[v] + 1
				cola.encolar(w)
	return padres, orden

def dijkstra(grafo, origen, destino, peso, calculo_centralidad):
	dist = {}
	padre = {}
	for v in grafo: 
		dist[v] = INFINITO
	dist[origen] = 0
	padre[origen] = None
	q = [] #Este seria mi "heap"
	heappush(q, (dist[origen], origen))
	while len(q) > 0:
		distancia_v, v = heappop(q)
		if destino == v:
			break
		for w in grafo.adyacentes(v):
			if not calculo_centralidad:
				if dist[w] == INFINITO or dist[v] + (grafo.peso(v, w))[peso] < dist[w]:
					dist[w] = dist[v] + (grafo.peso(v, w))[peso]
					padre[w] = v
					heappush(q, (dist[w], w))
			if calculo_centralidad:
				sumando = (1 / grafo.peso(v, w)[peso])
				if distancia_v + sumando < dist[w]:
					dist[w] = distancia_v + sumando
					padre[w] = v
					heappush(q, (dist[w], w))
	return dist, padre
