import pygame
from pygame.locals import *
import random
from vehicle import Vehicle, PlayerVehicle
from colors import *
from network import *
import datetime
import math

lastActionFw = datetime.datetime.now()

def delay(microsec):

    global lastActionFw
    now = datetime.datetime.now()

    print('now:')
    print(now.microsecond)
    print('last:')
    print(lastActionFw.microsecond)


    if now.microsecond - lastActionFw.microsecond:
        lastActionFw = datetime.datetime.now()
        print('delay true')
        return True
    else:
        print('delay false')
        return False

pygame.init()

control = 'NN'
neurons = [3, 4, 2]
network = NeuralNetwork(neurons)
input_values = [ 0.5 , 0.3 , 0.8]
output = NeuralNetwork.feed_forward(input_values, network)

# create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# player's starting coordinates
player_x = 250
player_y = 400

# frame settings
clock = pygame.time.Clock()
fps = 120

# game settings
gameover = False
speed = 1.5
score = 0

# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)
# player_group.add(player.sensors[0])
# player_group.add(player.sensors[1])
# player_group.add(player.sensors[2])
# player_group.add(player.sensors[3])
# player_group.add(player.sensors[4])

# lane coordinates
left_lane = 150
center_lane =250
right_lane = 300
road_width = 300
marker_width = 10
marker_height = 50
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)
lanes = [left_lane, center_lane, right_lane]
lane_marker_move_y = 0

def draw_road():
    global lane_marker_move_y
    global left_edge_marker
    global right_edge_marker
    global marker_width
    global marker_height
    # road and marker sizes


    # road and edge markers
    road = (100, 0, road_width, height)

    # draw the grass
    screen.fill([0,0,0])
    # draw the road
    pygame.draw.rect(screen, gray, road)
    # draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    # draw the lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    print(lane_marker_move_y)

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

# load the vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    # image = pygame.image.load('images/' + image_filename)
    image = pygame.Surface((50, 100))
    image.fill((1,1,1))
    vehicle_images.append(image)
    
# load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# game loop
running = True
while running:
    
    clock.tick(fps)
    player.updatePos(50)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # move the player's car using the left/right arrow keys
        if (event.type == KEYDOWN and control != 'NN') or control == 'NN':

            if control != 'NN':
                if event.key == K_LEFT and player.rect.center[0] > left_lane:
                    player.moveLeft()
                elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                    player.moveRight()
            else:
                if output[0] != output[1]:
                    if output[0] == 1 and delay(0.1):
                        player.moveLeft()
                        print('move left when output[0] is '+str(output[0]))
                    elif output[1] == 1 and delay(0.1):
                        player.moveRight()
                        print('move Right when output[1] is '+str(output[1]))
                    
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if player.is_collision_rotated(vehicle) or player.x < left_edge_marker[0] or player.x > right_edge_marker[0]:
                    print('looks like is true')
                    
                    gameover = True
                    
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.center[1] + vehicle.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.center[1] + vehicle.center[1]) / 2]
            
    draw_road()
        
    # draw the player's car
    player_group.draw(screen)
    
    # add a vehicle
    if len(vehicle_group) < 2:
        
        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            
            # select a random lane
            lane = random.choice(lanes)
            
            # select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        # remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            # add to score
            score += 1
            # speed up the game after passing 5 vehicles
            # if score > 0 and score % 5 == 0:
            #     speed += 1
    
    # draw the vehiclesis_collision2
    vehicle_group.draw(screen)
    
    # display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    
    # check if there's a head on collision
    for vehicle in vehicle_group:
        if player.is_collision_rotated(vehicle) or player.x < left_edge_marker[0] or player.x > right_edge_marker[0]:
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]
            
    # display game over
    if gameover:
        screen.blit(crash, crash_rect)
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
            

    for v in vehicle_group:
        distNextVehicle = 0
        if v.rect.y > 0:
            print('This vehicle is at : '+str(v.rect.x)+' '+str(v.rect.y))
            print('Distanta dintre acest vehicul si player este de :')
            distNextVehicle = math.sqrt((v.rect.center[0] - player.rect.center[0])**2 + (v.rect.center[0] - player.rect.center[0])**2)
            print(distNextVehicle)
        distFromRight = right_lane - player.rect.center[0] + 100
        distFromLeft  = player.rect.center[0] - left_lane + 50

        print('Distanta pana in dreapta')
        print(distFromRight)
        print('Distanta pana in stanga')
        print(distFromLeft)

        input_values = [ distNextVehicle , distFromRight , distFromLeft ]
        output = NeuralNetwork.feed_forward(input_values, network)
        print(output)

    pygame.display.update()

    # wait for user's input to play again or exit
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # get the user's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    player.x = 250
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()