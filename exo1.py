
#Liste des villes
import math


villes = ["Paris", "Lille", "Nancy", "Grenoble", "Lyon", "Dijon", "Caen", "Rennes", "Nantes", "Bordeaux"]
#Matrice d'adjacence
A = [
    [-1 , 70, -1, -1, -1, 60, 50, 110, 80, 150],
    [70, -1, 100, -1, -1, 120, 65, -1, -1, -1],
    [-1, 100, -1, 80, 90, 75, -1, -1, -1, -1],
    [-1, -1, 80, -1, 40, 75, -1, -1, -1, -1],
    [-1, -1, 90, 40, -1, 70, -1, -1, -1, 100],
    [60, 120, 75, 75, 70, -1, -1, -1, -1,-1],
    [50, 65, -1, -1, -1, -1, -1, 75, -1, -1],
    [110, -1, -1, -1, -1, -1, 75, -1, 45, 130],
    [80, -1, -1, -1, -1, -1, -1, 45, -1, 90],
    [150, -1, -1, -1, 100, -1, -1, 130, 90, -1]
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

def shortest_path(algo, start):
    if algo == "BFS":
        return parcours_largeur(start)
    elif algo == "DFS":
        return parcours_profondeur(start)
    elif algo == "Bellman":
        return bellman(villes, villes[start])
    else:
        return ValueError("Algorithme non supporté")
    
def find(parent, i):
    while parent[i] != i:
        i = parent[i]
    return i

def union(parent, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    if root_x != root_y:
        parent[root_y] = root_x
        return True
    return False


def kruskal():
    list_edges = dict()
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != -1:
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


def floyd_one_intermediate(graph):
    """
    Version simplifiée de Floyd–Warshall :
    ne considère qu'un seul sommet intermédiaire maximum entre i et j.
    (i -> k -> j au plus)
    
    :param graph: matrice d'adjacence avec -1 pour les absences d’arêtes
    :return: matrice des plus courts chemins avec au plus 1 intermédiaire
    """
    n = len(graph)
    dist = [[math.inf] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    # Initialisation
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif graph[i][j] != math.inf:
                dist[i][j] = graph[i][j]
                next_node[i][j] = j

    # On teste uniquement les chemins passant par UN sommet intermédiaire
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if dist[i][k] != math.inf and dist[k][j] != math.inf:
                    new_dist = dist[i][k] + dist[k][j]
                    if new_dist < dist[i][j]:
                        dist[i][j] = new_dist
                        next_node[i][j] = k  # on garde l’intermédiaire

    return dist, next_node


def reconstruct_path_one_intermediate(i, j, next_node):
    """
    Reconstruit le chemin le plus court entre i et j
    pour la version à un seul intermédiaire maximum.
    """
    if next_node[i][j] is None:
        return [i, j]  # soit lien direct, soit inexistant
    return [i, next_node[i][j], j]

def Prim(start):
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
                    if not visite[v] and A[u][v]!=-1:
                        if A[u][v]<min_edge[0]:
                            min_edge=(A[u][v],u,v)
                            pere[v]=u
        edges.append((min_edge[1],min_edge[2],min_edge[0]))
        visite[min_edge[2]]=True
    return pere

def bellman(start):
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


def parcours_largeur(start):
    n = len(A)
    pere = {i: None for i in range(n)}
    visite = [False] * n

    voisin = [start]
    visite[start] = True

    while voisin:
        u = voisin.pop(0)  # on enlève le premier élément (file FIFO)
        for v in range(n):
            if A[u][v] != -1 and not visite[v]:
                visite[v] = True
                pere[v] = u
                voisin.append(v)
    return pere


def parcours_profondeur(start):
    n = len(A)
    pere = {i: None for i in range(n)}
    visite = [False] * n

    def dfs(u):
        visite[u] = True
        for v in range(n):
            if A[u][v] != -1 and not visite[v]:
                pere[v] = u
                dfs(v)

    dfs(start)
    return pere


def affichage_chemin(pere, villes, start):
    print(f"\nChemins depuis {villes[start]} :")
    for i in range(len(villes)):
        if i == start:
            continue
        chemin = []
        courant = i
        # On remonte jusqu'à la racine
        while courant is not None:
            chemin.insert(0, villes[courant])
            courant = pere[courant]
        if len(chemin) > 1:
            print(" → ".join(chemin))
        else:
            print(f"{villes[i]} : inaccessible depuis {villes[start]}")


if __name__ == "__main__":

    start = 0  # Paris

    pere_bfs = parcours_largeur(start)
    pere_dfs = parcours_profondeur(start)

    print("=== Parcours en largeur (BFS) ===")
    affichage_chemin(pere_bfs, villes, start)

    print("\n=== Parcours en profondeur (DFS) ===")
    affichage_chemin(pere_dfs, villes, start)


    print(bellman("Paris"))
    print(Prim(0))
    print(kruskal())

    matrice_test = [ 
        [0, 4, math.inf, math.inf, math.inf, 1],
        [math.inf, 0, math.inf, 5, math.inf, math.inf],
        [5, math.inf, 0, math.inf, math.inf, 2],
        [math.inf, math.inf, math.inf, 0, 3, 3],
        [math.inf, math.inf, 1, -2, 0, 4],
        [2, 2, math.inf, math.inf, math.inf, 0]
    ]

    dist, next_node = floyd_one_intermediate(matrice_test)
    print(dist)

# Exemple : chemin le plus court de 0 à 96
chemin = reconstruct_path_one_intermediate(0, 5, next_node)
print("Chemin 0 → 9 :", chemin)
