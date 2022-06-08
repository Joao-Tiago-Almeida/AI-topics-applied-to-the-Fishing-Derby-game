import math
import random
import sys
EPSILON = sys.float_info.epsilon

def multiply(a, b):
    c =[[0] * len(b[0]) for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                c[i][j] += a[i][k] * b[k][j]
    #c = [[sum(i * j for i, j in zip(r, c)) for c in zip(*b)] for r in a]
    return c

def generate_matrix(n, m):
    base = 1.5/m
    mat = [[max(0, min(1, base + random.uniform(-base/2, base/2))) for _ in range(m)] for _ in range(n)]
    mat = [[max(0, min(1, base )) for _ in range(m)] for _ in range(n)]
    mat = [[el/sum(row) for el in row] for row in mat]
    return mat

class HMM:
    def __init__(self, N, M):
        self.A = generate_matrix(N, N)
        self.B = generate_matrix(N, M)
        self.pi = generate_matrix(1, N)
        self.n_states = N
        self.n_emissions = M
        self.fish_ids = []
        
    def alphaPass(self, o):
        # compute alpha(t=0)
        alpha = []
        c = []
        alpha.append([self.B[i][o[0]] * self.pi[0][i] for i in range(self.n_states)])
        c.append(1/(sum(alpha[-1]) + EPSILON))
        alpha[-1] = [a*c[-1] for a in alpha[-1]]
    
        # compute alpha(t)
        for t in range(1, len(o)):
            a = []
            ct = 0
            for i in range(self.n_states):
                s = 0
                for j in range(self.n_states):
                    s = s + self.A[j][i] * alpha[-1][j]
                at = self.B[i][o[t]] * s
                a.append(at)
                ct = ct + at
            c.append(1/(ct+EPSILON))
            alpha.append([al * c[-1] for al in a])
        return alpha, c
    
    def betaPass(self, o, c):
        betas = []
        betas.append([c[-1]]*self.n_states)
    
        for t in range(-2, -len(o)-1, -1):
            a = []
            for i in range(self.n_states):
                s = 0
                for j in range(self.n_states):
                    s = s + self.A[i][j] * betas[-1][j]*self.B[j][o[t+1]]
                s = c[t]*s
                a.append(s)
            betas.append(a)
        return list(reversed(betas))
    
    def computeGamma(self, o, alphas, betas):
        gammas = []
        digammas = {}
        for t in range(0, len(o)-1):
            gamma = []
            digammas_i = {}
            for i in range(self.n_states):
                s = 0
                digammas_j = {}
                for j in range(self.n_states):
                    digamma = alphas[t][i] * self.A[i][j]*self.B[j][o[t+1]]*betas[t+1][j]
                    s = s + digamma
                    digammas_j[j] = digamma
                gamma.append(s)
                digammas_i[i] = digammas_j
            gammas.append(gamma)
            digammas[t] = digammas_i
        gammas.append(alphas[-1])
        return gammas, digammas
    
    
    def reestimateModel(self, o, gammas, digammas):
        self.pi = [gammas[0]]
        for i in range(self.n_states):
            denom = 0
            for t in range(0, len(o)-1):
                denom = denom + gammas[t][i]
            for j in range(self.n_states):
                numer = 0
                for t in range(0, len(o) - 1):
                    numer = numer + digammas[t][i][j]
                self.A[i][j] = numer/(denom + EPSILON)
    
        for i in range(self.n_states):
            denom = 0
            for t in range(0, len(o)):
                denom = denom + gammas[t][i]
            for j in range(self.n_emissions):
                numer = 0
                for t in range(0, len(o)):
                    if o[t] == j:
                        numer = numer + gammas[t][i]
                self.B[i][j] = numer/(denom + EPSILON)
    
    def computeLogProb(self, c, o):
        logProb = 0
        for i in range(0, len(o)):
            logProb = logProb + math.log(c[i])
        return - logProb

    
    def train(self, o, maxIters=100):
        iters = 0
        oldLogProb = - float("inf")
        alphas, c = self.alphaPass(o)
        betas = self.betaPass(o, c)
        gammas, digammas = self.computeGamma(o, alphas, betas)
        self.reestimateModel(o, gammas, digammas)
        logProb = self.computeLogProb(c, o)
        iters += 1
        logProbs = [logProb]
        while True:
            if iters < maxIters and logProb > oldLogProb and not math.isclose(logProb, oldLogProb, rel_tol=0.00001, abs_tol=0.001):
                alphas, c = self.alphaPass(o)
                betas = self.betaPass(o, c)
                gammas, digammas = self.computeGamma(o, alphas, betas)
                self.reestimateModel(o, gammas, digammas)
                logProb = self.computeLogProb(c, o)
                iters += 1
                logProbs.append(logProb)
            else:
                return self.A, self.B, self.pi, logProbs

    def sequnceProbabilities(self, o):
        t = 0
        alpha = []
        alpha.append([self.B[i][o[t]] * self.pi[0][i] for i in range(len(self.B))])

        for t in range(1, len(o)):
            a = []
            for i in range(len(self.B)):
                s = 0
                for j in range(len(self.B)):
                    s = s + self.A[j][i] * alpha[-1][j]
                a.append(self.B[i][o[t]] * s)
            alpha.append(a)
        return sum(alpha[-1])

if __name__ == "__main__":
    model = HMM(3, 4)
    with open("/Users/kuba/PycharmProjects/AI/hmm_assignment/sample_data/hmm_c_N1000.txt") as f:
        lines = f.readlines()
    o = [int(i) for i in lines[0].split()]
    o = o[1:int(o[0]) + 1]
    model.pi = [[0.3, 0.2, 0.5]]
    model.A = [[0.54, 0.26, 0.20], [0.19, 0.53, 0.28], [0.22, 0.18, 0.6]]
    model.B = [[0.5, 0.2, 0.11, 0.19], [0.22, 0.28, 0.23, 0.27], [0.19, 0.21, 0.15, 0.45]]
    model.train(o)
    print(model.sequnceProbabilities(o[:10]))