"""
Step 3-json ：Basic Object-Orientation Abstraction  and Data Representation of The Ideal Rankine Cycle

 class Pump

                ┌───────┐
                │       │
    exitNode   ← ┼───────┼← inletNode
                │       │
                └───────┘  
  
  Author:Cheng Maohua  Email: cmh@seu.edu.cn               
"""
import seuif97
import node


class Pump():

    """
    Pump class： Represents a pump in the Rankine cycle
    """

    def __init__(self, dictDev):
        """
        Initializes the pump with nodes
        """
        self.name = dictDev['name']
        self.inletNode = dictDev['inNode']
        self.exitNode = dictDev['exNode']

    def state(self, nodes):
        #nodes[self.exitNode].s = nodes[self.inletNode].s
        #nodes[self.exitNode].h = nodes[self.inletNode].h + nodes[self.inletNode].v * \
        #    (nodes[self.exitNode].p - nodes[self.inletNode].p) * 1000
        # nodes[self.exitNode].hs()

        sout_s = nodes[self.inletNode].s
        hout_s = seuif97.ps2h(nodes[self.exitNode].p, sout_s)
        nodes[self.exitNode].h =  nodes[self.inletNode].h +(hout_s -  nodes[self.inletNode].h)
        nodes[self.exitNode].ph()    
        

    def simulate(self, nodes):
        """
        Simulates the pump 
        """
        self.workRequired = nodes[self.exitNode].h - nodes[self.inletNode].h

    def mdotenergy(self, mdot):
        self.WRequired = mdot * self.workRequired
