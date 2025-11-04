import copy
import math

#Liste des villes
villes = ["Paris", "Lille", "Nancy", "Grenoble", "Lyon", "Dijon", "Caen", "Rennes", "Nantes", "Bordeaux"]
#Matrice d'adjacence
A = [
    [0, 70, 0, 0, 0, 60, 50, 110, 80, 150],
    [70, 0, 100, 0, 0, 120, 65, 0,0, 0],
    [0, 100, 0, 80, 90, 75, 0, 0, 0, 0],
    [0, 0, 80, 0, 40, 75, 0, 0, 0, 0],
    [0, 0, 90, 40, 0, 70, 0, 0, 0, 100],
    [60, 120, 75, 75, 70, 0, 0, 0, 0,0],
    [50, 65, 0, 0, 0, 0, 0, 75, 0, 0],
    [110, 0, 0, 0, 0, 0, 75, 0, 45, 130],
    [80, 0, 0, 0, 0, 0, 0, 45, 0, 90],
    [150, 0, 0, 0, 100,0, 0, 130, 90, 0]
]

A_oriente =  [
    [-1, 70, -1, -1, -1, 60, 50, 110, 80, 150],      
    [-1, -1, 100, -1, -1, 120, 65, -1, -1, -1],
    [-1, -1, -1, 80, 90, 75, -1, -1, -1, -1],
    [-1, -1, -1, -1, 40, 75, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 70, -1, -1, -1, 100],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 75, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 45, 130],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 90],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]


def shortest_path(algo, start, end=None):
    """_summary_
    Exécute l’algorithme choisi pour trouver un chemin ou un arbre couvrant.
    Args:
        algo (str): le nom de l’algorithme à exécuter
        start (int): indice de la ville de départ
        end (int, optional):l’indice de la ville d’arrivée (nécessaire pour Dijkstra).

    Returns:
        dict : un dictionnaire contenant les résultats de l’algorithme (chemins, coûts ou arêtes).
    """
    if algo == "BFS":
        pere = parcours_largeur(start)
        return {"algo": "BFS", "paths": pere}

    elif algo == "DFS":
        pere = parcours_profondeur(start)
        return {"algo": "DFS", "paths": pere}

    elif algo == "Bellman":
        pere = bellman(villes[start])
        return {"algo": "Bellman", "paths": pere}

    elif algo == "Kruskal":
        T = kruskal()
        edges = [{"from": u, "to": v, "weight": w} for (u, v, w) in T]
        return {"algo": "Kruskal", "edges": edges}

    elif algo == "Prim":
        pere = Prim(start)
        edges = [
            {"from": pere[i], "to": i}
            for i in range(len(pere))
            if pere[i] is not False
        ]
        return {"algo": "Prim", "edges": edges}

    elif algo == "Dijkstra":
        debut, fin = start, end
        dist, chemin_indices = dijkstra(A, start, fin)
        chemin_noms = [i for i in chemin_indices]
        return {"algo": "Dijkstra", "path": chemin_noms, "cost": dist}

    elif algo == "Floyd-Warshall":
        W = Warshall(A_oriente)
        return {"algo": "Floyd-Warshall", "matrix": W}

    else:
        return {"error": "Algorithme non supporté"}


    
def find(parent, i):
    """_summary_
    Fonction auxiliaire utilisée par Kruskal, appelée dans la fonction union
    Args:
        parent (list): tableau indiquant le parent de chaque sommet.
        i (_type_): _description_

    Returns:
        _type_: _description_
    """
    while parent[i] != i:
        i = parent[i]
    return i

def union(parent, x, y):
    """_summary_
    Fonction auxiliaire utilisée par Kruskal,

    Args:
        parent (list): _description_
        x (int): _description_
        y (int): _description_

    Returns:
        _type_: _description_
    """
    root_x = find(parent, x)
    root_y = find(parent, y)
    if root_x != root_y:
        parent[root_y] = root_x
        return True
    return False


def kruskal():
    """_summary_
    Implémente l’algorithme de Kruskal pour construire un arbre couvrant minimal.
    Returns:
        Liste :Correspond a l'ordre des sommets visités
    """
    list_edges = dict()
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                list_edges[(i, j)] = A[i][j]

    # Trier les arêtes par poids croissant
    sorted_edges = sorted(list_edges.items(), key=lambda x: x[1])
    print(sorted_edges)

    parent = [i for i in range(n)]  # initialisation des pères
    T = []  # arbre couvrant minimal

    for (u, v), w in sorted_edges:
        # Vérifier qu’on ne crée pas de cycle
        if union(parent, u, v):
            T.append((u, v, w))

    return T

def Prim(start):
    """_summary_
    Implémente l’algorithme de Prim pour construire un arbre couvrant minimal à partir d’un sommet donné.

    Paramètres :
    Args:
        start (int):  indice du sommet de départ.

    Returns:
        list: tableau représentant les arêtes de l’arbre couvrant minimal
    """
    n=len(A)
    visite=[False]*n
    visite[start]=True
    edges=[]
    pere=[False]*n
    for _ in range(n-1):
        min_edge=(math.inf,-1,-1)  # (poids, u, v)
        for u in range(n):
            if visite[u]:
                for v in range(n):
                    if not visite[v] and A[u][v]!=0:
                        if A[u][v]<min_edge[0]:
                            min_edge=(A[u][v],u,v)
                            pere[v]=u
        edges.append((min_edge[1],min_edge[2],min_edge[0]))
        visite[min_edge[2]]=True
    return pere

def bellman(start):
    """_summary_
    Implémente l’algorithme de Bellman-Ford pour trouver les plus courts chemins depuis une ville donnée.
    Args:
        start (int):  indice de la ville de départ.

    Returns:
          list : tableau des pères indiquant le chemin le plus court vers chaque sommet.
    """
    n=len(A_oriente)
    source = villes.index(start)
    dist = [math.inf]*n
    pere = [False]*n
    dist[source]=0    # la distance d'une ville a elle meme est 0
    for _ in range(n-1):     # on parcours n-1 fois pour eviter de creer un cycle 
            for a in range(n):
                  for b in range(n):
                        if (A_oriente[a][b] != -1) :
                              if (dist[a] +A_oriente[a][b] < dist[b]) :      # on regarde si le chemin de a à b etait deja le plus court ou pas
                                    dist[b] = dist[a]+ A_oriente[a][b]       # on met a jour le nouveau poids de la nouvelle aretes si un chemin plus cours est trouver 
                                    pere[b]= a 
                                
    if A_oriente[a][b] != -1 and dist[a] + A_oriente[a][b] < dist[b]:
            print ("il y a un cycle de poids négatif")
    return pere


def Warshall(A_oriente):
    """_summary_
    Implémente l’algorithme de Floyd-Warshall pour calculer les plus courtes distances entre toutes les paires de sommets.
    Args:
        A_oriente (list) : matrice d’adjacence orientée.

    Returns:
        list : matrice contenant les plus courtes distances entre chaque paire de sommets.
    """
    W = copy.deepcopy(A_oriente)
    n = len(W)
    pere = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j and W[i][j] != -1:
                pere[i][j] = i 
             
   
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if W[i][k] != -1 and W[k][j] != -1:
                    dist = W[i][k] + W[k][j]
                    if W[i][j] == -1 or dist < W[i][j]:
                        W[i][j] = dist
                        pere[i][j] = pere[i][k]

    return W

 
def dijkstra(A, debut, fin):
    """_summary_
    Implémente l’algorithme de Dijkstra pour trouver le plus court chemin entre deux villes.

    Args:
         A (list) : matrice d’adjacence du graphe.
        debut (int) : indice du sommet de départ.
        fin (int) : indice du sommet d’arrivée.

    Returns:
        tuple : (distance totale, liste des indices du chemin le plus court).
    """
    n = len(A)
    visit = [False]*n
    distance = [math.inf]*n
    pere = [None]*n
    distance[debut] = 0

    for _ in range(n):
        # Chercher le sommet non visité avec la distance minimale
        o = None
        distance_mini = math.inf
        for i in range(n):
            if not visit[i] and distance[i] < distance_mini:
                distance_mini = distance[i]
                o = i
        if o is None:
            break

        visit[o] = True

        for v in range(n):
            if A_oriente[o][v] > 0 and not visit[v]:
                nouv_dist = distance[o] + A_oriente[o][v]
                if nouv_dist < distance[v]:
                    distance[v] = nouv_dist
                    pere[v] = o

    # Reconstituer le chemin
    parcours = []
    s = fin
    while s is not None:
        parcours.insert(0, s)
        s = pere[s]

    return distance[fin], parcours

def parcours_largeur(start):
    """_summary_
    Implémente le parcours en largeur (BFS) à partir d’un sommet donné.
    Args:
       start (int) : indice du sommet de départ.
    Returns:
        dict : indique le sommet depuis lequel chaque nœud a été découvert.
    """
    n = len(A)
    pere = {i: None for i in range(n)}
    visite = [False] * n

    voisin = [start]
    visite[start] = True

    while voisin:
        u = voisin.pop(0)  # on enlève le premier élément (file FIFO)
        for v in range(n):
            if A[u][v] != 0 and not visite[v]:
                visite[v] = True
                pere[v] = u
                voisin.append(v)
    return pere


def parcours_profondeur(start):
    """_summary_
     Implémente le parcours en profondeur (DFS) à partir d’un sommet donné.
    Args:
      start (int) : indice du sommet de départ.

    Returns:
        dict : dictionnaire des pères représentant l’arbre du parcours en profondeur.
    """
    n = len(A)
    pere = {i: None for i in range(n)}
    visite = [False] * n

    def dfs(u):
        visite[u] = True
        for v in range(n):
            if A[u][v] != 0 and not visite[v]:
                pere[v] = u
                dfs(v)

    dfs(start)
    return pere


