import NetworkInfo
from MemoryInfo import GetMemStat
import DiskInfo
import CpuInfo


class MachineInfo():
    def __init__(self):
        self.net = NetworkInfo.NetInfo()
        self.disk = DiskInfo.DiskInfo()
        self.cpu = CpuInfo.CpuInfo()

    def GetStats(self):
        netlist = []
        disklist = []
        cpulist = []
        eths = self.net.GetStat()
        disks = self.disk.GetStat()
        cpus = self.cpu.GetStat()
        for e in eths:
            netlist.append(eths[e])
        for d in disks:
            disklist.append(disks[d])
        for c in cpus:
            cpulist.append(cpus[c])
        memlist = [GetMemStat(),]
        return {'cpu':cpulist,'memory':memlist,'disk':disklist,'network':netlist}
    



"""
from time import sleep
info = MachineInfo()
while True:
    print info.GetStats()
    sleep(2)

"""
