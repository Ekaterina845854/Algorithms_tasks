GOOGOL = 9999999999999
def f(x, b, n, cache, bestnote):
    if x<0:
        return GOOGOL
    if x==0:
        return 0
    if cache[x]>=0:
        return cache[x]
    min = GOOGOL
    best = -1
    for i in range(n):
        r = f(x - b[i], b, n, cache, bestnote)
        if r < min:
            min = r
            bestnote[x] = b[i]
    cache[x] = min +1
    return cache[x]

def buildSolution(x, bestnote):
    ret = []
    while x > 0:
        banknote = bestnote[x]
        ret.append(banknote)
        x -= banknote
    return ret

b = [1, 5, 10, 25]
n = len(b)
x = 30
cache = [-1] * (x+1)
bestnote = [0] * (x+1)
f(x, b, n, cache, bestnote)
solution = buildSolution(x, bestnote)
print(solution)
