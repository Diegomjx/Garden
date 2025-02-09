import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import itertools
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, PULP_CBC_CMD

# 🔹 Define the garden area and obstacles
garden_vertices = [(0, 0), (10, 0), (10, 8), (5, 10), (0, 8)]
garden = Polygon(garden_vertices)

obstacles = [Polygon([(3, 3), (4, 3), (4, 4), (3, 4)])]

# 🔹 Sprinkler parameters
radius = 2  

# 🔹 Generate valid candidate positions inside the garden (avoiding obstacles)
minx, miny, maxx, maxy = garden.bounds
x_vals = np.arange(minx, maxx, radius)
y_vals = np.arange(miny, maxy, radius)
valid_positions = [(x, y) for x, y in itertools.product(x_vals, y_vals)
                   if garden.contains(Point(x, y)) and not any(o.contains(Point(x, y)) for o in obstacles)]

# 🔹 Generate coverage areas for each sprinkler
coverage_map = {p: [] for p in valid_positions}
for x, y in itertools.product(x_vals, y_vals):
    if garden.contains(Point(x, y)) and not any(o.contains(Point(x, y)) for o in obstacles):
        for spr_x, spr_y in valid_positions:
            if Point(x, y).distance(Point(spr_x, spr_y)) <= radius:
                coverage_map[(spr_x, spr_y)].append((x, y))

# 🔹 Optimization Model (ILP) to find the minimum number of sprinklers
model = LpProblem("Minimize_Sprinklers", LpMinimize)

# 🔹 Variables: 1 if a sprinkler is placed at (x, y), 0 otherwise
sprinkler_vars = {p: LpVariable(f"sprinkler_{p[0]}_{p[1]}", cat="Binary") for p in valid_positions}

# 🔹 Objective Function: Minimize the number of sprinklers
model += lpSum(sprinkler_vars.values())

# 🔹 Constraints: Every point in the garden must be covered at least once
for x, y in itertools.product(x_vals, y_vals):
    if garden.contains(Point(x, y)) and not any(o.contains(Point(x, y)) for o in obstacles):
        model += lpSum(sprinkler_vars[(spr_x, spr_y)] for spr_x, spr_y in valid_positions if (x, y) in coverage_map[(spr_x, spr_y)]) >= 1

# 🔹 Solve the optimization problem using CBC solver
model.solve(PULP_CBC_CMD(msg=False))  # Disable solver messages

# 🔹 Retrieve the optimal solution
optimal_solution = [(x, y) for (x, y), var in sprinkler_vars.items() if value(var) == 1]

# 🔹 Plot the result
fig, ax = plt.subplots(figsize=(8, 6))

# Draw the garden
x_poly, y_poly = zip(*garden_vertices + [garden_vertices[0]])  # Close the polygon
ax.plot(x_poly, y_poly, 'k-', linewidth=2, label="Garden")

# Draw obstacles
for obst in obstacles:
    x_obs, y_obs = zip(*list(obst.exterior.coords))
    ax.fill(x_obs, y_obs, 'gray', alpha=0.5, label="Obstacle")

# Draw sprinklers with coverage radius
for (x, y) in optimal_solution:
    ax.add_patch(plt.Circle((x, y), radius, color='blue', alpha=0.3))
    ax.plot(x, y, 'ro', markersize=5, label="Sprinkler")

# 🔹 Visual Enhancements
ax.set_xlabel("X (meters)")
ax.set_ylabel("Y (meters)")
ax.set_title(f"Optimal Coverage with {len(optimal_solution)} Sprinklers (ILP)")
ax.legend()
ax.grid(True)
plt.show()
