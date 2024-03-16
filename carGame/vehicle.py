import pygame
import math

VEHICLE_WIDTH = 50
VEHICLE_HEIGHT = 100

angle_maps = [40, 20, 0, -20, -40]

class Sensor(pygame.sprite.Sprite):

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle

        image = pygame.image.load('images/sensorColor.png')
        self.image = pygame.transform.scale(image, (5, 200))
        self.width, self.height = image.get_size()
        self.rect = self.image.get_rect()

    def updateSensorAlongWithSquare(self, Player, angle):
        self.angle = self.angle + angle

        print('update with the following sensor')
        print(angle)

        rotatedSquare =  Player.rotate_point(tuple([Player.x,Player.y]), Player.angle, tuple(Player.center))
        self.rect.x, self.rect.y = rotatedSquare[0] + Player.width / 2, rotatedSquare[1] - 100
        self.rect.center = [self.rect.x - Player.width/2, self.rect.y]

        image = pygame.image.load('images/sensorColor.png')
        self.image = pygame.transform.rotate(image, angle)
        print('widht:'+str(self.image.get_size()[0]))
        if angle <= 0 :
            self.rect = self.image.get_rect(center=[self.rect.x + self.image.get_size()[0]*1.5-8,self.rect.center[1] - 50])
        else:
            self.rect = self.image.get_rect(center=[self.rect.x - self.image.get_size()[0]+18,self.rect.center[1] - 50])



class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        self.image = pygame.transform.scale(image, (VEHICLE_WIDTH, VEHICLE_HEIGHT))
        self.width, self.height = VEHICLE_WIDTH , VEHICLE_HEIGHT
        self.rect = self.image.get_rect()
        self.rect.center = [x+self.width/2, y+self.height/2]
        self.x = x
        self.y = y
        self.center = [x+self.width/2, y+self.height/2]


class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)
        self.width, self.height = image.get_size()
        self.center = [x+self.width/2, y+self.height/2]
        self.x = x
        self.y = y
        self.angle = 0

        self.sensors = []

        # for i in range(5):
        #     self.sensors.append(Sensor(self.x, self.y, self.angle + angle_maps[i]))



    # movement functions

    def moveLeft(self):
        self.angle += 4
        self.rotateVehicle()
        self.x -= 2
        self.rect.center = [self.x, self.y]
        # for s in range(len(self.sensors)):
        #     # self.sensors[s].rect.x = self.x
        #     # self.sensors[s].rect.y = self.y
        #     self.sensors[s].updateSensorAlongWithSquare(self, self.angle + angle_maps[s])

    def moveRight(self):
        self.angle -= 4
        self.rotateVehicle()
        self.x += 2
        self.rect.center = [self.x, self.y]
        # for s in range(len(self.sensors)):
        #     # self.sensors[s].rect.x = self.x
        #     # self.sensors[s].rect.y = self.y
        #     self.sensors[s].updateSensorAlongWithSquare(self, self.angle + angle_maps[s])

    def updatePos(self, velocity):
        self.x -= velocity*(self.angle / 360)
        self.rect.center = [self.x, self.y]
        # for s in range(len(self.sensors)):
        #     # self.sensors[s].rect.x = self.x
        #     # self.sensors[s].rect.y = self.y
        #     self.sensors[s].updateSensorAlongWithSquare(self, self.angle)

    def rotateVehicle(self):
        image = pygame.image.load('images/car.png')
        self.image = pygame.transform.rotate(image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    #-------------------------------------------------------------

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
    # use this for the lane collision as well
    # verify if is a vehicle that colides , if not , create a long rect with the x pos of the lane
    def is_collision_rotated(self, rectCol):
        # Define two squares
        rect = (rectCol.rect.x + rectCol.width/2, rectCol.rect.y + rectCol.height/2, rectCol.width, rectCol.height)
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
                    print("These ones collide")
                    print(rotated_square1)
                    print(rect)
                    return True
        return False


