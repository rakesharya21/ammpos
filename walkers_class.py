#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 03:09:41 2021
walkers class
@author: rakesh
"""

# importing dependencies
import numpy as np
ar = np.array
add = np.add

from copy import copy

# creating Global Variables
cycles = []
apcycles = dict()
walkers = []
walkers_count = 1
MAX_STEPS = 12

# class Zvector:
#     def __init__(self, Z):
#         self.vector = Z
#         self.dimention = len(Z)

class Walker:
    
    def __init__(self, position, steps, odometer, path, ammonia_count, MAX_STEPS = MAX_STEPS):
        self.define_position(position)
        self.define_steps(steps)
        self.define_path(path)
        self.define_odometer(odometer)
        self.define_stamina(MAX_STEPS)
        self.define_neighbours()
        self.define_ammonia_count(ammonia_count)
        pass
    
    # class Position:
    def define_position(self, position):
        self.position = position
        pass
    
    def get_position(self):
        return self.position
    
    def text_position(self):
        return "".join(map(str, self.position))
    
    # class Steps:
    def define_steps(self, steps):
        self.steps = steps
        #print(self.steps)
        pass
    
    def get_steps(self):
        return self.steps
        
    # class Neighbours():
    def define_neighbours(self):
        N = dict()
        for step in self.steps:
            f = add(self.position, step)
            N["".join(map(str, f))] = f
            continue
        
        self.neighbours = N
        pass
    
    def get_neighbours(self):
        return self.neighbours
        
    def strange_neighbours(self):
        N = copy(self.get_neighbours())
        SN = dict()
        for n in N.keys():
            if n in self.text_path().split("->"):
                pass
            else:
                SN[n] = N[n]
            continue
        self.introduce = SN
        return copy(self.introduce)
    
    # def strange_non_negative_neighbours(self):
    #     N = copy(self.strange_neighbours())
    #     for n in N.keys():
            
        
    # Class path
    def define_path(self, path = []):
        self.path = path
        pass
    
    def text_path(self):
        #print(self.path,"asdf")
        #print("->".join(["".join(map(str, i)) for i in self.path]), "yo")
        return "->".join(["".join(map(str, i)) for i in self.path])
    
    # class odometer
    def define_odometer(self, odometer):
        self.odometer = odometer
        pass
    
    def read_odometer(self):
        return self.odometer
    
    def define_stamina(self, MAX_STEPS):
        self.MAX_STEPS = MAX_STEPS
        pass
    
    def get_stamina(self):
        return self.MAX_STEPS
    
    def define_ammonia_count(self, ac):
        self.ammonia_count = ac
        pass
    
    def get_ammonia_count(self):
        return self.ammonia_count
    
    #class Cycle_search_methods: 
    def BFCS(self, target = ""):#):
        if not target:
            target = "".join(map(str, self.position))
            pass
        
        global cycles
        global walkers
        global walkers_count
        
        for n in self.strange_neighbours().keys():
                #function get parameters for BFCS    
                p = self.strange_neighbours()[n]
                s = self.get_steps()
                o = self.read_odometer() + 1
                v = self.strange_neighbours()[n]-self.position
                vt = "".join(map(str, map(int, v)))
                ac = self.get_ammonia_count()
                if vt == "13":
                    ac += 1
                    pass
                elif vt == "-1-3":
                    ac -= 1
                    pass
                else:
                    pass
                pt = self.path + [self.strange_neighbours()[n]]
                
                #function add walker
                walkers += [Walker(p,s,o,pt,ac)]
                walkers_count += 1
                continue
        
        time = -1
        while len(walkers):
            time += 1
            w = walkers[0]
            if w.read_odometer() > self.get_stamina():
                pass
            elif w.text_position() == target and w.read_odometer()>1:
                cycles += [ar(w.path)]
                if w.get_ammonia_count() > 0:
                    apcycles[str(len(apcycles.keys()))+str(w.get_ammonia_count())]=ar(w.path)
                    pass
                if len(apcycles.keys())%1 == 0:
                    with open("cycles.dat",'a') as f:
                        f.write("".join(map(str, [time, "\t", len(cycles),"\t", len(apcycles),"\n"])))
                    pass
                
            else:
                for n in w.strange_neighbours().keys():
                    p = w.strange_neighbours()[n]
                    s = w.get_steps()
                    o = w.read_odometer() + 1
                    
                    ac = w.get_ammonia_count()
                    v = w.strange_neighbours()[n]-w.position
                    vt = "".join(map(str, map(int, v)))
                    
                    if vt == "13":
                        ac += 1
                        pass
                    elif vt == "-1-3":
                        ac -= 1
                        pass
                    else:
                        pass
                                            
                    pt = w.path + [w.strange_neighbours()[n]]
                    
                    #def add walker
                    walkers += [Walker(p,s,o,pt,ac)]
                    walkers_count += 1
                    continue
                pass
            
            walkers.pop(0)
            continue
        pass
    pass


   
# initialize a walker
m = MAX_STEPS
position = ar([0,0])
steps = ar([[2,0],[-2,0],[0,2],[0,-2],[1,3],[-1,-3]])
odometer = 0
path = []
W = Walker(position, steps, odometer, path, 0, MAX_STEPS=m)
walkers += [W]
W.BFCS()

# print the paths
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d

fig = plt.figure(figsize=(7,7))
#ax = fig.gca(projection='3d')
#ax.set_aspect('auto')


#do not run this function
def plot_cycles_together():
    C = 0
    for c in cycles:
        #print(c)
        C += 1
        xs = ar([i[0] for i in c])
        ys = ar([i[1] for i in c])
        zs = ar([C for i in range(len(c))])
        ax.scatter3D(xs[:-1], ys[:-1], zs[:-1])
        #ax.scatter3D(3*xs[:-1], 3*ys[:-1], -1+0*zs[:-1],c='w') 
        ax.scatter3D(xs[-1],ys[-1],zs[-1])
        ax.plot3D(xs,ys,zs,"gray")
        ax.plot3D([xs[0],xs[-1]],[ys[0],ys[-1]],[zs[0],zs[-1]],"gray")
        continue
    pass

def plot_apcycles():
    C = 0
    
    if len(apcycles.keys()):
        for c in apcycles.keys():
            plt.close("all")
#            ax = plt.subplot()
#            ax.set_aspect('auto')
            C += 1
            xs = ar([i[0] for i in apcycles[c]])
            ys = ar([i[1] for i in apcycles[c]])
            plt.scatter(xs[:-1], ys[:-1])
            #ax.scatter3D(3*xs[:-1], 3*ys[:-1], -1+0*zs[:-1],c='w') 
            plt.scatter(xs[-1],ys[-1])
            plt.plot(xs,ys,"gray")
            plt.plot([xs[0],xs[-1]],[ys[0],ys[-1]],"gray")
            plt.xlim((-6,+6))
            plt.ylim((-8,+8))
            plt.savefig("cycle_"+str(m)+"_"+str(len(apcycles[c]))+"_"+str(C))
            continue

#plot_cycles_together()
#plt.grid()
#fig.savefig("cycles_"+str(m))  
plot_apcycles() 
