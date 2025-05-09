import matplotlib.pyplot as plt
import sys
import json

# Data
data1 = {
    "balls": [
      { "id": 1, "x": 489, "y": 398 },
      { "id": 2, "x": 401, "y": 322 },
      { "id": 3, "x": 511, "y": 359 },
      { "id": 4, "x": 532, "y": 319 },
      { "id": 5, "x": 361, "y": 322 },
      { "id": 6, "x": 490, "y": 320 },
      { "id": 7, "x": 443, "y": 395 },
      { "id": 8, "x": 425, "y": 361 },
      { "id": 9, "x": 465, "y": 433 },
      { "id": 10, "x": 467, "y": 358 },
      { "id": 11, "x": 447, "y": 322 },
      { "id": 12, "x": 403, "y": 394 },
      { "id": 13, "x": 448, "y": 470 },
      { "id": 14, "x": 380, "y": 358 },
      { "id": 15, "x": 424, "y": 434 },
      { "id": "cue", "x": 0, "y": 0 }
    ]
}

# Check if we got the input argument
if len(sys.argv) < 2:
    print("Error: No data passed to graph.py")
    sys.exit(1)

# Read ballData from the command-line argument
ball_data_json = sys.argv[1]
data = json.loads(ball_data_json)

# Extracting x, y coordinates and labels
x_vals = [ball['x'] for ball in data['balls']]
y_vals = [ball['y'] for ball in data['balls']]
labels = [str(ball['id']) for ball in data['balls']]

# Plotting
plt.figure(figsize=(8, 6))
plt.scatter(x_vals, y_vals, color='blue')

# Labeling the points
for i, label in enumerate(labels):
    if x_vals[i] != 0 and y_vals[i] != 0:  # Skip the points with x=0, y=0
        plt.text(x_vals[i] + 5, y_vals[i] + 5, label, fontsize=12)

# Setting axis labels
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Ball Positions')

plt.savefig("ball_positions.png")

