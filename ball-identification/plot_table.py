# plot_table.py
import json
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def plot_impact_point(impact_point, cue_ball_radius, cue_ball_center=(0, 0)):
    """Plots the impact point on the cue ball."""
    # Plot the cue ball as a white circle
    cue_ball = Circle((0, 0), cue_ball_radius, color='white', ec='black', lw=2)  # (0, 0) is the center of the cue ball
    
    fig, ax = plt.subplots()
    ax.add_patch(cue_ball)

    # Extract x and y coordinates of the impact point
    x, y = impact_point
    
    # Plot the impact point as a blue dot
    ax.plot(x, y, 'bo', markersize=10, label='Impact Point')
    
    # Add text near the impact point
    ax.text(x + 0.01, y + 0.01, f'Impact', color='white', fontsize=10)

    # Set the limits and aspect ratio to ensure the circle is displayed correctly
    ax.set_xlim(cue_ball_center[0] - cue_ball_radius - 0.01, cue_ball_center[0] + cue_ball_radius + 0.01)
    ax.set_ylim(cue_ball_center[1] - cue_ball_radius - 0.01, cue_ball_center[1] + cue_ball_radius + 0.01)
    
    ax.set_aspect('equal', 'box')

    plt.show()

def plot_table_with_trajectory(table_state_file, trajectory):
    with open(table_state_file, 'r') as f:
        data = json.load(f)

    table_state = data['table_state']
    balls = {name: (info['x'], info['y']) for name, info in table_state.items()}
    cue = balls['cue-ball']
    target = balls['target-ball']
    pocket = balls['pocket']

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal')
    ax.set_facecolor('seagreen')
    plt.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color='black')

    for name, (x, y) in balls.items():
        if name == 'cue-ball':
            plt.plot(x, y, 'wo', markersize=10, markeredgecolor='black', label='Cue Ball')
        elif name == 'target-ball':
            plt.plot(x, y, 'ro', markersize=10, label='Target Ball')
        elif name == 'pocket':
            plt.plot(x, y, 'ks', markersize=10, label='Pocket')
        else:
            ball_id = table_state[name]['id']
            plt.plot(x, y, 'bo', markersize=8)
            plt.text(x + 0.01, y + 0.01, str(ball_id), color='white', fontsize=8)

    # Draw the trajectory
    path_x, path_y = zip(*trajectory)
    plt.plot(path_x, path_y, 'y--', linewidth=2, label='Trajectory')

    plt.title('Billiard Table Layout with Trajectory')
    plt.legend(loc='upper right')
    plt.gca().invert_yaxis()
    plt.show()