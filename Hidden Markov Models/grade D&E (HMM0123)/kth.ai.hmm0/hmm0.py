import sys

A_input = [float(x) for x in input().split()]
B_input = [float(x) for x in input().split()]
pi_input = [float(x) for x in input().split()]


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

ma, na, mb, nb = int(A_input[0]), int(A_input[1]), int(B_input[0]), int(B_input[1])
A, B, pi = build_matrix(A_input[2:], ma, na), build_matrix(B_input[2:], mb, nb), pi_input[2:]

output = lambda M: f"1 {len(M)} {str(M)[1:-1].replace(',','')}"

print(output(multiplication(multiplication(pi, A, 1, ma, na), B, 1, mb, nb)))
