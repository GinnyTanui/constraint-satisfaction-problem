# ============================================================
#   SEARCH ALGORITHMS: Breadth First Search & Depth First Search
#   Author  : [Your Name]
#   Course  : Artificial Intelligence
#   Task    : Task Four – Search and Optimization
# ============================================================
#
#   GRAPH USED (same graph for both algorithms):
#
#         A
#        / \
#       B   C
#      / \   \
#     D   E   F
#        / \
#       G   H
#
#   Start Node : A
#   Goal Node  : G
#
# ============================================================

# ----------------------------------------------------------
# GRAPH DEFINITION
# Represented as an adjacency list (dictionary).
# Each key is a node, and its value is a list of neighbours.
# ----------------------------------------------------------
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G', 'H'],
    'F': [],
    'G': [],
    'H': []
}

# ============================================================
#   PART (i): BREADTH FIRST SEARCH (BFS)
# ============================================================
#
#   HOW BFS WORKS:
#   - BFS explores the graph LEVEL BY LEVEL.
#   - It starts at the root node and visits ALL neighbours
#     at the current level before moving deeper.
#   - Uses a QUEUE (First In First Out – FIFO).
#   - Guarantees the SHORTEST PATH to the goal.
#
#   Think of it like ripples in water — it spreads outward
#   one level at a time before going deeper.
#
#   BFS ORDER for our graph:
#   Level 0: A
#   Level 1: B, C
#   Level 2: D, E, F
#   Level 3: G, H
#
# ============================================================

from collections import deque  # deque is used as an efficient queue

def bfs(graph, start, goal):
    """
    Breadth First Search Algorithm.

    Parameters:
        graph (dict) : The graph represented as an adjacency list.
        start (str)  : The starting/initial node.
        goal  (str)  : The target/goal node to find.

    Returns:
        list : The path from start to goal, or None if not found.
    """

    print("=" * 55)
    print("   BREADTH FIRST SEARCH (BFS)")
    print("=" * 55)
    print(f"   Start Node : {start}")
    print(f"   Goal Node  : {goal}")
    print("-" * 55)

    # Queue stores paths (not just nodes).
    # We store the entire path so we can trace it at the end.
    # Initial queue contains just the start node as a path.
    queue = deque([[start]])

    # Visited set keeps track of nodes we have already explored.
    # This prevents visiting the same node twice (avoids loops).
    visited = set()

    step = 1  # Step counter for display purposes

    while queue:
        # Dequeue the first path from the front of the queue (FIFO)
        path = queue.popleft()

        # The current node is the LAST node in the current path
        current_node = path[-1]

        print(f"   Step {step}: Exploring node '{current_node}' | Path so far: {' -> '.join(path)}")
        step += 1

        # GOAL TEST: Have we reached the destination?
        if current_node == goal:
            print("-" * 55)
            print(f"   ✔ GOAL '{goal}' FOUND!")
            print(f"   Final Path : {' -> '.join(path)}")
            print(f"   Path Length: {len(path) - 1} steps")
            print("=" * 55)
            return path

        # Mark current node as visited so we don't revisit it
        if current_node not in visited:
            visited.add(current_node)

            # Expand: add all unvisited neighbours to the queue
            for neighbour in graph[current_node]:
                if neighbour not in visited:
                    # Build a new path by extending the current path
                    new_path = path + [neighbour]
                    queue.append(new_path)

    # If the queue empties and goal was not found
    print(f"   ✘ Goal '{goal}' NOT FOUND.")
    print("=" * 55)
    return None


# ============================================================
#   PART (ii): DEPTH FIRST SEARCH (DFS)
# ============================================================
#
#   HOW DFS WORKS:
#   - DFS explores the graph by going as DEEP as possible
#     along one branch before backtracking.
#   - Uses a STACK (Last In First Out – LIFO).
#   - Does NOT guarantee the shortest path.
#   - Good for exploring all possible paths.
#
#   Think of it like exploring a maze — you keep going
#   straight until you hit a dead end, then you backtrack
#   and try a different direction.
#
#   DFS ORDER for our graph (going deep first):
#   A → B → D (dead end, backtrack) → E → G (GOAL!)
#
# ============================================================

def dfs(graph, start, goal):
    """
    Depth First Search Algorithm.

    Parameters:
        graph (dict) : The graph represented as an adjacency list.
        start (str)  : The starting/initial node.
        goal  (str)  : The target/goal node to find.

    Returns:
        list : The path from start to goal, or None if not found.
    """

    print("\n" + "=" * 55)
    print("   DEPTH FIRST SEARCH (DFS)")
    print("=" * 55)
    print(f"   Start Node : {start}")
    print(f"   Goal Node  : {goal}")
    print("-" * 55)

    # Stack stores paths (not just nodes).
    # We use a regular Python list as a stack.
    # Initial stack contains just the start node as a path.
    stack = [[start]]

    # Visited set prevents revisiting nodes (avoids infinite loops)
    visited = set()

    step = 1  # Step counter for display purposes

    while stack:
        # Pop the LAST path from the top of the stack (LIFO)
        path = stack.pop()

        # The current node is the LAST node in the current path
        current_node = path[-1]

        print(f"   Step {step}: Exploring node '{current_node}' | Path so far: {' -> '.join(path)}")
        step += 1

        # GOAL TEST: Have we reached the destination?
        if current_node == goal:
            print("-" * 55)
            print(f"   ✔ GOAL '{goal}' FOUND!")
            print(f"   Final Path : {' -> '.join(path)}")
            print(f"   Path Length: {len(path) - 1} steps")
            print("=" * 55)
            return path

        # Mark current node as visited so we don't revisit it
        if current_node not in visited:
            visited.add(current_node)

            # Expand: add all unvisited neighbours to the stack
            # We reverse the list so that the first neighbour
            # is explored first (left to right order maintained)
            for neighbour in reversed(graph[current_node]):
                if neighbour not in visited:
                    # Build a new path by extending the current path
                    new_path = path + [neighbour]
                    stack.append(new_path)

    # If the stack empties and goal was not found
    print(f"   ✘ Goal '{goal}' NOT FOUND.")
    print("=" * 55)
    return None


# ============================================================
#   COMPARISON SUMMARY
# ============================================================

def print_comparison(bfs_path, dfs_path):
    """Prints a side-by-side comparison of BFS and DFS results."""
    print("\n" + "=" * 55)
    print("   COMPARISON: BFS vs DFS")
    print("=" * 55)
    print(f"   {'Property':<25} {'BFS':<15} {'DFS':<15}")
    print(f"   {'-'*25} {'-'*15} {'-'*15}")
    print(f"   {'Strategy':<25} {'Level by level':<15} {'Deep first':<15}")
    print(f"   {'Data Structure':<25} {'Queue (FIFO)':<15} {'Stack (LIFO)':<15}")
    print(f"   {'Shortest Path?':<25} {'Yes':<15} {'Not always':<15}")
    bfs_len = str(len(bfs_path) - 1) + ' steps' if bfs_path else 'Not found'
    dfs_len = str(len(dfs_path) - 1) + ' steps' if dfs_path else 'Not found'
    print(f"   {'Path Length':<25} {bfs_len:<15} {dfs_len:<15}")
    bfs_str = ' -> '.join(bfs_path) if bfs_path else 'None'
    dfs_str = ' -> '.join(dfs_path) if dfs_path else 'None'
    print(f"   {'Path Found':<25} {bfs_str:<15} {dfs_str:<15}")
    print("=" * 55)


# ============================================================
#   MAIN — RUN BOTH ALGORITHMS
# ============================================================

if __name__ == "__main__":

    START = 'A'  # Initial/start node
    GOAL  = 'G'  # Target/goal node

    print("\n   GRAPH STRUCTURE:")
    print("         A        ")
    print("        / \\      ")
    print("       B   C      ")
    print("      / \\   \\   ")
    print("     D   E   F    ")
    print("        / \\      ")
    print("       G   H      ")
    print(f"\n   Searching from '{START}' to '{GOAL}'\n")

    # Run BFS
    bfs_result = bfs(graph, START, GOAL)

    # Run DFS
    dfs_result = dfs(graph, START, GOAL)

    # Print comparison
    print_comparison(bfs_result, dfs_result)