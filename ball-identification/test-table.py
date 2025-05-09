import matplotlib.pyplot as plt

# Table state data
table_state = {
    "ball1": { "id": 1, "x": 0.15, "y": 0.70 },
    "ball2": { "id": 2, "x": 0.20, "y": 0.25 },
    "ball3": { "id": 3, "x": 0.30, "y": 0.20 },
    "ball4": { "id": 4, "x": 0.40, "y": 0.30 },
    "ball5": { "id": 5, "x": 0.70, "y": 0.60 },
    "ball6": { "id": 6, "x": 0.60, "y": 0.50 },
    "ball7": { "id": 7, "x": 0.70, "y": 0.50 },
    "ball8": { "id": 8, "x": 0.70, "y": 0.70 },
    "ball9": { "id": 9, "x": 0.80, "y": 0.30 },
    "ball10": { "id": 10, "x": 0.20, "y": 0.90 },
    "ball11": { "id": 11, "x": 0.35, "y": 0.80 },
    "ball12": { "id": 12, "x": 0.45, "y": 0.85 },
    "ball13": { "id": 13, "x": 0.55, "y": 0.80 },
    "ball14": { "id": 14, "x": 0.65, "y": 0.75 },
    "ball15": { "id": 15, "x": 0.75, "y": 0.70 },
    "cue-ball": { "id": 17, "x": 0.30, "y": 0.50 },
    "target-ball": { "id": 18, "x": 0.10, "y": 0.20 },
    "pocket": { "id": 19, "x": 0.00, "y": 0.50 }
}

# Extracting ball positions for plotting
cue_ball = table_state["cue-ball"]
target_ball = table_state["target-ball"]
balls = [cue_ball] + [ball for key, ball in table_state.items() if "ball" in key and "cue" not in key and "target" not in key]

# Create plot
plt.figure(figsize=(10, 5))

# Plotting all the balls
for ball in balls:
    if ball["id"] == cue_ball["id"]:
        plt.scatter(ball["x"], ball["y"], s=120, c='orange', label=f"Cue Ball {ball['id']}", zorder=5)  # Cue ball in orange
    else:
        plt.scatter(ball["x"], ball["y"], s=100, c='blue', label=f"Ball {ball['id']}" if 'cue' in ball else "", zorder=5)

# Plotting target ball in a distinct color
plt.scatter(target_ball["x"], target_ball["y"], s=120, c='red', label=f"Target Ball {target_ball['id']}", zorder=6)

# Plotting the pocket (as a green circle at (0, 0))
plt.scatter(0, 0, s=300, c='green', marker='o', label="Pocket")

# Labels
plt.title("Pool Table State")
plt.xlabel("Table Length (0-1 scale)")
plt.ylabel("Table Width (0-1 scale)")

# Set limits and aspect for a more accurate table view
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.gca().set_aspect('equal', adjustable='box')

# Add a legend
plt.legend()

# Show plot
plt.grid(True)
plt.show()