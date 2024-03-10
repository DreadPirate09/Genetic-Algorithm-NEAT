import pygame
import math

VEHICLE_WIDTH = 50
VEHICLE_HEIGHT = 100

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        self.image = pygame.transform.scale(image, (VEHICLE_WIDTH, VEHICLE_HEIGHT))
        self.width, self.height = image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = [x+self.width/2,y+self.height/2]
        self.x = x
        self.y = y
        self.center = [x+self.width/2,y+self.height/2]


class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)
        self.width, self.height = image.get_size()
        self.center = [x+self.width/2,y+self.height/2]
        self.x = x
        self.y = y
        self.angle = 0

    def moveLeft(self):
        self.angle += 2
        self.rotateVehicle()
        self.x -= 2
        self.rect.center = [self.x, self.y]

    def moveRight(self):
        self.angle -= 2
        self.rotateVehicle()
        self.x += 2
        self.rect.center = [self.x, self.y]

    def updatePos(self, velocity):
    	self.x -= velocity*(self.angle / 360)
    	self.rect.center = [self.x, self.y]

    def rotateVehicle(self):
        # Load the original image
        image = pygame.image.load('images/car.png')
        # Rotate the original image by the current angle
        self.image = pygame.transform.rotate(image, self.angle)
        # Update the rectangle position
        self.rect = self.image.get_rect(center=self.rect.center)

       # Function to rotate a point around another point
    def rotate_point(self, point, angle, pivot):
        x, y = point
        px, py = pivot
        rotated_x = math.cos(math.radians(angle)) * (x - px) - math.sin(math.radians(angle)) * (y - py) + px
        rotated_y = math.sin(math.radians(angle)) * (x - px) + math.cos(math.radians(angle)) * (y - py) + py
        return (rotated_x, rotated_y)

    # Function to check collision between two rectangles
    def is_collision(self, rect1, rect2):
        return not (rect1[0] + rect1[2] < rect2[0] or rect1[0] > rect2[0] + rect2[2] or
                    rect1[1] + rect1[3] < rect2[1] or rect1[1] > rect2[1] + rect2[3])

    # Function to check collision between a rotated square and a regular square
    def is_collision_rotated(self, Vehicle):
        # Define two squares
        rect = (Vehicle.rect.x + Vehicle.width/2, Vehicle.rect.y + Vehicle.height/2, Vehicle.width, Vehicle.height)

        # Rotate square1 by 5 degrees
        rotated_square1 = tuple(round(coord) for coord in self.rotate_point(tuple([self.x,self.y]), self.angle, tuple(self.center)) + tuple([self.width, self.height]))

        # Check collision between the rotated rectangle and the regular rectangle
        if self.is_collision(rotated_square1, rect):
            # If collision detected, check each corner of the rotated rectangle
            # If any corner is inside the regular rectangle, return True (collision detected)
            for point in [(rotated_square1[0], rotated_square1[1]),
                          (rotated_square1[0] + rotated_square1[2], rotated_square1[1]),
                          (rotated_square1[0] + rotated_square1[2], rotated_square1[1] + rotated_square1[3]),
                          (rotated_square1[0], rotated_square1[1] + rotated_square1[3])]:
                if rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]:
                    return True
        return False


