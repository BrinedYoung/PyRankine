"""
Step5: The Base Class of Components and Textual Representation

Main Module: 
    1 RankineCycle: the class of Rankine Cycle 
    2 SimRankineCycle: the simulator of Rankine Cycle 
  
Last updated: 2019·.01.10

Author:Cheng Maohua(cmh@seu.edu.cn)

"""
import datetime
import json
import sys

import numpy as np

from components.node import Node

from components.boiler import Boiler
from components.condenser import Condenser
from components.openedheaterdw0 import OpenedheaterDw0
from components.pump import Pump
from components.turbineex0 import TurbineEx0
from components.turbineex1 import TurbineEx1

# -------------------------------------------------------------------
# compdict
#  1: key:value-> Type String: class  name
#  2  add the new key:value to the dict after you and the new device class/type
# --------------------------------------------------------------------------

compdict = {
    "BOILER": Boiler,
    "CONDENSER": Condenser,
    "TURBINE-EX1": TurbineEx1,
    "TURBINE-EX0": TurbineEx0,
    "PUMP": Pump,
    "FWH-OPENDED-DW0": OpenedheaterDw0
}


def read_jsonfile(filename):
    """ rankine cycle in json file"""

    # 1 read json file to dict
    with open(filename, 'r') as f:
        rkcyc = json.load(f)
        #rkcyc = json.loads(f.read())

    # print(rkcyc)
    name = rkcyc["name"]
    dictnodes = rkcyc["nodes"]
    dictcomps = rkcyc["comps"]

    # 2 convert dict to the object of nodes
    countNodes = len(dictnodes)
    nodes = [None for i in range(countNodes)]
    for curnode in dictnodes:
        nodes[int(curnode['id'])] = Node(curnode)
 
    # 3 convert dict to the object of Comps
    DevNum = len(dictcomps)
    Comps = {}
    for curdev in dictcomps:
        Comps[curdev['name']] = compdict[curdev['type']](curdev)

    return name, nodes, countNodes, Comps, DevNum


class RankineCycle(object):

    def __init__(self):
        """
          self.nodes : list of all nodes
          self.Comps : dict of all components
        """
        self.name = None
        self.nodes = []
        self.Comps = {}
        self.NodehNum = 0
        self.DevNum = 0
        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalWExtracted = 0
        self.totalWRequired = 0

        self.totalheatAdded = 0
        self.totalQAdded = 0

        self.netpoweroutput = 0
        self.efficiency = 100.0

        self.mdot = None
        self.Wcycledot = None

        self.fdotok = False

    def addRankine(self, filename):
        self.name, self.nodes, self.NodeNum, self.Comps, self.DevNum = read_jsonfile(
            filename)

    def componentState(self):
        for key in self.Comps:
            self.Comps[key].state(self.nodes)

    def cycleFdot(self):

        i = 0  # to avoid endless loop
        keys = list(self.Comps.keys())
        while (self.fdotok == False):

            for key in keys:
                self.Comps[key].fdot(self.nodes)
                if (self.Comps[key].fdotok == True):
                    keys.remove(key)

            i += 1
            if (i > self.DevNum or keys.count == 0):
                self.fdotok = True

    def cycleSimulator(self):

        self.totalworkExtracted = 0
        self.totalworkRequired = 0
        self.totalheatAdded = 0

        for key in self.Comps:
            self.Comps[key].simulate(self.nodes)
            if self.Comps[key].energy == "workExtracted":
                self.totalworkExtracted += self.Comps[key].workExtracted
            elif self.Comps[key].energy == "workRequired":
                self.totalworkRequired += self.Comps[key].workRequired
            elif self.Comps[key].energy == "heatAdded":
                self.totalheatAdded += self. Comps[key].heatAdded

        self.netpoweroutput = self.totalworkExtracted - self.totalworkRequired
        self.efficiency = 100.0 * self.netpoweroutput / self.totalheatAdded
        self.HeatRate = 3600.0 / (self.efficiency * 0.01)
        self.SteamRate = self.HeatRate / self.totalheatAdded

    def SpecifiedNetOutputPowerSimulator(self, Wcycledot):
        self.Wcycledot = Wcycledot
        self.mdot = self.Wcycledot * self.SteamRate * 1000.0

        for i in range(self.NodeNum):
            self.nodes[i].calmdot(self.mdot)

        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0
        for key in self.Comps:
            self.Comps[key].sm_energy(self.nodes)
            if self.Comps[key].energy == "workExtracted":
                self.totalWExtracted += self.Comps[key].WExtracted
            elif self.Comps[key].energy == "workRequired":
                self.totalWRequired += self.Comps[key].WRequired
            elif self.Comps[key].energy == "heatAdded":
                self.totalQAdded += self. Comps[key].QAdded

    def SpecifiedMassFlowSimulator(self, mdot):
        self.mdot = mdot
        self.Wcycledot = self.mdot * self.netpoweroutput / (1000.0 * 3600.0)

        for i in range(self.NodeNum):
            self.nodes[i].calmdot(self.mdot)

        self.totalWExtracted = 0
        self.totalWRequired = 0
        self.totalQAdded = 0
        for key in self.Comps:
            self.Comps[key].sm_energy(self.nodes)
            if self.Comps[key].energy == "workExtracted":
                self.totalWExtracted += self.Comps[key].WExtracted
            elif self.Comps[key].energy == "workRequired":
                self.totalWRequired += self.Comps[key].WRequired
            elif self.Comps[key].energy == "heatAdded":
                self.totalQAdded += self. Comps[key].QAdded

    def OutFiles(self, outfilename=None):
        savedStdout = sys.stdout
        if (outfilename != None):
            datafile = open(outfilename, 'w', encoding='utf-8')
            sys.stdout = datafile

        print("\n Rankine Cycle: {}, Time: {}".format(self.name, str(datetime.datetime.now())))
        print("{:>20} {:>.2f}".format('Net Power(MW)', self.Wcycledot))
        print("{:>20} {:>.2f}".format('Mass Flow(kg/h)', self.mdot))
        print("{:>20} {:>.2f}".format('Efficiency(%)', self.efficiency))
        print("{:>20} {:>.2f}".format('Heat Rate(kJ/kWh)', self.HeatRate))
        print("{:>20} {:>.2f}".format('Steam Rate(kg/kWh)', self.SteamRate))

        print("{:>20} {:>.2f}".format(
            'totalWExtracted(MW)', self.totalWExtracted))
        print("{:>20} {:>.2f}".format(
            'totalWRequired(MW)', self.totalWRequired))
        print("{:>20} {:>.2f} \n".format('totalQAdded(MW)', self.totalQAdded))

        # output nodes
        print(Node.title)
        for node in self.nodes:
            print(node)
        # output devices
        for key in self.Comps:
            print(self.Comps[key].export(self.nodes))

        if (outfilename != None):
            datafile.close()
            sys.stdout = savedStdout


class SimRankineCycle(object):

    def __init__(self, rankinefilename):
        self.jsonfilename = rankinefilename
        self.prefixResultFileName = (rankinefilename[0:-5]).replace("txtcycle","output")  # -5 remove .json

    def CycleSimulator(self):
        self.cycle = RankineCycle()
        self.cycle.addRankine(self.jsonfilename)
        self.cycle.componentState()
        self.cycle.cycleFdot()
        self.cycle.cycleSimulator()

    def SpecifiedNetOutputPowerSimulatorAndOutput(self, Wcycledot):
        """ Specified Net Output Power"""
        self.cycle.SpecifiedNetOutputPowerSimulator(Wcycledot)
        # output
        self.cycle.OutFiles()
        self.cycle.OutFiles(self.prefixResultFileName + '-SP.txt')

    def SpecifiedMassFlowSimulatorAndOutput(self, mdot):
        """ Specified Mass Flow"""
        self.cycle.SpecifiedMassFlowSimulator(mdot)
        # output
        self.cycle.OutFiles()
        self.cycle.OutFiles(self.prefixResultFileName + '-SM.txt')
