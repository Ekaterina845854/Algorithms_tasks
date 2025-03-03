import numpy as np
from scipy.optimize import linprog

c = [-2500, -2000] 

A = [
    [5, 3],  
]
b = [525]  

x0_bounds = (0, 100)  
x1_bounds = (0, 75)  

result = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')

if result.success:
    optimal_catch = result.x
    optimal_profit = -result.fun 
    print(f"Оптимальное количество курток: {optimal_catch[0]:.2f}")
    print(f"Оптимальное количество пиджаков: {optimal_catch[1]:.2f}")
    print(f"Максимальная прибыль: {optimal_profit:.2f} рублей")
else:
    print("Не удалось найти оптимальное решение.")


def greedy_jacket_production():
    total_hours = 525 
    hours_per_jacket = 5  
    hours_per_blazer = 3 
    max_jackets_demand = 100 
    max_blazers_supply = 75 
    profit_per_jacket = 2500 
    profit_per_blazer = 2000

    profit_per_hour_jacket = profit_per_jacket / hours_per_jacket
    profit_per_hour_blazer = profit_per_blazer / hours_per_blazer

    jackets_produced = 0
    blazers_produced = 0
    remaining_hours = total_hours

    if profit_per_hour_blazer > profit_per_hour_jacket:
        blazers_to_produce = min(max_blazers_supply, remaining_hours // hours_per_blazer)
        blazers_produced += blazers_to_produce
        remaining_hours -= blazers_to_produce * hours_per_blazer

        jackets_to_produce = min(max_jackets_demand, remaining_hours // hours_per_jacket)
        jackets_produced += jackets_to_produce
    else:
        jackets_to_produce = min(max_jackets_demand, remaining_hours // hours_per_jacket)
        jackets_produced += jackets_to_produce
        remaining_hours -= jackets_to_produce * hours_per_jacket

        blazers_to_produce = min(max_blazers_supply, remaining_hours // hours_per_blazer)
        blazers_produced += blazers_to_produce

    total_profit = (jackets_produced * profit_per_jacket) + (blazers_produced * profit_per_blazer)
    print(f"Оптимальное количество курток: {jackets_produced}")
    print(f"Оптимальное количество пиджаков: {blazers_produced}")
    print(f"Максимальная прибыль: {total_profit} рублей")

greedy_jacket_production()

