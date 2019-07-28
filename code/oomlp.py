#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  oomlp.py
#  
#  Copyright 2019  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

class Weight:
    learning_rate = 0.1
    def __init__ (self,weight):
        self.node_from = None
        self.node_to = None
        self.weight = weight
        self.delta = 0

    def output(self):
        return self.node_from.output * self.weight
        
    def calc_delta(self):
        self.delta = self.node_to.delta*self.node_from.output
    
    def update(self):
        self.calc_delta()
        self.weight-=Weight.learning_rate*self.delta
        


class Node:
    def __init__ (self,function,derivitive):
        self.weights_in=[]
        self.weights_out=[]
        self.value = 0.0
        self.output = 0.0
        self.error = 0.0
        self.delta = 0.0
        self.function = function
        self.derivitive = derivitive

        
    def feed_foward(self):
        self.value = 0.0
        for w in self.weights_in :
            self.value+=w.output()
        self.output = self.function(self.value)   

    def add_weight_in(self,weight):
        self.weights_in.append(weight)
        weight.node_to = self


    def add_weight_out(self,weight):
        self.weights_out.append(weight)
        weight.node_from = self

class NodeIn:
    def __init__ (self,output):
        self.weights_out=[]
        self.output = output


    def add_weight_out(self,weight):
        self.weights_out.append(weight)
        weight.node_from = self




def test1():
    input_node = NodeIn(0.9)
    hidden_node = Node((lambda x : x ),None)
    weight = Weight(0.5)
    input_node.add_weight_out(weight)
    hidden_node.add_weight_in(weight)
    hidden_node.feed_foward()
    print("value  :",hidden_node.value)
    print("output :",hidden_node.output)

def test2():
    X=[[8.5,0.65,1.2],[9.5,0.8,1.3],[9.9,0.8,0.5],[9.0,0.9,1.0]]
    y=[1,1,0,1]
    layer_0=[NodeIn(X[0][0]),NodeIn(X[0][1]),NodeIn(X[0][2])]
    print(layer_0[1].output)
    output_layer =[]
    output_layer.append(Node((lambda x : x ),None))
    weights_0 = [Weight(0.1),Weight(0.2),Weight(-0.1)]
    for i in range(len(weights_0)):
        layer_0[i].add_weight_out(weights_0[i])
        output_layer[0].add_weight_in(weights_0[i])
    for _ in range(1):
        for i in range(len(y)):
            for n in range(len(layer_0)):
                layer_0[n].output = X[i][n]
            output_layer[0].feed_foward()
            print("output :",output_layer[0].output)
            output_layer[0].delta = y[i]-output_layer[0].output
            print("delta  :",output_layer[0].delta )
            Weight.learning_rate = 0.01
            for w in weights_0:
                w.update()
                print(w.weight,end="  ")
            print()
            print()
    
def main(args):
    test2()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

