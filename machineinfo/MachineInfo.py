import NetworkInfo
from MemoryInfo import GetMemStat
import DiskInfo
import CpuInfo


class MachineInfo():
    def __init__(self):
        self.net = NetworkInfo.NetInfo()
        self.disk = DiskInfo.DiskInfo()
        self.cpu = CpuInfo.CpuInfo()

    def GetHostname(self):
        import socket
        try:
            f = open("/etc/salt/minion_id",'r')
            line = f.readline()
        except IOError:
            return socket.gethostname()
        finally:
            f.close()
        line = line.strip()
        if len(line) > 0:
            hostname = line
        else:
            hostname = socket.gethostname()
        return hostname

    def GetStats(self):
        netlist = []
        disklist = []
        cpulist = []
        eths = self.net.GetStat()
        disks = self.disk.GetStat()
        cpus = self.cpu.GetStat()
        memlist = [GetMemStat(),]
        hostname = self.GetHostname()
        if not eths:
            netlist = "nodata"
        if not disks:
            disklist = "nodata"
        if not cpus:
            cpulist = "nodata"
        if not memlist:
            memlist = "nodata"
        for e in eths:
            netlist.append(eths[e])
        for d in disks:
            disklist.append(disks[d])
        for c in cpus:
            cpulist.append(cpus[c])
        return {'cpu':cpulist,'memory':memlist,'disk':disklist,'network':netlist,'hostname':hostname}
    



"""
from time import sleep
info = MachineInfo()
while True:
    print info.GetStats()
    sleep(2)
"""
