"""
Step 2：Basic Object-Orientation Abstraction of The Ideal Rankine Cycle

Turbine

         inletNode inlet steam   
                 ┌────────┐
              ↓ ╱         │ 
               ┤          │
                ╲         │
                 └────────┤
                          ↓  exitNode exhausted steam   

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""

import node

class Turbine():

    """
    Turbine class

    Represents a turbine in the Rankine cycle
    """

    def __init__(self, inletNode,exitNode):
        """
        Initializes the turbine with nodes
        """
        self.inletNode = inletNode
        self.exitNode=exitNode
    
    def simulate(self,nodes):
        """
        Simulates the turbine 
        """
        nodes[self.exitNode].s=nodes[self.inletNode].s
        nodes[self.exitNode].ps()
      
        self.workExtracted = nodes[self.inletNode].h- nodes[self.exitNode].h 
