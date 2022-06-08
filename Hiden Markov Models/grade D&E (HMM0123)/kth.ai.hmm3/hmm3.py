import math

# A_input = [float(x) for x in input().split()]
# B_input = [float(x) for x in input().split()]
# pi_input = [float(x) for x in input().split()]
# obs_input = [float(x) for x in input().split()]

A_input = [4.0, 4.0, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4]
B_input = [4.0, 4.0, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4]
pi_input = [1.0, 4.0, 0.241896, 0.266086, 0.249153, 0.242864]
obs_input = [1000.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 0.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 3.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 0.0, 0.0]

build_matrix = lambda M, rows, cols: [[M[n+m*cols] for n in range(cols)] for m in range(rows)]

squezee = lambda M: M[0] if type(M) is list and len(M)==1 and type(M[0]) is list and len(M[0])>1 else M
transpose = lambda M, rows, cols: squezee([ [M[n][m] for n in range(rows)]
                                        if rows > 1 else [M[m]]  
                                        if cols > 1 else M[m][0]
                                    for m in range(cols) ])
                                    

mul_vect = lambda a,b: sum([(a[idx] if type(a) is list else a)*(b[idx] if type(b) is list else b) for idx in range(len(a) if type(a) is list else 1) ])
multiplication = lambda A, B, rows, dim_inside, cols: squezee([[mul_vect(A[m] if rows>1 else A, 
                                                                transpose(B, dim_inside, cols)[n] if dim_inside > 1 else B[n])
                                                    for n in range(cols)]
                                                    for m in range(rows)])
# have to be the same size
mul_matrix = lambda A,B: [[A[m][n]*B[m][n] for n in range(len(A[0]))] for m in range(len(A))]


dot_vect = lambda a,b: [(a[idx] if type(a) is list else a)*(b[idx] if type(b) is list else b) for idx in range(len(a) if type(a) is list else 1) ]

max_and_argmax = lambda iterable: tuple(max(enumerate(iterable), key=lambda x: x[1]))




ma, na, mb, nb = int(A_input[0]), int(A_input[1]), int(B_input[0]), int(B_input[1])
A, B, pi = build_matrix(A_input[2:], ma, na), build_matrix(B_input[2:], mb, nb), pi_input[2:]
n_obs, seq_obs = int(obs_input[0]), [int(o) for o in obs_input[1:]]



def baum_welch(lambda_:tuple):
    ## Forward Algotithm - α-pass

    # compute α0(i)
    alpha0 = dot_vect(
        pi, 
        transpose(B, mb, nb)[seq_obs[0]]
    )
    c0 = 1/sum(alpha0)

    #scale the α0(i)
    alpha0 = [c0*alpha0[idx] for idx in range(len(alpha0))]

    alpha = [alpha0]
    c = [c0]

    # compute αt(i)
    for idx in range(1,n_obs):
        obs = seq_obs[idx]
        alphaA = multiplication(alpha[idx-1], A, 1, ma, na) if idx>0 else pi # row vector
        B_obs = transpose(B, mb, nb)[obs] # row vector

        alpha_aux = dot_vect(alphaA, B_obs)

        #scale the αt(i)
        c.append(1/sum(alpha_aux))
        alpha.append(
            multiplication(
            c[idx],
            alpha_aux,
            1, 1, ma
            )
        )

    ## The β-pass

    # Let βT−1(i) = 1, scaled by cT−1
    beta = [mb*[c[-1]]]

    # β-pass
    for idx in range(0, n_obs-1):

        obs = seq_obs[-idx-1]
        B_obs = transpose(B, mb, nb)[obs] # row vector

        beta_times_obs = multiplication(
                        transpose(B_obs, 1, mb),
                        beta[idx],
                        mb, 1, ma
                    )
                    
        beta_aux = mul_matrix(
                beta_times_obs,
                transpose(A, ma, na)
            )

        beta.append([c[-2-idx]*sum(row) for row in transpose(beta_aux, ma, na)])
# [4.527940651794514, 3.7404727123519907, 3.7404727123519903, 3.7404727123519903]
    beta.reverse()

    digamma=[]
    gamma=[]
    for idx in range(0, n_obs-1):

        obs = seq_obs[idx+1]
        B_obs = transpose(B, mb, nb)[obs] # row vector

        beta_times_obs = multiplication(
                        transpose(B_obs, 1, mb),
                        beta[idx+1],
                        mb, 1, ma
                    )
                    
        beta_aux = mul_matrix(
                beta_times_obs,
                transpose(A, ma, na)
            )

        digamma_aux = [ dot_vect(
            alpha[idx],
            transpose(beta_aux, ma, na)[id]) # TODO NÃO SEI SE É TRANSPOSTO
            for id in range(0,mb)
        ]

        gamma_aux = [
            sum(digamma_aux[id])
            for id in range(0,mb)
        ]

        digamma.append(digamma_aux)
        gamma.append(gamma_aux)

        breakpoint

    # Special case for γT−1(i) (as above, no need to normalize)
    gamma.append(alpha[-1])


    ## Re-estimate A, B and π

    # re-estimate π
    lambda_["pi"] = gamma[0]

    #  re-estimate A
    lambda_["A"] = [[math.nan for i in range(na)] for j in range(ma)]
    for i in range(ma):
        denom = 0
        for t in range(n_obs-1):
            denom += gamma[t][i]

        for j in range(na):
            numer = 0

            for t in range(n_obs-1):
                numer = numer + digamma[t][i][j]
                lambda_["A"][i][j] = numer/denom


    # re-estimate B
    lambda_["B"] = [[math.nan for i in range(nb)] for j in range(mb)]
    for i in range(mb):
        denom = 0
        for t in range(n_obs):
            denom += gamma[t][i]

        for j in range(nb):
            numer = 0
            for t in range(n_obs):
                if seq_obs[t] == j:
                    numer += gamma[t][i]

                lambda_["B"][i][j] = numer/denom


    # Compute log[P (O | λ)
    lambda_["logProb"] = 0
    for i in range(n_obs):
        lambda_["logProb"] = lambda_["logProb"] - math.log(c[i])


    # To iterate or not to iterate, that is the question. . .

    return lambda_

max_iters = 10
lambda_ = {
    "A":A,
    "B":B,
    "pi":pi,
    "logProb": -math.inf
}
best_lambda_ = {
    "A":math.nan,
    "B":math.nan,
    "pi":math.nan,
    "logProb": -math.inf
}

for run in range(max_iters):
    lambda_ = baum_welch(lambda_)

    if (lambda_["logProb"] > best_lambda_["logProb"]):
        best_lambda_ = lambda_
    else:
        break
        


# if __name__ == "__main__":
#     # execute only if run as a script
     


breakpoint
