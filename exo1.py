
#Liste des villes
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
