from math import sin
import macierze
import matplotlib.pyplot as plt
import time

def generuj_A(a1,a2,a3,N):
    A = [[0]*N for _ in range(N)]
    for i in range(N):
        A[i][i] = a1
    for i in range(N-1):
        A[i][i+1] = a2
        A[i+1][i] = a2
    for i in range(N-2):
        A[i+2][i] = a3
        A[i][i+2] = a3
    return A
def generuj_b(f,N):
    b = [[0] for _ in range(N)]
    for n in range(N):
        b[n][0] = sin(n*(f+1))
    return b
def gauss(A,b):
    L = macierze.lower(A)
    U = macierze.upper(A)
    D = macierze.diag(A)
    # gauss - siedl method
    LD = macierze.dodaj(L, D)
    norm = 10
    normy = []
    x = [[1] for _ in range(N)]
    liczba_iter = 0
    czas = time.perf_counter()
    while norm > 10 ** -9 and liczba_iter < 100:
        temp = macierze.mnozenie(U, x)
        temp = macierze.odejmij(b, temp)
        x = macierze.forwardSubstitution(LD, temp)
        res = macierze.mnozenie(A, x)
        res = macierze.odejmij(res, b)
        norm = macierze.norma(res)
        liczba_iter += 1
        normy.append(norm)
    czas = time.perf_counter() - czas
    print("liczba iteracji:" + str(liczba_iter))
    return liczba_iter,czas, normy
def jacobi(A,b):
    L = macierze.lower(A)
    U = macierze.upper(A)
    D = macierze.diag(A)
    norm = 10
    normy = []
    liczba_iter = 0
    x = [[1] for _ in range(N)]
    LU = macierze.dodaj(L, U)
    czas = time.perf_counter()
    temp2 = macierze.odwrotnaDiag(D)
    while norm > 10 ** -9 and liczba_iter < 100:
        temp = macierze.mnozenie(LU, x)
        temp = macierze.odejmij(b, temp)
        x = macierze.mnozenie(temp2, temp)
        res = macierze.mnozenie(A, x)
        res = macierze.odejmij(res, b)
        norm = macierze.norma(res)
        liczba_iter += 1
        normy.append(norm)
    czas = time.perf_counter() - czas
    print("liczba iteracji:" + str(liczba_iter))
    return liczba_iter,czas ,normy
def LUsolve(A,b):
    czas = time.perf_counter()
    L,U = macierze.LUdecomposition(A)
    temp = macierze.forwardSubstitution(L,b)
    x = macierze.backwardSubstitution(U,temp)
    czas = time.perf_counter() - czas
    res = macierze.mnozenie(A, x)
    res = macierze.odejmij(res, b)
    norm = macierze.norma(res)
    print(norm)
    return czas

if __name__ == '__main__':
    e = 5
    a1 = 5+e
    a2 = a3 = -1
    N = 967
    A = generuj_A(a1,a2,a3,N)
    f = 8
    b = generuj_b(8,N)
    #task B
    liczba_iter,czas,normy = gauss(A,b)
    print(czas)
    plt.plot(normy)
    plt.title("zadanie B")
    plt.ylabel("norma błędu")
    plt.xlabel("iteracje")
    print("----------")
    liczba_iter,czas,normy = jacobi(A,b)
    print(czas)
    plt.plot(normy)
    plt.yscale("log")
    plt.legend(["Gauss-Seidl","Jacobi"])
    plt.show()
    print("\n\n\n\n")
    #task C
    e = 5
    a1 = 3
    a2 = a3 = -1
    N = 967
    A = generuj_A(a1, a2, a3, N)
    f = 8
    b = generuj_b(8, N)
    liczba_iter,czas,normy = gauss(A,b)
    print(czas)
    plt.plot(normy)
    plt.title("zadanie C")
    plt.ylabel("norma błędu")
    plt.xlabel("iteracje")
    print("----------")
    liczba_iter,czas,normy = jacobi(A,b)
    print(czas)
    plt.plot(normy)
    plt.yscale("log")
    plt.legend(["Gauss-Seidl", "Jacobi"])
    plt.show()
    #LU faktoryzacja - task D
    czas = LUsolve(A,b)
    print(czas)

    #task E
    czasyG = []
    czasyJ = []
    czasyLU = []
    Nki = [100,500,1000,1500,2000,2500]
    for N in Nki:
        e = 5
        a1 = 5 + e
        a2 = a3 = -1
        A = generuj_A(a1, a2, a3, N)
        f = 8
        b = generuj_b(8, N)
        liczba_iter, czas, normy = gauss(A, b)
        czasyG.append(czas)
        liczba_iter, czas, normy = jacobi(A, b)
        czasyJ.append(czas)
        czas = LUsolve(A,b)
        czasyLU.append(czas)
    plt.plot(Nki,czasyG)
    plt.plot(Nki,czasyJ)
    plt.plot(Nki,czasyLU)
    plt.xlabel("rozmiar macierzy")
    plt.ylabel("czas wykonania[s]")
    plt.legend(["Gauss-Seidl","Jacobi","Faktoryzacja LU"])
    plt.title("zadanie E")
    plt.show()
