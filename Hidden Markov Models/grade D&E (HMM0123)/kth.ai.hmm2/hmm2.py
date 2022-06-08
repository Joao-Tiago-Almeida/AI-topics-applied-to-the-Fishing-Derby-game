import sys

A_input = [float(x) for x in input().split()]
B_input = [float(x) for x in input().split()]
pi_input = [float(x) for x in input().split()]
obs_input = [float(x) for x in input().split()]

# A_input = [4.0, 4.0, 0.6, 0.1, 0.1, 0.2, 0.0, 0.3, 0.2, 0.5, 0.8, 0.1, 0.0, 0.1, 0.2, 0.0, 0.1, 0.7]
# B_input = [4.0, 4.0, 0.6, 0.2, 0.1, 0.1, 0.1, 0.4, 0.1, 0.4, 0.0, 0.0, 0.7, 0.3, 0.0, 0.0, 0.1, 0.9]
# pi_input = [1.0, 4.0, 0.5, 0.0, 0.0, 0.5]
# obs_input = [4, 2, 0, 3, 1]

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

ma, na, mb, nb = int(A_input[0]), int(A_input[1]), int(B_input[0]), int(B_input[1])
A, B, pi = build_matrix(A_input[2:], ma, na), build_matrix(B_input[2:], mb, nb), pi_input[2:]
n_obs, seq_obs = int(obs_input[0]), [int(o) for o in obs_input[1:]]

dot_vect = lambda a,b: [(a[idx] if type(a) is list else a)*(b[idx] if type(b) is list else b) for idx in range(len(a) if type(a) is list else 1) ]

max_and_argmax = lambda iterable: tuple(max(enumerate(iterable), key=lambda x: x[1]))

beta = []
argbeta = []

for idx in range(len(seq_obs)):
    obs = seq_obs[idx]

    B_obs = transpose(B, mb, nb)[obs] # row vector
    if idx>0:
        beta_times_obs = multiplication(
                            transpose(B_obs, 1, mb),
                            beta[idx-1],
                            mb, 1, ma
                        )
                            
        
        M = mul_matrix(
                beta_times_obs,
                transpose(A, ma, na)
            )

        argmax_temp = []
        max_temp = []
        for state in M:
            agrmax_, max_ = max_and_argmax(state)
            max_temp.append(max_)
            argmax_temp.append(agrmax_)

        argbeta.append(argmax_temp)

    else:
        max_temp = dot_vect(pi, B_obs)
    
    beta.append(max_temp)
    

# backtrack - only done for one sequence ... yet
last_state = max_and_argmax(beta[-1])[0]
sequence = [last_state]
for states in range(len(argbeta)):
    last_state = argbeta[-states-1][last_state]
    sequence.append(last_state)

print(str(sequence[::-1])[1:-1].replace(",",""))
