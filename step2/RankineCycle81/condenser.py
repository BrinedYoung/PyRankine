"""
Step 2：Basic Object-Orientation Abstraction of The Ideal Rankine Cycle

Condenser

                    ↓   inletNode exhausted steam
                ┌───┴───┐
                │       │ 
                │       │
                │       │
                └───┬───┘  
                    ↓    exitNode condensate water 

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""

import node


class Condenser:
    """
    The condenser class
    """

    def __init__(self, inletNode, exitNode, inletNodeW, exitNodeW):
        """
        Initializes the condenser with nodes
        """
        self.inletNode = inletNode
        self.exitNode = exitNode
        self.inletNodeW = inletNodeW
        self.exitNodeW = exitNodeW

    def simulate(self, nodes, nodew, mdot):
        """
        Simulates the Condenser 
        """

        self.heatExtracted = nodes[self.inletNode].h - nodes[self.exitNode].h
        self.Qoutdot = mdot * self.heatExtracted / (3600*1000)
        self.mcwdot = (self.Qoutdot*1000*3600) / \
            (nodew[self.exitNodeW].h-nodew[self.inletNodeW].h)
