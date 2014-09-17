
class NetInfo():

    def __init__(self):
        self.timeA = None
        self.timeB = None
        self.itv = 1
        self.eths = {}

    def ReadStat(self):
        f = open("/proc/net/dev")
        lines = f.readlines()
        f.close()
        eths = {}
        for line in lines[2:]:
            con = line.split() 
            interface = con[0].rstrip(":") 
            if interface == 'lo':
                continue
            intf = dict(
                zip(
                    ['Recv', 'RecvPackets',
                    'RecvErrs', 'RecvDrop', 'RecvFifo',
                    'RecvFrames', 'RecvCompressed', 'RecvMulticast',
                    'Tran', 'TranPackets', 'TranErrs',
                    'TranDrop', 'TranFifo', 'TranFrames',
                    'TranCompressed','TranMulticast']
                    ,[ long(con[1]),long(con[2]),long(con[3]),long(con[4]),long(con[5]),long(con[6]),long(con[7]),
                    long(con[8]),long(con[9]),long(con[10]),long(con[11]),long(con[12]),long(con[13]),long(con[14]),
                    long(con[15]),long(con[16])]
                    )   
                        )
            intf['uptime'] = self.GetUptime()
            eths[interface] = intf
            eth = dict(
                        zip(
                            ['interface','speedRC','packRC','errRC','speedTR','packTR','errTR','Tcp'],
                            [interface,'0','0','0','0','0','0','0']
                            )
                    )
            self.eths[interface] = eth
        return eths

    def GetUptime(self):
        f = open("/proc/uptime",'r')
        uptime = float(f.readline().split()[0])*1000
        f.close()
        return uptime

    def GetStat(self):
        if self.itv:
            self.timeA = self.ReadStat()
        else :
            self.timeB = self.ReadStat()
        self.itv = int(not self.itv)
        if self.timeB and self.timeA:
            self.ComputeStat()
        return self.eths
    def ComputeStat(self):
        for interface in self.timeA:
            etha = self.timeA[interface]
            ethb = self.timeB[interface]
            ticks = etha['uptime'] - ethb['uptime']
            speedRC = "%0.2f"%abs((etha['Recv'] - ethb['Recv'])/ticks*1000)
            packRC = "%0.2f"%abs((etha['RecvPackets'] - ethb['RecvPackets'])/ticks*1000)
            errRC = "%0.2f"%abs((etha['RecvErrs'] - ethb['RecvErrs'])/ticks*1000)
            speedTR = "%0.2f"%abs((etha['Tran'] - ethb['Tran'])/ticks*1000)
            packTR = "%0.2f"%abs((etha['TranPackets'] - ethb['TranPackets'])/ticks*1000)
            errTR = "%0.2f"%abs((etha['TranErrs'] - ethb['TranErrs'])/ticks*1000)
            eth = dict(
                        zip(
                            ['speedRC','packRC','errRC','speedTR','packTR','errTR'],
                            [speedRC,packRC,errRC,speedTR,packTR,errTR]
                            )
                    )
            eth['Tcp'] = self.GetTcpStat()
            self.eths[interface].update(eth)
    
    def GetTcpStat(self):
        f = open('/proc/net/snmp')
        while True:
            line = f.readline()
            if not line:
                break
            con = line.split()
            if con[0] == 'Tcp:' and con[1].isdigit():
                break
        if len(con) > 10:
            return con[9]
        else:
            return 'nodate'


"""

import time
n = NetInfo()
while True:
    print n.GetStat()
    #print n.GetUptime()
    time.sleep(1)

"""
