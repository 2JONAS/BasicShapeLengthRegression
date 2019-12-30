
import numpy as np
import math
import random
from torch.utils.data import Dataset
class Scan():
    def __init__(self):
        self.theta_range =np.array([i*math.pi/180 for i in range(0,360)]).reshape((360,1))
        self.alpha_range = np.array([j*math.pi/180  for j in range(0,180)]).reshape((180,1))
    def get_angle(self):
        np.random.shuffle(self.theta_range)
        np.random.shuffle(self.alpha_range)
        return (self.theta_range[0],self.alpha_range[0])

class Point():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def tolist(self):
        return [self.x,self.y,self.z]
class Circle():
    def __init__(self,radius=10,points_num=1024):
        self.radius = radius
        self.points_num = points_num
        self.points = list()
        self.make_points()
    def make_points(self):
        for p in range(self.points_num):
            self.points.append(self.make_point(*scanner.get_angle()))
    def make_point(self,theta,alpha):
        r_ = self.radius * math.cos(alpha)
        x = abs(r_) * math.cos(theta)
        y = abs(r_) * math.sin(theta)
        try:
            z = math.sqrt(self.radius*self.radius-x*x-y*y)
        except:
            z = 0
        if r_ < 0:
            z = z*-1
        return Point(x,y,z).tolist()
    def tonp(self):
        return np.array(self.points)
class Cube():
    def __init__(self,l=10,w=10,h=10,points_num=1024):
        self.l = l
        self.w = w
        self.h = h
        self.points = list()
        self.points_num = points_num
        self.picth_angle_max = math.atan(self.h/self.w)
        self.heading_angle_max = math.atan(self.l/self.w)
        self.make_points()
    def make_points(self):
        for p in range(self.points_num):
            w = self.make_point(*scanner.get_angle())
            if w is not None:
                self.points.append(w)
    def make_point(self,theta,alpha):
        alpha = alpha - math.pi/2
        if abs(alpha) > self.picth_angle_max:
            z = self.h/2
            x = z / math.tan(alpha)
            y = x * math.tan(theta)

        else:
            if (theta >= self.heading_angle_max and theta <= math.pi-self.heading_angle_max) or\
                    (theta >= self.heading_angle_max + math.pi and theta <= 2*math.pi-self.heading_angle_max):
                y = self.l/2
                x = y/math.tan(theta)
                z = y*math.tan(alpha)
            else:
                x = self.w/2
                y = x*math.tan(theta)
                z = x*math.tan(alpha)
        x,y,z = abs(x),abs(y),abs(z)
        if alpha < 0:
            z = -1 * abs(z)
        if not (theta <= math.pi / 2 or theta >= math.pi * 3 / 2):
            x = abs(x) * -1
        if not theta >= math.pi:
            y = abs(y) * -1
        x = max(min(x, self.w / 2), -self.w / 2)
        y = max(min(y, self.l / 2), -self.l / 2)
        z = max(min(z, self.h / 2), -self.h / 2)
        return Point(x,y,z).tolist()
    def tonp(self):
        return np.array(self.points)

class CircleFactory(object):
    def __init__(self):
        super(CircleFactory,self).__init__()
    def make_circle(self):
        r = random.randrange(15,35)
        return Circle(r,1024).tonp(),r,0


class CubeFactory(object):
    def __init__(self):
        super(CubeFactory,self).__init__()
    def make_cube(self):
        l = random.randrange(15,35)
        return Cube(l=l,w=l,h=l,points_num=1024).tonp(),l,1

class DataGen(Dataset):
    def __init__(self,num):
        super(DataGen,self).__init__()
        self.num = num
        self.circle_f = CircleFactory()
        self.cube_f = CubeFactory()
    def __len__(self):
        return self.num
    def __getitem__(self, index):
        if random.randrange(0,2):
            return self.circle_f.make_circle()
        else:
            return self.cube_f.make_cube()

scanner = Scan()

# CF = CircleFactory()
# CubeF = CubeFactory()
# CubeF = CubeFactory()
# w = CubeF[0]
# print(w)
# import pptk
# v = pptk.viewer(np.naddary)

