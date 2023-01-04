import operator
import random
import re

with open("input.txt") as file:
    lines = [line.rstrip() for line in file]
blueprints = [list(map(int, re.findall("-?\d+", l))) for l in lines]
# calculate the number of materials for the given build path
def number_of_geodes(robot_build_path, buildcost):
    robots = [1, 0, 0, 0]
    materials = [0, 0, 0, 0]

    for minute in range(len(robot_build_path)):
        robot_to_build = robot_build_path[minute]
        build_robot = (
            min(tuple(map(operator.sub, materials, buildcost[robot_to_build]))) > -1
        )
        materials = tuple(map(operator.add, materials, robots))
        if build_robot:
            robots[robot_to_build] += 1
            materials = tuple(map(operator.sub, materials, buildcost[robot_to_build]))
    return materials


def fitness_function(materials):
    ore, clay, obsidian, geode = materials
    return geode * 10000 + obsidian * 100 + clay


def sort_function(value):
    return fitness_function(value[1])


def crossover(a, b):
    half = len(a) // 2
    crossover_point = random.randint(0, half)

    return (
        b[0:crossover_point]
        + a[crossover_point : crossover_point + half]
        + b[crossover_point + half :]
    )


def mutate(a, mutation_rate):
    for i, _ in enumerate(a):
        if random.random() < mutation_rate:
            if random.randint(0, 2) == 0:
                a[i] = (a[i] + 1) % 4
            else:
                a[i] = (a[i] - 1) % 4
    return a


total = 0

minutes = 24
minutes = 32  # pt 2
mutation_rate = 0.12
population_size = minutes * 8
number_of_generations = 100 * 3
sample_size = 12

pt2_total = 1

for (idx, blueprint) in enumerate(blueprints[:5]):
    blue_print_numer, ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = blueprint

    population = []
    best_result = (0, 0, 0, 0)
    # make a random population
    for _ in range(population_size):
        population.append([random.randint(0, 3) for _ in range(minutes)])

    # let the genetic mutation do its thing
    for generation in range(number_of_generations):
        results = []
        for i in range(population_size):
            result = number_of_geodes(
                population[i],
                [
                    (ore, 0, 0, 0),
                    (clay_ore, 0, 0, 0),
                    (obs_ore, obs_clay, 0, 0),
                    (geo_ore, 0, geo_obs, 0),
                ],
            )
            # store best result
            if fitness_function(result) > fitness_function(best_result):
                best_result = result

            results.append((population[i], result))

        # make new population
        population = []
        for _ in range(population_size):
            # take 8 random
            sample = random.sample(results, 8)
            # take the best 2
            sample.sort(key=sort_function, reverse=True)
            # cross over
            child = crossover(sample[0][0], sample[1][0])
            # mutate
            child = mutate(child, mutation_rate)
            # add to population
            population.append(child)

    total += blue_print_numer * best_result[3]
    print(f"{blue_print_numer}: {best_result[3]} = {total}")
    if idx < 3:
        pt2_total *= best_result[3]
print(pt2_total)
