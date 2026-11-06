import random

def calculate_distance(route, distance_matrix):
    distance = 0
    num_cities = len(route)
    for i in range(num_cities):
        distance += distance_matrix[route[i]][route[(i + 1) % num_cities]]
    return distance

def inversion_mutation(route):
    new_route = route.copy()
    idx1, idx2 = sorted(random.sample(range(len(route)), 2))
    new_route[idx1:idx2+1] = reversed(new_route[idx1:idx2+1])
    return new_route

def discrete_cuckoo_search(distance_matrix, num_cities, max_generations=1000):
    n = 5
    pa = 0.0
    m = 6
   
    population = [random.sample(range(num_cities), num_cities) for _ in range(n)]
   
    for generation in range(max_generations):
        fitness = [calculate_distance(r, distance_matrix) for r in population]
        best_idx = fitness.index(min(fitness))
        best_cuckoo = population[best_idx]
       
        candidates = []
        for route in population:
            candidates.append(route)
           
        random_cuckoo = random.choice(population)
        for _ in range(m):
            random_cuckoo = inversion_mutation(random_cuckoo)
            candidates.append(random_cuckoo)
           
        best_temp = best_cuckoo.copy()
        for _ in range(m):
            best_temp = inversion_mutation(best_temp)
            candidates.append(best_temp)
           
        if random.random() < pa:
            worst_idx = fitness.index(max(fitness))
            worst_cuckoo = population[worst_idx]
            for _ in range(m):
                worst_cuckoo = inversion_mutation(worst_cuckoo)
                candidates.append(worst_cuckoo)
               
        unique_candidates = []
        for c in candidates:
            if c not in unique_candidates:
                unique_candidates.append(c)
               
        unique_candidates.sort(key=lambda r: calculate_distance(r, distance_matrix))
       
        population = unique_candidates[:n]
        while len(population) < n:
            population.append(random.sample(range(num_cities), num_cities))
           
    final_fitness = [calculate_distance(r, distance_matrix) for r in population]
    global_best_idx = final_fitness.index(min(final_fitness))
    return population[global_best_idx], final_fitness[global_best_idx]

def generate_mock_data(num_cities):
    matrix = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            dist = random.randint(10, 100)
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

if __name__ == "__main__":
    cities = 10
    mock_matrix = generate_mock_data(cities)
   
    best_route, best_dist = discrete_cuckoo_search(mock_matrix, cities)
   
    print("Best Route:", best_route)
    print("Best Distance:", best_dist)
