def parcours_largeur(A, start):
    n = len(A)
    pere = {i: None for i in range(n)}
    visite = [False] * n

    file = [start]
    visite[start] = True

    while file:
        u = file.pop(0)  # on enlève le premier élément (file FIFO)
        for v in range(n):
            if A[u][v] != -1 and not visite[v]:
                visite[v] = True
                pere[v] = u
                file.append(v)
    return pere


def parcours_profondeur(A, start):
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

    start = 0  # Paris

    pere_bfs = parcours_largeur(A, start)
    pere_dfs = parcours_profondeur(A, start)

    print("=== Parcours en largeur (BFS) ===")
    affichage_chemin(pere_bfs, villes, start)

    print("\n=== Parcours en profondeur (DFS) ===")
    affichage_chemin(pere_dfs, villes, start)
