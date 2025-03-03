from scipy.optimize import minimize

def q(p):
    q = 5000 + ((1000-p)/50) * 1000
    return q

def f(p):
    if p <= 300:
        return None
    F = (p - 300) * q(p) - 100_000
    return -F

initial_price = 1000
bounds = [(300, None)]
result = minimize(f, initial_price)
optimal_price = result.x[0]
optimal_quantity = q(optimal_price)

print(optimal_price)
print(optimal_quantity)
