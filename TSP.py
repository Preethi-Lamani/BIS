import random

n = int(input("Enter number of cities: "))

dist = []
print("Enter the distance matrix:")
for i in range(n):
    dist.append(list(map(int, input().split())))

population_size = 10
generations = 100

def fitness(route):
    total = 0
    for i in range(n):
        total += dist[route[i]][route[(i + 1) % n]]
    return total

# Initial population
population = []
for i in range(population_size):
    population.append(random.sample(range(n), n))

# Genetic Algorithm
for g in range(generations):
    population.sort(key=fitness)
    new_population = population[:2]

    while len(new_population) < population_size:
        p1 = random.choice(population[:5])
        p2 = random.choice(population[:5])

        point = random.randint(1, n - 1)
        child = p1[:point]

        for city in p2:
            if city not in child:
                child.append(city)

        if random.random() < 0.1:
            i, j = random.sample(range(n), 2)
            child[i], child[j] = child[j], child[i]

        new_population.append(child)

    population = new_population

best = min(population, key=fitness)

print("Best route:", [city + 1 for city in best] + [best[0] + 1])
print("Minimum distance:", fitness(best))
