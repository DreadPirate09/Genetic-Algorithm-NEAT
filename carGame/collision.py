import math

# Function to rotate a point around another point
def rotate_point(point, angle, pivot):
    x, y = point
    px, py = pivot
    rotated_x = math.cos(math.radians(angle)) * (x - px) - math.sin(math.radians(angle)) * (y - py) + px
    rotated_y = math.sin(math.radians(angle)) * (x - px) + math.cos(math.radians(angle)) * (y - py) + py
    return (rotated_x, rotated_y)

# Function to check collision between two rectangles
def is_collision(rect1, rect2):
    return not (rect1[0] + rect1[2] < rect2[0] or rect1[0] > rect2[0] + rect2[2] or
                rect1[1] + rect1[3] < rect2[1] or rect1[1] > rect2[1] + rect2[3])

# Function to check collision between a rotated square and a regular square
def is_collision_rotated(rotated_rect, rect):
    # Check collision between the rotated rectangle and the regular rectangle
    if is_collision(rotated_rect, rect):
        # If collision detected, check each corner of the rotated rectangle
        # If any corner is inside the regular rectangle, return True (collision detected)
        for point in [(rotated_rect[0], rotated_rect[1]),
                      (rotated_rect[0] + rotated_rect[2], rotated_rect[1]),
                      (rotated_rect[0] + rotated_rect[2], rotated_rect[1] + rotated_rect[3]),
                      (rotated_rect[0], rotated_rect[1] + rotated_rect[3])]:
            if rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]:
                return True
    return False

# Define two squares
square1 = (300, 200, 100, 100)  # x, y, width, height
square2 = (400, 300, 100, 100)

# Rotate square1 by 5 degrees
center = (square1[0] + square1[2] // 2, square1[1] + square1[3] // 2)  # Center of square1
rotated_square1 = tuple(round(coord) for coord in rotate_point((300,200), 0, center))

print(rotated_square1)

# Check for collision between rotated square1 and square2
if is_collision_rotated(rotated_square1 + square1[2:], square2):
    print("Collision detected!")