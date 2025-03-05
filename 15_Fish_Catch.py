import numpy as np
from scipy.optimize import minimize

def fish_population(catch):
    initial_population = 20
    population = np.zeros(5)
    population[0] = initial_population - catch[0]

    for i in range(1, 5):
        population[i] = population[i-1] - catch[i] + 2

    return population

def f(catch):
    population = fish_population(catch)
    profit = np.sum(catch * 300)
    penalty = np.sum(500 * np.maximum(0, 8 - population))
    return - (profit - penalty)

def coordinate_descent(initial_catch, max_iterations=100):
    catch = initial_catch.copy()
    for _ in range(max_iterations):
        for i in range(5):
            best_catch = catch[i]
            best_profit = f(catch)
            for new_catch in np.arange(0, 4.1, 0.1):
                catch[i] = new_catch
                current_profit = f(catch)
                if current_profit < best_profit:
                    best_catch = new_catch
                    best_profit = current_profit
            catch[i] = best_catch
    return catch

if __name__ == "__main__":

    # minimize от scipy
    initial_catch = np.array([0, 0, 0, 0, 0])

    bounds = [(0, 4) for _ in range(5)]

    result = minimize(f, initial_catch, bounds=bounds)

    optimal_catch = result.x
    optimal_profit = -result.fun
    optimal_population = fish_population(optimal_catch)

    print("Оптимальный план вылова рыбы на 5 лет:", optimal_catch)
    print("Максимальная прибыль:", optimal_profit)
    print("Популяция рыбы на 5 лет:", optimal_population)

    # Координатный спуск
    optimal_catch_cd = coordinate_descent(initial_catch)
    optimal_profit_cd = -f(optimal_catch_cd)
    optimal_population_cd = fish_population(optimal_catch_cd)

    print("Оптимальный план вылова рыбы на 5 лет:", optimal_catch_cd)
    print("Максимальная прибыль:", optimal_profit_cd)
    print("Популяция рыбы на 5 лет:", optimal_population_cd)
