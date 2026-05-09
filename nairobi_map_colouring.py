
# Map Coloring of Nairobi Sub-Counties using Backtracking (CSP)

# So Nairobi has 17 sub-counties. We color them using the MINIMUM
# number of colors such that no two adjacent sub-counties share
# the same color.
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

# --- 1. Defining  all the 17 sub-counties ---
sub_counties = [
    "Westlands",
    "Dagoretti North",
    "Dagoretti South",
    "Langata",
    "Kibra",
    "Roysambu",
    "Kasarani",
    "Ruaraka",
    "Embakasi South",
    "Embakasi North",
    "Embakasi Central",
    "Embakasi East",
    "Embakasi West",
    "Makadara",
    "Kamukunji",
    "Starehe",
    "Mathare",
]

# --- 2. Adjacency list based on actual geographic borders ---

adjacency = {
    "Westlands":        ["Dagoretti North", "Roysambu", "Starehe"],
    "Dagoretti North":  ["Westlands", "Dagoretti South", "Kibra", "Starehe"],
    "Dagoretti South":  ["Dagoretti North", "Kibra", "Langata"],
    "Langata":          ["Dagoretti South", "Kibra", "Embakasi South"],
    "Kibra":            ["Dagoretti North", "Dagoretti South", "Langata", "Starehe", "Kamukunji"],
    "Roysambu":         ["Westlands", "Kasarani", "Ruaraka", "Mathare"],
    "Kasarani":         ["Roysambu", "Ruaraka", "Embakasi North"],
    "Ruaraka":          ["Roysambu", "Kasarani", "Embakasi North", "Mathare", "Kamukunji"],
    "Embakasi South":   ["Langata", "Embakasi West", "Embakasi Central"],
    "Embakasi North":   ["Kasarani", "Ruaraka", "Embakasi Central", "Embakasi East"],
    "Embakasi Central": ["Embakasi South", "Embakasi North", "Embakasi West", "Embakasi East", "Makadara"],
    "Embakasi East":    ["Embakasi North", "Embakasi Central"],
    "Embakasi West":    ["Embakasi South", "Embakasi Central", "Makadara", "Kamukunji"],
    "Makadara":         ["Embakasi Central", "Embakasi West", "Kamukunji", "Starehe"],
    "Kamukunji":        ["Kibra", "Ruaraka", "Embakasi West", "Makadara", "Starehe"],
    "Starehe":          ["Westlands", "Dagoretti North", "Kibra", "Kamukunji", "Makadara", "Mathare"],
    "Mathare":          ["Roysambu", "Ruaraka", "Starehe"],
}

# --- 3. Determine minimum colors needed using backtracking ---
def is_valid(region, color, assignment):
    """Check if assigning this color to region violates any constraint."""
    for neighbor in adjacency[region]:
        if assignment.get(neighbor) == color:
            return False
    return True

def backtrack(assignment, regions, colors):
    """Recursive backtracking solver."""
    if len(assignment) == len(regions):
        return assignment  # All counties assgined colours so solution found

    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]

    for color in colors:
        if is_valid(region, color, assignment):
            assignment[region] = color
            result = backtrack(assignment, regions, colors)
            if result:
                return result
            del assignment[region]  # Undo and try next color

    return None  # Dead end — backtrack

# Try with 2 colors first, then 3, then 4 (find minimum)
solution = None
num_colors_used = 0
for num_colors in range(2, 5):
    color_names = ["Color A", "Color B", "Color C", "Color D"][:num_colors]
    result = backtrack({}, sub_counties, color_names)
    if result:
        solution = result
        num_colors_used = num_colors
        break

# --- 4. Print results ---
print("=" * 52)
print("   Nairobi Sub-County Map Coloring Solution")
print("=" * 52)
if solution:
    print(f"  ✅ Solved using {num_colors_used} colors!\n")
    for sc, color in solution.items():
        print(f"  {sc:<22} → {color}")
else:
    print("  ❌ No solution found with up to 4 colors.")
print("=" * 52)


from collections import Counter
usage = Counter(solution.values())
print("\n  Color usage summary:")
for color, count in sorted(usage.items()):
    print(f"    {color}: {count} sub-counties")

# --- 5. Approximate geographic centroids (lon, lat) ---

positions = {
    "Westlands":        (36.800, -1.258),
    "Dagoretti North":  (36.768, -1.285),
    "Dagoretti South":  (36.755, -1.318),
    "Langata":          (36.740, -1.360),
    "Kibra":            (36.784, -1.312),
    "Roysambu":         (36.840, -1.225),
    "Kasarani":         (36.898, -1.222),
    "Ruaraka":          (36.868, -1.255),
    "Embakasi South":   (36.840, -1.340),
    "Embakasi North":   (36.910, -1.265),
    "Embakasi Central": (36.900, -1.295),
    "Embakasi East":    (36.955, -1.305),
    "Embakasi West":    (36.870, -1.310),
    "Makadara":         (36.858, -1.300),
    "Kamukunji":        (36.835, -1.278),
    "Starehe":          (36.818, -1.275),
    "Mathare":          (36.855, -1.258),
}

# --- 6. Color palette that I used ---
palette = {
    "Color A": "#E74C3C",   # Vivid Red
    "Color B": "#2ECC71",   # Emerald Green
    "Color C": "#3498DB",   # Sky Blue
    "Color D": "#F39C12",   # Orange (only if needed)
}

label_for = {
    "Color A": "Red",
    "Color B": "Green",
    "Color C": "Blue",
    "Color D": "Orange",
}

# --- 7. Visualize ---
fig, ax = plt.subplots(figsize=(13, 11))
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#16213e")

# Background grid lines for geo feel
for lon in np.arange(36.72, 36.99, 0.02):
    ax.axvline(lon, color='#0f3460', linewidth=0.4, alpha=0.5)
for lat in np.arange(-1.40, -1.20, 0.02):
    ax.axhline(lat, color='#0f3460', linewidth=0.4, alpha=0.5)

# Draw adjacency edges
drawn_edges = set()
for region, neighbors in adjacency.items():
    x1, y1 = positions[region]
    for neighbor in neighbors:
        edge = tuple(sorted([region, neighbor]))
        if edge not in drawn_edges:
            x2, y2 = positions[neighbor]
            ax.plot([x1, x2], [y1, y2],
                    color='#4a4a6a', linewidth=1.2, alpha=0.6,
                    linestyle='--', zorder=1)
            drawn_edges.add(edge)

# Draw sub-county nodes
node_radius = 0.012
for sc, (lon, lat) in positions.items():
    color_key = solution.get(sc, "Color A")
    hex_color = palette[color_key]

    # Outer glow ring
    glow = plt.Circle((lon, lat), node_radius * 1.5,
                       color=hex_color, alpha=0.15, zorder=2)
    ax.add_patch(glow)

    # Main circle
    circle = plt.Circle((lon, lat), node_radius,
                         color=hex_color, ec='white',
                         linewidth=1.5, zorder=3)
    ax.add_patch(circle)

    # Sub-county label (split long names for readability)
    words = sc.split()
    if len(words) > 2:
        label = words[0] + '\n' + ' '.join(words[1:])
    elif len(words) == 2:
        label = words[0] + '\n' + words[1]
    else:
        label = sc

    ax.text(lon, lat + node_radius * 1.8, label,
            ha='center', va='bottom',
            fontsize=6.5, fontweight='bold',
            color='white', zorder=5,
            path_effects=[pe.withStroke(linewidth=1.5, foreground='black')])

    # Color label inside circle
    ax.text(lon, lat, label_for[color_key][0],  # Just first letter R/G/B
            ha='center', va='center',
            fontsize=7, fontweight='bold',
            color='white', zorder=6)

# --- 8. Legend ---
legend_patches = [
    mpatches.Patch(color=palette[ck], label=f"{label_for[ck]}  ({usage[ck]} sub-counties)")
    for ck in sorted(usage.keys())
]
legend = ax.legend(
    handles=legend_patches,
    loc='lower left',
    fontsize=10,
    title=f"Colors Used: {num_colors_used}",
    title_fontsize=11,
    facecolor='#0f3460',
    edgecolor='#4a4a6a',
    labelcolor='white',
)
legend.get_title().set_color('white')

# --- 9. Title & Labels ---
ax.set_title(
    f"Nairobi City County — Sub-County Map Coloring\n"
    f"17 Sub-Counties · {num_colors_used} Colors (Minimum) · Backtracking CSP",
    fontsize=13, fontweight='bold', color='white', pad=16
)
ax.set_xlabel("Longitude (°E)", color='#aaaacc', fontsize=9)
ax.set_ylabel("Latitude (°S)", color='#aaaacc', fontsize=9)
ax.tick_params(colors='#aaaacc', labelsize=8)

# Compass rose (simple N indicator)
ax.annotate('N ↑', xy=(36.975, -1.215), fontsize=11, color='white',
            fontweight='bold', ha='center')

ax.set_xlim(36.71, 36.99)
ax.set_ylim(-1.42, -1.20)

plt.tight_layout()
plt.savefig("nairobi_map_coloring.png", dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("\n Map saved as 'nairobi_map_coloring.png'")