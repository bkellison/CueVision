import json
import sys
import math
from typing import List, Tuple, Optional
from plot_table import plot_table_with_trajectory, plot_impact_point

# Constants
TABLE_WIDTH = 1.0
TABLE_HEIGHT = 1.0
BALL_RADIUS = 0.01  # Normalized units (2" diameter)
CUE_RADIUS = 0.009375  # Normalized units (1 7/8" diameter)

Point = Tuple[float, float]
Path = List[Point]

def distance(a: Point, b: Point) -> float:
    """Calculate the Euclidean distance between two points."""
    
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def angle_between(a: Point, b: Point, c: Point) -> float:
    """Calculate the angle between three points (a, b, c)."""
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    dot = ab[0] * cb[0] + ab[1] * cb[1]
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)
    
    if mag_ab == 0 or mag_cb == 0:
        return 0.0
    cos_angle = dot / (mag_ab * mag_cb)
    
    return math.degrees(math.acos(max(min(cos_angle, 1), -1)))

def angle_between_vectors(a: Point, b: Point, c: Point) -> float:
    """Calculate the angle between two vectors formed by points a-b and b-c."""
    ab = (b[0] - a[0], b[1] - a[1])
    bc = (c[0] - b[0], c[1] - b[1])

    dot = ab[0] * bc[0] + ab[1] * bc[1]
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    if mag_ab == 0 or mag_bc == 0:
        return 0.0
    
    cos_angle = dot / (mag_ab * mag_bc)
    cos_angle = max(min(cos_angle, 1), -1)
    
    return math.degrees(math.acos(cos_angle))


def is_path_blocked(a: Point, b: Point, ball: Point) -> bool:
    """Check if a ball blocks the path between two points."""
    ax, ay = a
    bx, by = b
    cx, cy = ball

    lab = distance(a, b)
    if lab == 0:
        return False

    ab = (bx - ax, by - ay)
    ac = (cx - ax, cy - ay)
    
    # Project ac onto ab to find the closest point on the line segment
    ab_len_squared = ab[0] ** 2 + ab[1] ** 2
    t = (ac[0] * ab[0] + ac[1] * ab[1]) / ab_len_squared
    t = max(0, min(1, t))

    # Find the closest point on the segment
    closest = (ax + ab[0] * t, ay + ab[1] * t)
    
    # Check distance from ball to closest point
    dist_to_closest = distance(closest, ball)

    return dist_to_closest < BALL_RADIUS * 2

# Shot score
def score_path(path: Path) -> float:
    """Score a path: lower is better (shorter distance, smaller angles).
        Angles less than 90° or greater than 270° are filtered out.
    """
    total_dist = sum(distance(path[i], path[i+1]) for i in range(len(path)-1))
    angles = 0
    for i in range(1, len(path)-1):
        angle = angle_between(path[i-1], path[i], path[i+1])
        
        # Exclude angles less than 90° or greater than 270°
        if angle < 90 or angle > 270:
            return -1
        angles += angle
    return total_dist + angles / 180

# Load data from table_state.json
def load_table_state(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def is_valid_shot(cue: Point, target: Point, pocket: Point) -> bool:
    """
    Check if the angle between the cue → target and target → pocket is between 90° and 270°.
    """
    angle = angle_between_vectors(cue, target, pocket)
    
    if 90 <= angle <= 270:
        return True
    else:
        return False

def point_on_circle(center: Point, angle: float, radius: float) -> Point:
    """Find the point on the circle at a given angle from the center."""
    x, y = center
    return (x + radius * math.cos(math.radians(angle)), y + radius * math.sin(math.radians(angle)))

def point_on_circle(center: Point, angle: float, radius: float) -> Point:
    """Find the point on the circle at a given angle from the center."""
    x, y = center
    return (x + radius * math.cos(math.radians(angle)), y + radius * math.sin(math.radians(angle)))

def calculate_impact_point(cue: Point, target: Point) -> Point:
    """
    Calculate the (x, y) impact point ON THE SURFACE of the cue ball relative to its center.
    Returns coordinates between -CUE_RADIUS and +CUE_RADIUS.
    """
    dx = target[0] - cue[0]
    dy = target[1] - cue[1]
    line_angle = math.degrees(math.atan2(dy, dx))

    # Find the surface point along that angle
    impact_point_world = point_on_circle(cue, line_angle, CUE_RADIUS)

    # Offset relative to cue ball center (for graphing)
    relative_impact_point = (impact_point_world[0] - cue[0], impact_point_world[1] - cue[1])

    return relative_impact_point

def find_best_path(cue: Point, target: Point, pocket: Point, balls: List[Point], max_depth: int = 2) -> Optional[List[Tuple[float, float]]]:
    """
    Find the best path from cue to target to pocket possibly with up to `max_depth` intermediate contacts.
    Instead of returning points, returns the y=mx+b lines between points.
    """

    def dfs(current_path: Path, remaining_balls: List[Point], depth: int) -> List[Path]:
        """Depth-first search for possible shot paths."""
        paths = []

        if depth > max_depth:
            return paths

        last_point = current_path[-1]

        # Try direct shot to pocket
        if all(not is_path_blocked(last_point, pocket, b) for b in remaining_balls):
            complete_path = current_path + [pocket]
            paths.append(complete_path)

        # Try banking off other balls
        for ball in remaining_balls:
            if ball == last_point:
                continue
            if all(not is_path_blocked(last_point, ball, b) for b in remaining_balls if b != ball):
                new_path = current_path + [ball]
                new_remaining = [b for b in remaining_balls if b != ball]
                paths.extend(dfs(new_path, new_remaining, depth + 1))
        return paths

    # Start search from cue to target
    obstacles = [b for b in balls if b != cue and b != target]
    if any(is_path_blocked(cue, target, b) for b in obstacles):
        return None

    initial_path = [cue, target]
    all_paths = dfs(initial_path, obstacles, 0)

    if not all_paths:
        return None

    # Score all paths and pick the best one
    scored_paths = [(score_path(path), path) for path in all_paths if score_path(path) != -1]
    if not scored_paths:
        return None

    scored_paths.sort()
    best_path = scored_paths[0][1]

    # Calculate the impact point on the cue ball based on the desired trajectory
    impact_point = calculate_impact_point(cue, target)
    plot_impact_point(impact_point, CUE_RADIUS)

    # Now instead of returning points, return the lines (m, b) between each consecutive point
    line_segments = []
    for i in range(len(best_path) - 1):
        p1, p2 = best_path[i], best_path[i+1]
        x1, y1 = p1
        x2, y2 = p2
        
        if x2 == x1:  # vertical line case
            m = float('inf')  # or None, depending on how you want to handle verticals
            b = x1           # for vertical lines, store x = b
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
        
        line_segments.append((m, b))
    
    return best_path, line_segments


# Main function to run the simulation with the new shot validation
def main():
    # Load table state
    table_state = load_table_state('ball-identification/table_state.json')['table_state']

    # Extract balls and positions (filter for balls by checking the id)
    balls = [(ball['x'], ball['y']) for key, ball in table_state.items() if 'ball' in key]
    cue = (table_state['cue-ball']['x'], table_state['cue-ball']['y'])
    target = (table_state['target-ball']['x'], table_state['target-ball']['y'])
    pocket = (table_state['pocket']['x'], table_state['pocket']['y'])

    
    best_path, line_segments = find_best_path(cue, target, pocket, balls)
    if best_path:
        plot_table_with_trajectory('ball-identification/table_state.json', best_path)
        
    return json.dumps({"trajectory": line_segments})


if __name__ == "__main__":
    table_state = json.loads(sys.argv[1])
            
    balls = [(ball['x'], ball['y']) for key, ball in table_state.items() if 'ball' in key]
    cue = (table_state['cue-ball']['x'], table_state['cue-ball']['y'])
    target = (table_state['target-ball']['x'], table_state['target-ball']['y'])
    pocket = (table_state['pocket']['x'], table_state['pocket']['y'])
    
    best_path, line_segments = find_best_path(cue, target, pocket, balls)
    impact_point = calculate_impact_point(cue, target)

    # Example dummy output
    result = {
        "trajectory": line_segments,
        "cue_impact": impact_point
    }

    # Output to stdout
    print(json.dumps(result), flush=True)