# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

# def CirclesOverlap (c1, c2):
#     dist12 = np.sqrt( (c1.x - c2.x)**2 + (c1.y - c2.y)**2 )
#     if dist12 < c1.radius + c2.radius:
#         return True # if overlaps
#     return False 

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices



class myTriangle():
    def __init__(self, radius=50, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.vertices = getRegularPolygon(3, radius=self.radius)

        self.color = color

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position
        pygame.draw.polygon(screen, self.color, points)
#

class myPolygon():
    def __init__(self, nvertices = 3, radius=70, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.nvertices = nvertices
        self.vertices = getRegularPolygon(self.nvertices, radius=self.radius)

        self.color = color
        self.color_org = color 

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position

        pygame.draw.polygon(screen, self.color, points)
#

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("assets/diyong.mp3")
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 200
    h = 40
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]

    w1 = 100
    h1 = 20
    Y = np.array([ [0,0], [w1, 0], [w1, h1], [0, h1] ])

    w2 = 40
    h2 = 20
    Z = np.array([ [0,0], [w2, 0], [w2, h2], [0, h2] ])



    joint_1 = 0
    joint_2 = 0
    joint_3 = 0
    joint_4 = 0
    grab = 0
    joint_1dx = 0
    joint_2dx = 0
    joint_3dx = 0
    joint_4dx = 0


    tick = 0

    done = False
    while not done:
        tick += 1
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    joint_1dx = -3
                elif event.key == pygame.K_w:
                    joint_1dx = 3
                elif event.key == pygame.K_a:
                    joint_2dx = -3
                elif event.key == pygame.K_s:
                    joint_2dx = 3
                elif event.key == pygame.K_z:
                    joint_3dx = -3
                elif event.key == pygame.K_x:
                    joint_3dx = 3
                elif event.key == pygame.K_1:
                    joint_4dx = -1
                elif event.key == pygame.K_2:
                    joint_4dx = 1
                elif event.key == pygame.K_SPACE:
                    while grab <= 25:
                        grab += 1

        # 키가 놓일 경우
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q or event.key == pygame.K_w:
                    joint_1dx = 0
                elif event.key == pygame.K_a or event.key == pygame.K_s:
                    joint_2dx = 0
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    joint_3dx = 0
                elif event.key == pygame.K_1 or event.key == pygame.K_2:
                    joint_4dx = 0
                elif event.key == pygame.K_SPACE:
                    while grab >= 0:
                        grab -= 1
                
        
        joint_1 += joint_1dx
        joint_2 += joint_2dx
        joint_3 += joint_3dx
        joint_4 += joint_4dx
        


        # drawing
        screen.fill( (200, 254, 219))

        # base
        pygame.draw.circle(screen, (255,0,0), position, radius=3)
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(X, H0, screen, (0,0,0)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)  
        x, y = H1[0,2], H1[1,2] # joint position
        H11 = H1 @ Rmat(-90) @ Tmat(0,-h/2)
        H12 = H11 @ Tmat(0, h/2) @ Rmat(joint_1) @ Tmat(0, -h/2)    
        draw(X, H12, screen, (200,200,0)) # arm 1, 90 degree

        # arm 2
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H21 = H2 @ Rmat(joint_2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0,0, 200))

        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H31 = H3 @ Rmat(joint_3) @ Tmat(0, -h/2)
        draw(X, H31, screen, (0,0, 200))

        H4 = H31 @ Tmat(w,h/2) @ Rmat(90 + joint_4) @Tmat(-w1/2, -h1/2)
        draw(Y, H4, screen, (0,0, 200))

        H41 = H4 @Tmat(grab,0) @ Rmat(-90)
        draw(Z,H41, screen, (0,0, 200))

        H42 = H4 @Tmat(-grab,0) @ Rmat(-90) @Tmat(0,w1 - h2) 
        draw(Z,H42, screen, (0,0, 200))

    
        # pygame.draw.circle(screen, RED, (cx, cy), radius=3)
        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()