def GetMemStat():
    mem = {}
    f = open("/proc/meminfo")
    lines = f.readlines()
    f.close()
    for line in lines:
        if len(line) < 2: continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = var
    minfo = {} 
    minfo['memtotal'] = mem['MemTotal'] 
    minfo['memfree'] = mem['MemFree'] 
    minfo['buffers'] = mem['Buffers']
    minfo['cached'] = mem['Cached']
    minfo['swaptotal'] = mem['SwapTotal']
    minfo['swapfree'] = mem['SwapFree']
    
    return minfo
