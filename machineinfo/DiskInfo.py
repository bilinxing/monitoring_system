class DiskInfo():
    def __init__(self):
        self.dev = {}
        self.ReadDiskStat()
        self.itv = 1;
        self.devsA = None
        self.devsB = None
    def LoopFlush(self):
        while True:
            self.ComputeStat()
    def ReadDiskStat(self):
        f = open("/proc/diskstats","r")
        devs = {}
        while True:
            line = f.readline()
            if not line:
                break
            con = line.split()
            if not self.IsDisk(con[2]):
                continue
            if len(con) < 14:
                continue
            dev = dict(\
                    zip(['devName','rdIos', 'rdMerges', 'rdSec', 'rdTicks',\
                    'wrIos', 'wrMerges', 'wrSec', 'wrTicks', 'iosPgr', 'totTicks', 'rqTicks']\
                    ,[con[2],int(con[3]),int(con[4]),int(con[5]),int(con[6]),int(con[7]),\
                    int(con[8]),int(con[9]),int(con[10]),int(con[11]),int(con[12]),int(con[13])])\
                    )
            dev['uptime'] = self.GetUptime()
            devs[con[2]] = dev
            self.dev[con[2]] = {'diskName':con[2],'SpeedRD':'nodate','SpeedWR':'nodate','util':'nodata'}
        f.close()
        return devs
    def IsDisk(self,devname):
        if len(devname) > 3:
            return 0
        hd = devname[:2]
        if hd == 'sd' or hd == 'hd':
            return 1
        return 0
    def GetUptime(self):
        f = open("/proc/uptime",'r')
        uptime = float(f.readline().split()[0])*1000
        f.close()
        return uptime
    def ComputeStat(self):
        for devName in self.devsA:
            deva = self.devsA[devName]
            devb = self.devsB[devName]
            self.dev[devName] = {}
            interval = devb['uptime'] - deva['uptime']
            SpeedRD = (devb['rdSec'] - deva['rdSec'])/(2*interval)*1000
            SpeedWR = (devb['wrSec'] - deva['wrSec'])/(2*interval)*1000
            util = (float)(\
                            #devb['rdTicks'] + devb['wrTicks']\
                            #- deva['rdTicks'] - deva['wrTicks']\
                            #+devb['rqTicks'] - deva['rqTicks']\
                            +devb['totTicks'] - deva['totTicks']\
                            )/interval
            self.dev[devName]['SpeedRD'] = "%0.2f"%abs(SpeedRD)
            self.dev[devName]['SpeedWR'] = "%0.2f"%abs(SpeedWR)
            self.dev[devName]['util'] = "%0.2f"%(abs)(util*100)
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
d = DiskInfo()
while True:
    print d.GetStat()
    time.sleep(2)
"""
