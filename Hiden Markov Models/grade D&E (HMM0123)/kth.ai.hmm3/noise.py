def add_noise(m,n,noise=0.1):
    rows=[]
    if m>1 and n>1:
        const = 1/len(n)
        for n in range(len(v[0])):
            cols_aux=[]
            for  m in range(len(v)):
                cols_aux.append(const+random.uniform(-noise,noise))
            cols_aux.append(1-sum(cols_aux))
            rows.append(cols_aux)
    elif m==1 and n>1:
        const = 1/len(n)
        cols_aux=[]
        for  m in range(len(v)):
            cols_aux.append(const+random.uniform(-noise,noise))
        cols_aux.append(1-sum(cols_aux))
        rows.append(cols_aux)
    else:
        [[1] for idx in range(m)]

    return rows
