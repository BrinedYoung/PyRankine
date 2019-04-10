"""
Step 2：Basic Object-Orientation Abstraction of The Ideal Rankine Cycle
     
       object-oriented programming

The ideal rankine cycle as 
   
    ┌─── Node 0 ── Turbine ── Node 1 ──┐
    │                                  │
  Boiler                            Condenser
    │                                  │
    └─── Node 3 ──   Pump  ── Node 2 ──┘  

 Michael J . Moran. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011
        Chapter 8 : Vapour Power Systems
             Example 8.1:Analyzing an Ideal Rankine Cycle  Page 438

Running:

python rankine.py

License: this code is in the public domain

Author:Cheng Maohua
Email: cmh@seu.edu.cn

"""
import node
import turbine
import pump
import condenser
import boiler


def RankineCycle():
    boilerPressure = 8.0
    condenserPressure = 0.008
    Wcycledot = 100.00

    # 1 init nodes
    nodes = [node.Node() for i in range(4)]
    
    nodes[0].p = boilerPressure
    nodes[0].x = 1

    nodes[1].p = condenserPressure

    nodes[2].p = condenserPressure
    nodes[2].x = 0

    nodes[3].p = boilerPressure

    nodes[0].px()
    nodes[2].px()

    # 2 connect device
    t = turbine.Turbine(0, 1)
    p = pump.Pump(2, 3)
    b = boiler.Boiler(3, 0)

    # 3 simulate
    t.simulate(nodes)
    p.simulate(nodes)

    bwr = p.workRequired / t.workExtracted
    mdot = Wcycledot * 1000.0* 3600.0 / (t.workExtracted - p.workRequired)

    b.simulate(nodes, mdot)                  # in MW
    efficiency = (t.workExtracted - p.workRequired) / \
        (b.heatAdded)                # in MW

   # 4 condenser
    nodew = []
    for i in range(2):
        nodew.append(node.Node())

    nodew[0].t = 15
    nodew[0].x = 0
    nodew[1].t = 35
    nodew[1].x = 0
    nodew[0].tx()
    nodew[1].tx()

    c = condenser.Condenser(1, 2, 0, 1)
    c.simulate(nodes, nodew, mdot)

    print("Boiler Pressure: ", boilerPressure, "MPa")
    print("Condenser Pressure: ", condenserPressure, "MPa")
    print("The net power output of the cycle: ", Wcycledot, "MW")
    print("Cooling water enters the condenser T", nodew[0].t, "°C")
    print("Cooling water exits  the condenser T", nodew[1].t, "°C")
    print(" \n --------------------------------------------------")
    print("Efficiency: ", '%.2f' % (efficiency * 100), "%")
    print("The back work ratio: ", '%.2f' % (bwr * 100), "%")
    print("The mass flow rate: ",  '%.2f' % mdot, "%")
    print('The rate of heat transfer as the fluid passes the boiler: ',
          '%.2f' % b.Qindot, 'MW')
    print('The rate of heat transfer from the condensing steam: ',
          '%.2f' % c.Qoutdot, 'MW')
    print('The mass flow rate of the condenser cooling water: ', '%.2f' %
          c.mcwdot, 'kg/h')


if __name__ == '__main__':
    RankineCycle()
