from datetime import datetime 
import glob
import copy
import sys
import os
def read_F2C(filename, RES):
    
    objects = list()
    facility_main = ""
    
    current_satellite = ""
    with open(filename,'r') as infile:        
        lines = [line.rstrip("\r\n") for line in infile]
        #skip the date and civil air header
        for i in range(2,len(lines)):
            line = lines[i]
            line = line.strip("\r\n")
            if len(line)>0:
                if line.startswith("Facility"):
                    p = line.split(", ")
                    objects = p
                    facility_main = objects[0].split("-")[1]
                    if facility_main in RES:
                        print("Facility already exists")
                    RES[facility_main] = dict()
                elif line.startswith(facility_main) and facility_main!="":
                    current_satellite = line.split("-")[-1]
                    RES[facility_main][current_satellite] = list()
                elif line.startswith("    "):
                    p = line.strip(" ").split("  ")
                    p = [u.strip(" ") for u in p if len(u.strip(" "))>0]
                    if p[0] != "Access" and p[0] != "------":
                        #parse times
                        if len(p[1].split(" ")[0])==1:
                            p[1] = "0" + p[1]
                        t1 = datetime.strptime(p[1]+"000", "%d %b %Y %H:%M:%S.%f")
                        if len(p[2].split(" ")[0])==1:
                            p[2] = "0" + p[2]
                        t2 = datetime.strptime(p[2]+"000", "%d %b %Y %H:%M:%S.%f")
                        #print(str(t1))
                        #print(str(t2))
                        t3 = float(p[3])
                        RES[facility_main][current_satellite].append((t1,t2,t3))
    return RES
                        #assert(float(t2-t1) == t3)

def load_F2C_data(pathname):
    F2Cdict = dict()
    files = glob.glob(pathname+"*.txt")
    for file in files:
        read_F2C(file, F2Cdict)
    return F2Cdict

def read_R2C(filename, RES):
    objects = list()
    facility_main = ""
    
    current_satellite = ""
    with open(filename,'r') as infile:        
        lines = [line.rstrip("\r\n") for line in infile]
        #skip the date and civil air header
        for i in range(2,len(lines)):
            line = lines[i]
            line = line.strip("\r\n")
            if len(line)>0:
                if line.startswith("AreaTarget"):
                    p = line.split(", ")
                    objects = p
                    objects[0] = objects[0].split("-")[-1]                                        
                elif line.startswith("Russia-To"):
                    current_satellite = line.split("-")[-1]
                    RES[current_satellite] = list()
                elif line.startswith("    "):
                    p = line.strip(" ").split("  ")
                    p = [u.strip(" ") for u in p if len(u.strip(" "))>0]
                    if p[0] != "Access" and p[0] != "------":
                        #parse times
                        if len(p[1].split(" ")[0])==1:
                            p[1] = "0" + p[1]
                        t1 = datetime.strptime(p[1]+"000", "%d %b %Y %H:%M:%S.%f")
                        if len(p[2].split(" ")[0])==1:
                            p[2] = "0" + p[2]
                        t2 = datetime.strptime(p[2]+"000", "%d %b %Y %H:%M:%S.%f")
                       # print(str(t1))
                       # print(str(t2))
                        t3 = float(p[3])
                        RES[current_satellite].append((t1,t2,t3))
    return RES

def load_R2C_data(pathname):
    R2Cdict = dict()
    files = glob.glob(pathname+"*.txt")
    for file in files:
        read_R2C(file, R2Cdict)
    return R2Cdict


        
class satelite:
   
            
    def __init__(self, ID, Type, RtS, Storage_size, Capture_speed, Transfer_speed, max_time):
        self.id = ID
        self.class_type = Type
        self.AreaAccess = RtS
        self.initial_storage = 0
        self.storage_size = Storage_size
        self.capture_speed = Capture_speed
        self.transfer_speed = Transfer_speed


class observer:
    def __init__(self, ID, F2C):
        self.id = ID
        self.satellite_access = F2C


def proc_R2C(R2C, startdate = datetime(2027,6,1,0,0)):
    R2C_proc = copy.deepcopy(R2C)
    for u in R2C_proc:
        for v in range(len(R2C_proc[u])):
            dt1 = R2C_proc[u][v][0]
            dt2 = R2C_proc[u][v][1] 
            t3 = R2C_proc[u][v][2]
            dt1_new = (dt1 - startdate).total_seconds()
            dt2_new = (dt2 - startdate).total_seconds()
            assert(abs((dt2_new-dt1_new) - R2C_proc[u][v][2]) <= 0.02)
            R2C_proc[u][v] = (dt1_new,dt2_new,t3)
    return R2C_proc

def proc_F2C(F2C):
    F2C_proc = copy.deepcopy(F2C)
    for u in F2C_proc:
        for h in F2C_proc[u]:
            for v in range(len(F2C_proc[u][h])):
                dt1 = F2C_proc[u][h][v][0]
                dt2 = F2C_proc[u][h][v][1] 
                t3 = F2C_proc[u][h][v][2]
                dt1_new = (dt1- datetime(2027,6,1,0,0)).total_seconds()
                dt2_new = (dt2- datetime(2027,6,1,0,0)).total_seconds()
                assert(abs((dt2_new-dt1_new) - t3) <= 0.02)
                F2C_proc[u][h][v] = (dt1_new,dt2_new,t3)
    return F2C_proc

def load_and_convert_to_csv(F2C_path, R2C_path):
    F2C = load_F2C_data(F2C_path)
    R2C_Kinosputnik = dict()
    R2C_Zorky = dict()

    read_R2C(R2C_path + "Russia-To-Satellite-SatPlanes_1_5.txt", R2C_Kinosputnik)
    read_R2C(R2C_path + "Russia-To-Satellite-SatPlanes_6_20.txt", R2C_Zorky)
    R2C_Kinosputnik_pr = proc_R2C(R2C_Kinosputnik)
    R2C_Zorky_pr = proc_R2C(R2C_Zorky)

    F2C_pr = proc_F2C(F2C)

    maxtime = 14*24*60*60

   
    SAT_group = list()
    for u in R2C_Kinosputnik_pr:
        a = satelite(u,"Kinosputnik",R2C_Kinosputnik_pr[u],1000,0.5,0.125,maxtime)
        SAT_group.append(a)

    for u in R2C_Zorky_pr:
        a = satelite(u,"Zorky",R2C_Zorky_pr[u],500,0.5,0.03125,maxtime)
        SAT_group.append(a)
        
    csvdirname = "./Data_csv/"
    csvdirname_satellites = "./Data_csv/satellites/"
    if not os.path.exists(csvdirname_satellites):
        os.makedirs(csvdirname_satellites)


    csvdirname_stations = "./Data_csv/stations/"
    if not os.path.exists(csvdirname_stations):
        os.makedirs(csvdirname_stations)

    for sputnik in SAT_group:
        csvfile = csvdirname_satellites + sputnik.class_type + "_" + sputnik.id + ".csv"
        if not os.path.isfile(csvfile):
            with open(csvfile,'w') as outfile:
                for interval in sputnik.AreaAccess:
                    outfile.write("{},{},{}\n".format(interval[0],interval[1],interval[2]))

    observers_group = list()
    for u in F2C_pr:
        o = observer(u,F2C_pr[u])
        observers_group.append(o)

    for obs in observers_group:
        csvfile = csvdirname_stations+obs.id+".csv"
        if not os.path.isfile(csvfile):
            with open(csvfile,'w') as outfile:
                for sputnik in obs.satellite_access:
                    outfile.write("*"+sputnik+"\n")
                    for interval in obs.satellite_access[sputnik]:  
                        outfile.write("{},{},{}\n".format(interval[0],interval[1],interval[2]))

if len(sys.argv) == 1: 
    print("To generate Data in csv specify path to /DATA_files/ (unzipped)")
    exit(0)
elif sys.argv[1] == "-h" or sys.argv[1] =="-help":
    print("To generate Data in csv specify path to /DATA_files/ (unzipped)")
    exit(0)
else:
    sep = "/"
    if os.name == 'nt' :
        sep = "\\"
    F2C_path = sys.argv[1] + sep+"Facility2Constellation" + sep
    R2C_path = sys.argv[1] + sep+"Russia2Constellation2" + sep
    load_and_convert_to_csv(F2C_path, R2C_path)
 