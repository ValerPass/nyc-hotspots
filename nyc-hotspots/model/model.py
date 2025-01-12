import networkx as nx

from database.DAO import DAO
from geopy.distance import distance

class Model:
    def __init__(self):
        self._providers = DAO.getAllProvider()
        self.grafo = nx.Graph()
        self.idMap = {}

    def getAllProviders(self):
        return self._providers

    def buildGrafo(self, provider, soglia):
        #self._nodes = DAO.getAllLocations(provider)
        self._nodes = DAO.getLocationsOfProviderV2(provider)
        self.grafo.add_nodes_from(self._nodes)

        # Add Edges.
        # Modo 1: faccio una query che restituisce gli archi
        """
        allEdges = DAO.getAllEdges(provider)
        for edge in allEdges:
            l1 = edge[0]
            l2 = edge[1]
            dist = distance((l1.latitude, l1.longitude), (l2.latitude, l2.longitude)).km
            if dist < soglia:
                self.grafo.add_edge(l1.Location,l2.Location, weight = dist)
        """

        # Modo 2: Modifico il metodo del DAO che legge i nodi e ci aggiungo le coordinate (lat e lon) di ogni Location,
        # Dopo... doppio ciclo sui nodi e mi calcolo le distanze in Python
        for u in self._nodes:
            for v in self._nodes:
                if u != v:
                    dist = distance((u.latitude , u.longitude), (v.latitude, v.longitude)).km
                    if dist < soglia:
                        self.grafo.add_edge(u, v, weight=dist)

        # Modo 3: Doppio ciclo sui nodi e per ogni possibile arco faccio una query ---> meglio non farlo
        # (solo con tabelle molto piccole)

    def getGrafoDettagli(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    #ho lista di nodi voglio quelli con il maggiorn numero di vicini
    def getNodesMostVicini(self):
        listTuples = []
        for v in self._nodes:
            listTuples.append(((v, len(list(self.grafo.neighbors(v)))))) #faccio una lista di tuple con (nodo e numero
            # di vicini)
        listTuples.sort(key= lambda x: x[1], reverse=True) #la ordino per numero di vicini più alto

        #result1 = list(filter(lambda x: x[1] == listTuples[0][1], listTuples)) #filtro solo le tuple che hanno il
        #numero di vicini più alto
        result = [x for x in listTuples if x[1] == listTuples[0][1]]

        return result