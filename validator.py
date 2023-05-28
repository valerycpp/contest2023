#- Результат работы кода: собственно расписание сеансов сброса для
# каждой наземной станции и каждого спутника на интервале моделирования в
# виде таблиц Время начала-Время конца, с указанием спутника, станции, объема
# переданных в течение сеанса данных, т.е. упорядоченная последовательность
# сеансов сброса (пересекаются по времени с соот. зонами прямой видимости),
# назначенных между спутниками и наземными станциями.
#- Результирующий расчетный объем данных, передаваемый в сутки;
# за весь период моделирования

# Рекомендуемый формат выходных данных
# (на каждую станцию отдельный файл)
# Anadyr1 - имя станции
#-------------------------
#Access *
#Start Time (UTCG)
#* Stop Time (UTCG) *Duration (sec) * Sat
# Jun 2027 00:04:21.296260.296
#name * Data (Mbytes)
#1.
#1 Jun 2027 00:00:01.000
#KinoSat_110101 100
#2.
#…

import glob
import os
import sys
import datetime
import math
import re

stations = ['Anadyr1', 'Anadyr2', 'CapeTown', 'Delhi', 'Irkutsk', \
            'Magadan1', 'Magadan2', 'Moscow', 'Murmansk1', 'Murmansk2', \
            'Norilsk', 'Novosib', 'RioGallegos', 'Sumatra']

satellites = ['KinoSat_110310', 'KinoSat_110409', 'KinoSat_111106', 'KinoSat_111609', 'KinoSat_110607', 'KinoSat_110906', 'KinoSat_112002', 'KinoSat_110501', 'KinoSat_111906', 'KinoSat_110609', 'KinoSat_111006', 'KinoSat_111003', 'KinoSat_110801', 'KinoSat_110109', 'KinoSat_111709', 'KinoSat_110610', 'KinoSat_111801', 'KinoSat_110505', 'KinoSat_110107', 'KinoSat_111407', 'KinoSat_111702', 'KinoSat_111110', 'KinoSat_112008', 'KinoSat_110710', 'KinoSat_111308', 'KinoSat_111509', 'KinoSat_110104', 'KinoSat_110405', 'KinoSat_111203', 'KinoSat_111205', 'KinoSat_111602', 'KinoSat_110807', 'KinoSat_111908', 'KinoSat_110809', 'KinoSat_111502', 'KinoSat_112009', 'KinoSat_112010', 'KinoSat_110201', 'KinoSat_110103', 'KinoSat_111610', 'KinoSat_111010', 'KinoSat_110509', 'KinoSat_110204', 'KinoSat_110302', 'KinoSat_110304', 'KinoSat_112003', 'KinoSat_110203', 'KinoSat_110704', 'KinoSat_110604', 'KinoSat_110101', 'KinoSat_110110', 'KinoSat_111810', 'KinoSat_111907', 'KinoSat_110805', 'KinoSat_110703', 'KinoSat_111306', 'KinoSat_111303', 'KinoSat_111504', 'KinoSat_110605', 'KinoSat_110308', 'KinoSat_111809', 'KinoSat_110410', 'KinoSat_110910', 'KinoSat_111706', 'KinoSat_111901', 'KinoSat_111909', 'KinoSat_111503', 'KinoSat_111109', 'KinoSat_110301', 'KinoSat_111001', 'KinoSat_110908', 'KinoSat_111802', 'KinoSat_111603', 'KinoSat_110808', 'KinoSat_111209', 'KinoSat_111701', 'KinoSat_110510', 'KinoSat_110806', 'KinoSat_111705', 'KinoSat_110902', 'KinoSat_110106', 'KinoSat_110306', 'KinoSat_110901', 'KinoSat_110105', 'KinoSat_111102', 'KinoSat_111107', 'KinoSat_111305', 'KinoSat_111607', 'KinoSat_110401', 'KinoSat_111902', 'KinoSat_110303', 'KinoSat_110502', 'KinoSat_111002', 'KinoSat_111103', 'KinoSat_111207', 'KinoSat_111310', 'KinoSat_111808', 'KinoSat_110402', 'KinoSat_110507', 'KinoSat_110307', 'KinoSat_110403', 'KinoSat_111401', 'KinoSat_110708', 'KinoSat_110407', 'KinoSat_111210', 'KinoSat_111710', 'KinoSat_111309', 'KinoSat_111108', 'KinoSat_111009', 'KinoSat_110602', 'KinoSat_111204', 'KinoSat_110210', 'KinoSat_110503', 'KinoSat_111307', 'KinoSat_111707', 'KinoSat_110404', 'KinoSat_110305', 'KinoSat_111007', 'KinoSat_111505', 'KinoSat_111406', 'KinoSat_110804', 'KinoSat_112007', 'KinoSat_111506', 'KinoSat_112001', 'KinoSat_110207', 'KinoSat_110904', 'KinoSat_111410', 'KinoSat_111402', 'KinoSat_110108', 'KinoSat_110706', 'KinoSat_111301', 'KinoSat_110206', 'KinoSat_110208', 'KinoSat_111101', 'KinoSat_111703', 'KinoSat_110701', 'KinoSat_111904', 'KinoSat_110702', 'KinoSat_110209', 'KinoSat_111408', 'KinoSat_111807', 'KinoSat_112006', 'KinoSat_110506', 'KinoSat_111202', 'KinoSat_111004', 'KinoSat_110408', 'KinoSat_111404', 'KinoSat_111403', 'KinoSat_111601', 'KinoSat_111005', 'KinoSat_110905', 'KinoSat_111304', 'KinoSat_111708', 'KinoSat_110909', 'KinoSat_111409', 'KinoSat_111201', 'KinoSat_111905', 'KinoSat_111508', 'KinoSat_111105', 'KinoSat_111608', 'KinoSat_110907', 'KinoSat_111803', 'KinoSat_111805', 'KinoSat_110601', 'KinoSat_111806', 'KinoSat_111208', 'KinoSat_111903', 'KinoSat_110608', 'KinoSat_110309', 'KinoSat_110406', 'KinoSat_111008', 'KinoSat_111804', 'KinoSat_110709', 'KinoSat_111604', 'KinoSat_110603', 'KinoSat_111501', 'KinoSat_111704', 'KinoSat_112005', 'KinoSat_112004', 'KinoSat_110810', 'KinoSat_111605', 'KinoSat_110202', 'KinoSat_110707', 'KinoSat_110802', 'KinoSat_110504', 'KinoSat_111104', 'KinoSat_111510', 'KinoSat_110102', 'KinoSat_110705', 'KinoSat_111606', 'KinoSat_110803', 'KinoSat_110606', 'KinoSat_111302', 'KinoSat_110903', 'KinoSat_111405', 'KinoSat_111910', 'KinoSat_110508', 'KinoSat_111507', 'KinoSat_111206', 'KinoSat_110205']

FILL_SPEED_MEGABYTES_PER_SEC = 512
TRANSM_SPEED_MEGABYTES_PER_SEC_FAST_SAT = 128
TRANSM_SPEED_MEGABYTES_PER_SEC_SLOW_SAT = 32
SPACE_MEGABYTES_FAST_SAT = 1048576
SPACE_MEGABYTES_SLOW_SAT = 524288

class interval:
   dt1 = datetime.datetime.now()
   dt2 = datetime.datetime.now()
   is_transmit = False
   def __init__(self, dt1, dt2, is_transmit):
     self.dt1 = dt1
     self.dt2 = dt2
     self.is_transmit = is_transmit
   def __str__(self):
     return str(self.dt1) + ' ' + str(self.dt2) + ' ' + str(self.is_transmit)

delimiter = '-------------------------'
header = 'Access * Start Time (UTCG) * Stop Time (UTCG) * Duration (sec) * Sat * Data (Mbytes)'

def fill_res_files():
    for f in stations:
      fname = f + '.res'
      s = 'touch ' + fname
      os.system(s)
      with open(fname, 'w') as ofile:
         ofile.write(f + '\n')
         ofile.write(delimiter + '\n')
         ofile.write(header + '\n')

def datetime_from_str(datetime_str : str):
   # 1 Jun 2027 00:04:21.296
   days = int(datetime_str.split()[0])
   time = datetime_str.split()[3]
   assert(datetime_str.split()[1] == 'Jun')
   assert(datetime_str.split()[2] == '2027')
   hour = int(time.split(':')[0])
   min = int(time.split(':')[1])
   sec_str = time.split(':')[2]
   sec = int(sec_str.split('.')[0])
   millisec_str = sec_str.split('.')[1]
   #print('millisec_str : ' + millisec_str)
   millisec = int(millisec_str)
   microsec = int(millisec * math.pow(10, 6 - len(millisec_str))) # time object takes microseconds
   #print('microsec : ' + str(microsec))
   dt = datetime.datetime(2027,6,days,hour,min,sec,microsec)
   return dt

def check_time(start_datetime_str : str, stop_datetime_str : str, duration_sec : float):
   assert(duration_sec >= 0)
   #print('start_datetime : ' + start_datetime)
   #print('stop_datetime : ' + stop_datetime)
   #print('duration_sec : ' + str(duration_sec))
   start_datetime = datetime_from_str(start_datetime_str)
   stop_datetime = datetime_from_str(stop_datetime_str)
   datetime_delta = stop_datetime - start_datetime
   date_duration_sec = datetime_delta.total_seconds()
   assert(date_duration_sec > 0)
   #print('date_duration_sec : ' + str(date_duration_sec))
   assert(duration_sec == date_duration_sec)
   return start_datetime, stop_datetime

#if len(sys.argv) > 1 and sys.argv[1] == '-fill':
#  fill_res_files()

if len(sys.argv) < 3:
  print('Usage : script data-folder solution-folder')
  exit(1)

data_folder = sys.argv[1]
sol_folder = sys.argv[2]

print('Станции :')
print(stations)

station_sat_possib_intervals = dict()
for stat in stations:
   second_dict = dict()
   station_sat_possib_intervals[stat] = second_dict

# Прочитать допустимые интервалы связи:
#os.chdir("./DATA_Files/Facility2Constellation/")
for f in glob.glob(data_folder + '*.txt'):
   fshort = f.split('/')[-1]
   if 'Facility' not in fshort:
      continue
   #print(f)
   print(fshort)
   stat_name = fshort.split('Facility-')[1].split('.txt')[0]
   if stat_name == 'Cape_Town':
      stat_name = 'CapeTown'
   if stat_name == 'Dehli':
      stat_name = 'Delhi'
   print(stat_name)
   with open(f, 'r') as ifile:
      lines = ifile.read().splitlines()
      #print(lines)
      line_num = 0
      is_start_reading = False
      sat_name = ''
      for line in lines[6:]:
         if line == '':
            is_start_reading = False
            if len(sat_intervals) > 0:
               assert(sat_name != '')
               station_sat_possib_intervals[stat_name][sat_name] = sat_intervals
            continue
         if '-To-' in line:
            sat_name = line.split('-To-')[1]
            sat_intervals = []
            continue
         #print(line)
         words = re.split(r'\s{2,}', line)[1:]
         #print(words)
         if is_start_reading:
            #print(line)
            line_num += 1
            assert(line_num == int(words[0]))
            #print(words)
            intrvl = interval(words[1], words[2], True)
            #print('*')
            sat_intervals.append(intrvl)
            #print(line)
         elif len(words) > 0 and words[0] == '------':
            line_num = 0
            is_start_reading = True

for x in station_sat_possib_intervals['Anadyr1']['KinoSat_110102']:
   print(x)

# Прочитать названия спутников:
#os.chdir("./DATA_Files/Facility2Constellation/")
#satellites = set()
#for f in glob.glob("*.txt"):
#    if 'Facility' in f:
#        with open(f, 'r') as ifile:
#           lines = ifile.read().splitlines()
#           for line in lines:
#              if '-To-' in line and 'Facility-' not in line:
#                 s_name = line.split('-To-')[1]
#                 assert(' ' not in s_name)
#                 satellites.add(s_name)
print(str(len(satellites)) + ' спутников :')
#print(satellites)
satellites_fast = set()
satellites_slow = set()
for sat in satellites:
   num = int(sat.split('_')[1][2:4])
   if num >= 1 and num <= 5:
      satellites_fast.add(sat)
   else:
      satellites_slow.add(sat)

print('Быстрые спутники Kinosat :')
print(satellites_fast)
print('Медленные спутники Zorkiy :')
print(satellites_slow)
assert(len(satellites_fast) == 50)
assert(len(satellites_slow) == 150)

#os.chdir("../../solution/")
res_file_names = []
for f in glob.glob(sol_folder + '*.res'):
    #f = f.split('/')[-1]
    print(f)
    res_file_names.append(f)
    sys_str = 'dos2unix ' + f
    os.system(sys_str)
res_file_names.sort()
print('Файлы с результатами :')
print(res_file_names)

correct_station_files_names = [sol_folder + s + '.res' for s in stations]
correct_station_files_names.sort()

print('Корректные файлы с результатами :')
print(correct_station_files_names)
   
assert(res_file_names == correct_station_files_names)
print('Имена файлов с результатами корректны.')

sat_intervals = dict()
for sat in satellites:
   sat_intervals[sat] = []

total_transmitted_data_mb = 0.0
for res in res_file_names:
   print('***')
   print('Чтение файла ' + res)
   station_name_from_res_file = res.split('.')[0].split('/')[-1]
   assert(station_name_from_res_file != '')
   station_transmitted_data_mb = 0
   line_num = 0
   station_total_work_time = 0
   with open(res, 'r') as ifile:
      lines = ifile.read().splitlines()
      assert(len(lines) >= 3)
      assert(lines[0] == station_name_from_res_file)
      assert(lines[1] == delimiter)
      assert(lines[2] == header)
      for line in lines[3:]:
        #print(line)
        line_num += 1
        words = line.split('\t')
        assert(len(words) == 6)
        assert(int(words[0]) == line_num)
        start_time = words[1]
        stop_time = words[2]
        duration_sec = float(words[3])
        station_total_work_time += duration_sec
        res_dt = check_time(start_time, stop_time, duration_sec)
        sat_name = words[4]
        assert(sat_name in satellites)
        assert(' ' not in words[-1])
        transmitted_data_mb = float(words[-1])
        assert(transmitted_data_mb > 0)
        total_transmitted_data_mb += transmitted_data_mb
        station_transmitted_data_mb += transmitted_data_mb
        max_transmitted_data_mb = -1
        #print('duration_sec : ' + str(duration_sec))
        is_fast = False
        if sat_name in satellites_fast:
          is_fast = True
          max_transmitted_data_mb = duration_sec * TRANSM_SPEED_MEGABYTES_PER_SEC_FAST_SAT
        else:
          assert(sat_name in satellites_slow)
          max_transmitted_data_mb = duration_sec * TRANSM_SPEED_MEGABYTES_PER_SEC_SLOW_SAT
        #print('max_transmitted_data_mb : ' + str(max_transmitted_data_mb))
        assert(max_transmitted_data_mb > 0)
        assert(transmitted_data_mb <= max_transmitted_data_mb)
        intrvl = interval(res_dt[0], res_dt[1], True)
        sat_intervals[sat_name].append(intrvl)
        is_possible_interval = False
        #print('sat_name : ' + sat_name)
        #print('intrvl.dt1 : ' + str(intrvl.dt1))
        #print('intrvl.dt2 : ' + str(intrvl.dt2))
        for pos_interv in station_sat_possib_intervals[station_name_from_res_file][sat_name]:
           if intrvl.dt1 >= datetime_from_str(pos_interv.dt1) and intrvl.dt2 <= datetime_from_str(pos_interv.dt2):
             is_possible_interval = True
             #print('pos_interv.dt1 : ' + str(pos_interv.dt1))
             #print('pos_interv.dt2 : ' + str(pos_interv.dt2))
        if not is_possible_interval:
          print('sat_name : ' + sat_name)
          print(line)
          print('intrvl.dt1 : ' + str(intrvl.dt1))
          print('intrvl.dt2 : ' + str(intrvl.dt2))
        #if station_name_from_res_file == 'CapeTown':
        #  continue
        assert(is_possible_interval)
   print('Сеансов связи : ' + str(line_num))
   print('Передано Mb на станцию : ' + str(station_transmitted_data_mb))
   print('Передано Gb на станцию : ' + str(station_transmitted_data_mb / 1000))
   print('Станция простаивала в секундах :' + str(1123200 - station_total_work_time))

for sat_name in satellites:
   sat_intervals[sat_name].sort(key=lambda x: x.dt1, reverse=False)

# Интервалы моделирования:
total_dt_start = datetime.datetime(2027, 6, 1, 0, 0, 1, 0)
total_dt_stop = datetime.datetime(2027, 6, 14, 0, 0, 1, 0)

# Добавить начальный и конечный интервал съемки видео если нужно:
for sat_name in sat_intervals:
   if len(sat_intervals[sat_name]) == 0:
      continue
   new_intervals = []
   first_intrvl = sat_intervals[sat_name][0]
   last_intrvl = sat_intervals[sat_name][len(sat_intervals[sat_name]) - 1]
   if first_intrvl.dt1 > total_dt_start:
      intrvl = interval(total_dt_start, first_intrvl.dt1, False)
      new_intervals = [intrvl]
   for s_i in sat_intervals[sat_name]:
      new_intervals.append(s_i)
   if last_intrvl.dt2 < total_dt_stop:
      intrvl = interval(last_intrvl.dt2, total_dt_stop, False)
      new_intervals.append(intrvl)
   #sat_intervals[sat_name] = new_intervals

# Добавить интервалы съемки видео там, где интервалов нет:
for sat_name in sat_intervals:
   if len(sat_intervals[sat_name]) == 0:
      continue
   new_intervals = []
   # Для каждой пары интервалов:
   for i in range(len(sat_intervals[sat_name]) - 1):
      intrvl1 = sat_intervals[sat_name][i]
      intrvl2 = sat_intervals[sat_name][i+1]
      assert(intrvl1.dt1 < intrvl1.dt2)
      assert(intrvl2.dt1 < intrvl2.dt2)
      assert(intrvl1.dt2 <= intrvl2.dt1)
      new_intervals.append(intrvl1)
      if intrvl2.dt1 != intrvl1.dt2:
         new_intrvl = interval(intrvl1.dt2, intrvl2.dt1, False)
         new_intervals.append(new_intrvl)
   new_intervals.append(sat_intervals[sat_name][-1])
   #sat_intervals[sat_name] = new_intervals
   #for s_i in sat_intervals[sat_name]:
   #   print(s_i)

print('Всего передано данных на все станции : ' + str(total_transmitted_data_mb) + ' Mb')
total_transmitted_data_gb = total_transmitted_data_mb / 1000
print('Всего передано данных на все станции : ' + str(total_transmitted_data_gb) + ' Gb')
