import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import itertools
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, PULP_CBC_CMD

def generate_valid_positions(garden, obstacles, radius):
    minx, miny, maxx, maxy = garden.bounds
    x_vals = np.arange(minx, maxx + radius, radius)
    y_vals = np.arange(miny, maxy + radius, radius)
    return [(x, y) for x, y in itertools.product(x_vals, y_vals)
            if garden.contains(Point(x, y)) and not any(o.contains(Point(x, y)) for o in obstacles)]

def generate_coverage_map(valid_positions, radius):
    coverage_map = {p: [] for p in valid_positions}
    for spr_x, spr_y in valid_positions:
        for x, y in valid_positions:
            if Point(spr_x, spr_y).distance(Point(x, y)) <= radius:
                coverage_map[(spr_x, spr_y)].append((x, y))
    return coverage_map

def solve_optimization(valid_positions, coverage_map):
    model = LpProblem("Minimize_Sprinklers", LpMinimize)
    sprinkler_vars = {p: LpVariable(f"sprinkler_{p[0]}_{p[1]}", cat="Binary") for p in valid_positions}
    model += lpSum(sprinkler_vars.values())
    
    for x, y in valid_positions:
        model += lpSum(sprinkler_vars[(spr_x, spr_y)] for spr_x, spr_y in valid_positions if (x, y) in coverage_map[(spr_x, spr_y)]) >= 1
    
    model.solve(PULP_CBC_CMD(msg=False))
    return [(x, y) for (x, y), var in sprinkler_vars.items() if value(var) == 1]

def plot_solution(garden, obstacles, optimal_solution, radius):
    fig, ax = plt.subplots(figsize=(8, 6))
    x_poly, y_poly = zip(*garden.exterior.coords)
    ax.plot(x_poly, y_poly, 'k-', linewidth=2, label="Garden")
    
    for obst in obstacles:
        x_obs, y_obs = zip(*list(obst.exterior.coords))
        ax.fill(x_obs, y_obs, 'gray', alpha=0.5, label="Obstacle")
    
    for (x, y) in optimal_solution:
        ax.add_patch(plt.Circle((x, y), radius, color='blue', alpha=0.3))
        ax.plot(x, y, 'ro', markersize=5, label="Sprinkler")
    
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Y (meters)")
    ax.set_title(f"Optimal Coverage with {len(optimal_solution)} Sprinklers (ILP)")
    ax.legend()
    ax.grid(True)
    plt.show()

def main():
    garden_vertices = [(0, 0), (10, 0), (10, 8), (5, 10), (0, 8)]
    garden = Polygon(garden_vertices)
    obstacles = [Polygon([(3, 3), (4, 3), (4, 4), (3, 4)])]
    radius = 2
    
    valid_positions = generate_valid_positions(garden, obstacles, radius)
    coverage_map = generate_coverage_map(valid_positions, radius)
    optimal_solution = solve_optimization(valid_positions, coverage_map)
    plot_solution(garden, obstacles, optimal_solution, radius)

if __name__ == "__main__":
    main()

