# ============================================================
# Map Coloring of Australia using Backtracking (CSP approach)
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. Define the regions and their adjacencies ---
regions = [
    "WA",   # Western Australia
    "NT",   # Northern Territory
    "SA",   # South Australia
    "QLD",  # Queensland
    "NSW",  # New South Wales
    "VIC",  # Victoria
    "TAS",  # Tasmania
]

# Adjacency list: each region borders these others
adjacency = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "QLD"],
    "SA":  ["WA", "NT", "QLD", "NSW", "VIC"],
    "QLD": ["NT", "SA", "NSW"],
    "NSW": ["SA", "QLD", "VIC"],
    "VIC": ["SA", "NSW"],
    "TAS": [],  # Island — no land borders
}

COLORS = ["Red", "Green", "Blue"]

# --- 2. Constraint check: can we assign this color? ---
def is_valid(region, color, assignment):
    for neighbor in adjacency[region]:
        if assignment.get(neighbor) == color:
            return False
    return True

# --- 3. Backtracking solver ---
def backtrack(assignment, regions):
    # All regions assigned → solution found
    if len(assignment) == len(regions):
        return assignment

    # Pick the next unassigned region
    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]

    for color in COLORS:
        if is_valid(region, color, assignment):
            assignment[region] = color
            result = backtrack(assignment, regions)
            if result:
                return result
            del assignment[region]  # backtrack

    return None  # No valid color found → backtrack further

# --- 4. Solve ---
solution = backtrack({}, regions)

# --- 5. Display result in terminal ---
print("=" * 40)
print("   Australia Map Coloring Solution")
print("=" * 40)
if solution:
    for region, color in solution.items():
        print(f"  {region:<5} → {color}")
else:
    print("No solution found with 3 colors.")
print("=" * 40)

# --- 6. Visualize using matplotlib ---
# Approximate centroid positions for each region (longitude, latitude)
positions = {
    "WA":  (121.6, -25.5),
    "NT":  (133.4, -19.5),
    "SA":  (135.5, -30.0),
    "QLD": (145.0, -22.5),
    "NSW": (146.5, -32.5),
    "VIC": (144.5, -37.0),
    "TAS": (146.5, -42.0),
}

color_map = {
    "Red":   "#E74C3C",
    "Green": "#2ECC71",
    "Blue":  "#3498DB",
}

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_facecolor("#D6EAF8")
fig.patch.set_facecolor("#EBF5FB")

# Draw edges (adjacency lines)
drawn_edges = set()
for region, neighbors in adjacency.items():
    x1, y1 = positions[region]
    for neighbor in neighbors:
        edge = tuple(sorted([region, neighbor]))
        if edge not in drawn_edges:
            x2, y2 = positions[neighbor]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.4, zorder=1)
            drawn_edges.add(edge)

# Draw nodes (regions as colored circles)
for region, (x, y) in positions.items():
    color_name = solution.get(region, "Gray")
    hex_color = color_map.get(color_name, "#AAAAAA")

    circle = plt.Circle((x, y), 2.2, color=hex_color,
                         ec="black", linewidth=2, zorder=2)
    ax.add_patch(circle)
    ax.text(x, y, region, ha='center', va='center',
            fontsize=11, fontweight='bold', color='white', zorder=3)
    ax.text(x, y - 3.2, color_name, ha='center', va='center',
            fontsize=8, color='#333333', zorder=3)

# Legend
legend_patches = [
    mpatches.Patch(color=hex_color, label=color)
    for color, hex_color in color_map.items()
]
ax.legend(handles=legend_patches, loc='lower left',
          fontsize=10, title="Colors Used", title_fontsize=11)

ax.set_xlim(110, 160)
ax.set_ylim(-47, -10)
ax.set_title("Australia Map Coloring — 3 Colors (Backtracking CSP)",
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.tight_layout()
plt.savefig("australia_map_coloring.png", dpi=150)
plt.show()
print("\nMap saved as 'australia_map_coloring.png'")