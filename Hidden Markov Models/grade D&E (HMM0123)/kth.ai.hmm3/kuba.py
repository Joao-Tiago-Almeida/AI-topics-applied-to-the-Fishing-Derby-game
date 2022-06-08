import math
import matplotlib.pyplot as plt

def createMatrix(line):
    rowCount = int(line[0])
    colCount = int(line[1])
    data = line[2:rowCount * colCount + 2]
    mat = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            rowList.append(data[colCount * i + j])
        mat.append(rowList)
    return mat


def multiply(a, b):
    c = [[0] * len(b[0])] * len(a)
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                c[i][j] += a[i][k] * b[k][j]
    return c


def alphaPass(A, B, pi, o):
    # compute alpha(t=0)
    alpha = []
    c = []
    alpha.append([B[i][o[0]] * pi[0][i] for i in range(len(B))])
    c.append(1/sum(alpha[-1]))
    alpha[-1] = [a*c[-1] for a in alpha[-1]]

    # compute alpha(t)
    for t in range(1, len(o)):
        a = []
        ct = 0
        for i in range(len(B)):
            s = 0
            for j in range(len(B)):
                s = s + A[j][i] * alpha[-1][j]
            at = B[i][o[t]] * s
            a.append(at)
            ct = ct + at
        c.append(1/ct)
        alpha.append([al * c[-1] for al in a])
    return alpha, c

def betaPass(A, B, pi, o, c):
    betas = []
    betas.append([c[-1]]*len(B))

    for t in range(-2, -len(o)-1, -1):
        a = []
        for i in range(len(B)):
            s = 0
            for j in range(len(B)):
                s = s + A[i][j] * betas[-1][j]*B[j][o[t+1]]
            s = c[t]*s
            a.append(s)
        betas.append(a)
    return list(reversed(betas))

def computeGamma(A, B, o, alphas, betas):
    gammas = []
    digammas = {}
    for t in range(0, len(o)-1):
        gamma = []
        digammas_i = {}
        for i in range(len(B)):
            s = 0
            digammas_j = {}
            for j in range(len(B)):
                digamma = alphas[t][i] * A[i][j]*B[j][o[t+1]]*betas[t+1][j]
                s = s + digamma
                digammas_j[j] = digamma
            gamma.append(s)
            digammas_i[i] = digammas_j
        gammas.append(gamma)
        digammas[t] = digammas_i
    gammas.append(alphas[-1])
    return gammas, digammas

def reestimateModel(A, B, o, gammas, digammas):
    pi = [gammas[0]]
    for i in range(len(B)):
        denom = 0
        for t in range(0, len(o)-1):
            denom = denom + gammas[t][i]
        for j in range(len(B)):
            numer = 0
            for t in range(0, len(o) - 1):
                numer = numer + digammas[t][i][j]
            A[i][j] = numer/denom

    for i in range(len(B)):
        denom = 0
        for t in range(0, len(o)):
            denom = denom + gammas[t][i]
        for j in range(len(B[0])):
            numer = 0
            for t in range(0, len(o)):
                if o[t]==j:
                    numer = numer + gammas[t][i]
            B[i][j] = numer/denom
    return A, B, pi

def computeLogProb(c, o):
    logProb = 0
    for i in range(0, len(o)):
        logProb = logProb + math.log(c[i])
    return - logProb



def train(A, B, pi, o, maxIters=100):
    iters = 0
    oldLogProb = - float("inf")
    alphas, c = alphaPass(A, B, pi, o)
    betas = betaPass(A, B, pi, o, c)
    gammas, digammas = computeGamma(A, B, o, alphas, betas)
    A, B, pi = reestimateModel(A, B, o, gammas, digammas)
    logProb = computeLogProb(c, o)
    iters += 1
    logProbs = [logProb]
    while True:
        if iters < maxIters and logProb > oldLogProb and not math.isclose(logProb, oldLogProb, abs_tol = 0.001):
            alphas, c = alphaPass(A, B, pi, o)
            betas = betaPass(A, B, pi, o, c)
            gammas, digammas = computeGamma(A, B, o, alphas, betas)
            A, B, pi = reestimateModel(A, B, o, gammas, digammas)
            oldLogProb = logProb
            logProb = computeLogProb(c, o)
            iters += 1
            logProbs.append(logProb)
        else:
            print(logProbs)
            return A, B, pi, logProbs
# def read():
#     A = [float(i) for i in input().split()]
#     A = createMatrix(A)
#     B = [float(i) for i in input().split()]
#     B = createMatrix(B)
#     pi = [float(i) for i in input().split()]
#     pi = createMatrix(pi)
#     o = [int(i) for i in input().split()]
#     o = o[1:int(o[0])+1]
#     return A, B, pi, o

A = [4.0, 4.0, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4]
B = [4.0, 4.0, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4]
pi = [1.0, 4.0, 0.241896, 0.266086, 0.249153, 0.242864]
o = [1000.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0]

A, B, pi, o = createMatrix(A), createMatrix(B), createMatrix(pi), [int(o[value]) for value in range(1, len(o))]
maxIters = 100
A, B, pi, logProbs = train(A, B, pi, o, maxIters)
elem = [round(x, 6) for row in A for x in row]
print(str(len(A)), str(len(A[0])), ' '.join([str(x) for x in elem]))
elem = [round(x, 6) for row in B for x in row]
print(str(len(B)), str(len(B[0])), ' '.join([str(x) for x in elem]))
