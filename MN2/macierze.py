import math
from copy import deepcopy

def dodaj(A,B):
    wynik = [[0]*len(A[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            wynik[i][j] = A[i][j] + B[i][j]
    return wynik
def odejmij(A,B):
    wynik = [[0]*len(A[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            wynik[i][j] = A[i][j] - B[i][j]
    return wynik

def lower(A):
    L = [[0]*len(A) for _ in range(len(A))]
    for i in range(1,len(A)):
        for j in range(len(A) - (len(A) - i)):
            L[i][j] = A[i][j]
    return L
def upper(A):
    U = [[0]*len(A) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(i+1,len(A)):
            U[i][j] = A[i][j]
    return U
def diag(A):
    D = [[0] * len(A) for _ in range(len(A))]
    for i in range(len(A)):
        D[i][i] = A[i][i]
    return D

def mnozenie(A,B):
    wynik = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for n in range(len(B)):
                wynik[i][j] += A[i][n]*B[n][j]
    return wynik

def forwardSubstitution(A,b):
    x = [[0] for _ in range(len(b))]
    for i in range(len(b)):
        x[i][0]+=b[i][0]
        for j in range(len(A[0]) - (len(A[0])-i)):
            x[i][0] -= A[i][j]*x[j][0]
        x[i][0] /= A[i][i]
    return x
def backwardSubstitution(A,b):
    x = [[0] for _ in range(len(b))]
    n = len(b)
    for i in range(n):
        x[n - 1 - i][0] += b[n - 1-i][0]
        m = len(A[0])
        for j in range(m - (m-i)):
            x[n - 1 - i][0] -= A[n- 1 - i][m - 1 - j]*x[n - 1 - j][0]
        x[n - i- 1][0] /= A[n-i- 1][n-i- 1]
    return x

def norma(A):
    wynik = 0
    for i in range(len(A)):
        wynik += A[i][0] * A[i][0]
    wynik = math.sqrt(wynik)
    return wynik

def odwrotnaDiag(D):
    wynik = [[0]*len(D) for _ in range(len(D))]
    for i in range(len(D)):
        wynik[i][i] = 1/D[i][i]
    return wynik

def LUdecomposition(A):
    n = len(A)
    L = [[0 for x in range(n)]
             for y in range(n)]
    for i in range(n):
        L[i][i] = 1
    U = deepcopy(A)
    for k in range(n-1):
        for j in range(k+1,n):
            L[j][k] = U[j][k]/U[k][k]
            for i in range(k,n):
                U[j][i] = U[j][i] - L[j][k]*U[k][i]
    return L,U



