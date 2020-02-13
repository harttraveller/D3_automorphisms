import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

class Point:
    def __init__(self,x,y,label,color):
        self.x = x
        self.y = y
        self.label = label
        self.color = color

class D3:
    ### INITIALIZATION FUNCTION
    def __init__(self):
        self.original_points = [Point(0,1,'a','red'),
                               Point(-0.8660254037844387, -0.4999999999999998,'b','blue'),
                               Point(0.8660254037844384, -0.5000000000000003,'c','green')]

        self.transformed_points = self.original_points
        self.tset_dict = self.transformation_set()
        pd.options.mode.chained_assignment = None

    ### INTERNAL MATH FUNCTIONS
    def deg2rad(self,deg):
        return deg*(np.pi/180)

    def rotate(self,point,angle):
        origin = (0,0)
        angle = self.deg2rad(angle)
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    def deg2slope(self,deg):
        if deg == 90:
            deg += 1/1e10
        return np.sin(self.deg2rad(deg))/np.cos(self.deg2rad(deg))

    def reflect(self,point,angle):
        m = self.deg2slope(angle)
        d = (point[0] + (point[1]*m))/(1 + m**2)
        x1 = (2*d) - point[0]
        y1 = (2*d*m) - point[1]
        return (x1,y1)

    ### TRANSFORMATIONS
    def I(self):
        # Identity, changes nothing
        pass

    def R1(self):
        # Rotation of 120 degrees about origin
        new_points = []
        for i in self.transformed_points:
            x,y,label,color = i.x,i.y,i.label,i.color
            new_x,new_y = self.rotate((x,y),120)
            new_points.append(Point(new_x,new_y,label,color))
        self.transformed_points = new_points


    def R2(self):
        # Rotation of 240 degrees about origin
        new_points = []
        for i in self.transformed_points:
            x,y,label,color = i.x,i.y,i.label,i.color
            new_x,new_y = self.rotate((x,y),240)
            new_points.append(Point(new_x,new_y,label,color))
        self.transformed_points = new_points

    def S1(self):
        # Reflection about 45 degree line
        new_points = []
        for i in self.transformed_points:
            x,y,label,color = i.x,i.y,i.label,i.color
            new_x,new_y = self.reflect((x,y),30)
            new_points.append(Point(new_x,new_y,label,color))
        self.transformed_points = new_points

    def S2(self):
        # Reflection about 90 degree line
        new_points = []
        for i in self.transformed_points:
            x,y,label,color = i.x,i.y,i.label,i.color
            new_x,new_y = self.reflect((x,y),90)
            new_points.append(Point(new_x,new_y,label,color))
        self.transformed_points = new_points

    def S3(self):
        # Reflection about 135 degree line
        new_points = []
        for i in self.transformed_points:
            x,y,label,color = i.x,i.y,i.label,i.color
            new_x,new_y = self.reflect((x,y),150)
            new_points.append(Point(new_x,new_y,label,color))
        self.transformed_points = new_points

    def apply(self,transforms):
        # apply a sequence of transformations
        for i in transforms:
            getattr(self,i)()


    ### RESET TRANSFORMED POINTS TO ORIGINAL
    def reset(self):
        self.transformed_points = self.original_points

    ### SHOW THE LABELED (transformed) POINTS
    def plot(self):
        fig = plt.figure(figsize=(4,4))
        ax = fig.add_subplot(111)
        for point in self.transformed_points:
            ax.text(point.x,point.y,point.label,color=point.color,fontsize=30)
        plt.xlim(-3,3)
        plt.ylim(-3,3)
        plt.xticks([])
        plt.yticks([])
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.show()

    ### GENERATING CALEY TABLE

    def transformation_set(self):
        # what point set results from each single transformation?
        transformation_order = ['I','R1','R2','S1','S2','S3']
        # transformation set dictionary
        tset_dict = {}
        for transformation in transformation_order:
            getattr(self,transformation)()
            pset_dict = {}
            for point in self.transformed_points:
                pset_dict['{}'.format(point.label)] = (round(point.x,2),round(point.y,2))
            tset_dict['{}'.format(transformation)] = pset_dict
            self.reset()
        return tset_dict

    def get_current_state(self):
        # what would the current set of transformed points correspond to as a single transformation?
        pset_dict = {}
        for point in self.transformed_points:
            pset_dict['{}'.format(point.label)] = (round(point.x,2),round(point.y,2))
        for k,v in self.tset_dict.items():
            if pset_dict == v:
                return k

    def table(self,transformation_order):
        # once caley table generator function is complete,
        # simply run on every ordered combination of
        # transformations
        caley_table = pd.DataFrame(np.zeros((len(transformation_order),len(transformation_order))))
        caley_table.index = transformation_order
        caley_table.columns = transformation_order
        self.reset()
        for i in transformation_order:
            for j in transformation_order:
                self.apply([i,j])
                state = self.get_current_state()
                caley_table[i][j] = state
                self.reset()
        return caley_table
