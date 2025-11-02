
#Liste des villes
import math
import copy 


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

def shortest_path(algo, start):
    if algo == "BFS":
        return parcours_largeur(start)
    elif algo == "DFS":
        return parcours_profondeur(start)
    elif algo == "Bellman":
        return bellman(villes, villes[start])
    else:
        return ValueError("Algorithme non supporté")
    
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


def Warshall(A_oriente):
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
            if A[o][v] > 0 and not visit[v]:
                nouv_dist = distance[o] + A[o][v]
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





        

               

def shortest_path(algo, start):
    if algo == "BFS":
        return parcours_largeur(start)
    elif algo == "DFS":
        return parcours_profondeur(start)
    else:
        return ValueError("Algorithme non supporté")

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
    print(Warshall(A_oriente))
    debut_nom = "Bordeaux"
    fin_nom = "Caen"
    debut = villes.index(debut_nom)
    fin = villes.index(fin_nom)

    # Calcul Dijkstra
    dist, chemin_indices = dijkstra(A, debut, fin)
    chemin_noms = [villes[i] for i in chemin_indices]

    print("Chemin:", chemin_noms)
    print("Distance:", dist)

