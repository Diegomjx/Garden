# Optimal Sprinkler Placement

## Overview
Ever wanted to optimize the placement of sprinklers in a garden while avoiding obstacles? This script does exactly that. It uses Integer Linear Programming (ILP) to determine the minimum number of sprinklers needed to cover the entire garden area.

## How It Works
- Defines a garden as a polygon.
- Identifies obstacles inside the garden.
- Computes valid positions for sprinklers.
- Builds a coverage map based on sprinkler radius.
- Uses ILP to minimize the number of sprinklers while ensuring full coverage.
- Visualizes the optimal solution.

## Dependencies
Make sure you have the following installed:
```bash
pip install numpy matplotlib shapely pulp
```

## Usage
Run the script:
```bash
python bard.py
```
It will generate an optimized sprinkler placement and display it graphically.

## File Breakdown
- `generate_valid_positions()`: Filters out positions inside the garden but not inside obstacles.
- `generate_coverage_map()`: Maps which sprinklers cover which areas.
- `solve_optimization()`: Uses ILP to find the optimal sprinkler placement.
- `plot_solution()`: Visualizes the final solution.
- `main()`: Puts everything together and runs the program.

## Notes
- The garden and obstacles are hardcoded. Modify `garden_vertices` and `obstacles` in `main()` for custom inputs.
- The solver used is `PULP_CBC_CMD`, which is included in PuLP.
- The radius of each sprinkler can be adjusted by modifying the `radius` variable.

## License
Do whatever you want with this. Just don't blame me if your garden floods.

