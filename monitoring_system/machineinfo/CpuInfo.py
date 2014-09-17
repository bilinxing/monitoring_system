class CpuInfo():
    def __init__(self):
        self.dev = {}
        self.itv = 1
        self.devsA = None
        self.devsB = None
    def LoopFlush(self):
        while True:
            self.ComputeStat()
    def ReadDiskStat(self):
        f = open("/proc/stat","r")
        while True:
            line = f.readline()
            con = line.split()
            if con[0] == 'cpu':
                break
        f.close()
        devs = {}
        dev = dict(\
                    zip(['user','nice','system','idle','iowait','irq','softirq']\
                    ,[long(con[1]),long(con[2]),long(con[3]),long(con[4]),long(con[5]),long(con[6]),\
                    long(con[7])])\
                    )
        devs['cpu'] = dev
        self.dev['cpu'] = {'%cpu':'nodate'}
        return devs
    def ComputeStat(self):
        for devName in self.devsA:
            deva = self.devsA[devName]
            devb = self.devsB[devName]
            self.dev[devName] = {}
            cpuTimeA = deva['user'] + deva['system'] + deva['idle'] + deva['nice']\
                        + deva['iowait'] + deva['irq'] + deva['softirq']
            cpuTimeB = devb['user'] + devb['system'] + devb['idle'] + devb['nice']\
                        + devb['iowait'] + devb['irq'] + devb['softirq']
            #cpu = float(deva['user'] - devb['user'] \
            #            + deva['system'] - devb['system'])/float(cpuTimeA-cpuTimeB)
            cpu = 1 - float(deva['idle'] - devb['idle'])/float(cpuTimeA-cpuTimeB)
            #print ' total %d user:%d sys:%d'%(cpuTimeA-cpuTimeB,deva['user']-devb['user'],deva['system'] - devb['system'])
            self.dev[devName]['%cpu'] = "%0.2f"%(abs)(cpu*100)
    def GetStat(self): 
        if self.itv:
            self.devsA = self.ReadDiskStat()
        else:
            self.devsB = self.ReadDiskStat()
        self.itv = int(not self.itv)
        if self.devsB and self.devsA:
            self.ComputeStat()
        return self.dev



"""
import time
d = CpuInfo()
while True:
    print d.GetStat()
    time.sleep(2)
"""
