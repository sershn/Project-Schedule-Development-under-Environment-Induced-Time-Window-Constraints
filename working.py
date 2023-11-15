import datetime
import gantt
import math
import random
import pandas as pd
import numpy as np
import pyprind
number_of_runs = 9
pd.set_option('display.max_columns', None)
# Formatting
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")

gantt.define_not_worked_days([])  # list_of_days -- list of integer (0: Monday ... 6: Sunday) - default [5, 6]
# CREWS
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Berm and abutment base'''
# Excavate (p. 603, added 15% to cost for loading onto trucks)
# [output/hr BCY, cost $/hr, workers, equipment weight lb, excavator capacity, CAT model]
B12B = [125, 316, 2, 49600, '1.5 CY', '320 4F excavator']  # line 31 23 16.42 0250
B12C = [165, 339, 2, 67900, '2 CY', '330 GC excavator']  # line 31 23 16.42 0260
B12D = [260, 539, 2, 83100, '3.5 CY', '340 excavator']  # line 31 23 16.42 0300
# Haul
# [output/hr LCY (calculated), cost $/hr, workers, total equipment weight lb, truck heaped capacity, CAT model]
B34E = [32.7, 238, 1, 50975, '19.6 CY', '725 truck']
B34F = [43.8, 259, 1, 70548, '26.2 CY', '735 truck']
B34G = [68.1, 303, 1, 76529, '40.8 CY', '772G truck']
# Spread
# [output/hr BCY, cost $/hr, workers, total equipment weight lb, dozer power, CAT model]
B10W = [87.5, 184, 1.5, 20640, '104 HP', 'D3 dozer']
B10B = [237.5, 285, 1.5, 50733, '215 HP', 'D6 dozer']
B10X = [241.3, 434, 1.5, 110225, '452 HP', 'D9 dozer']
# Define alternative methods for a1_build_berm
a1_alternative_0 = [B12B, B34E, B10W]
a1_alternative_1 = [B12C, B34F, B10B]
a1_alternative_2 = [B12D, B34G, B10X]
a1_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
a9_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
a10_alternatives = [a1_alternative_0, a1_alternative_1, a1_alternative_2]
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Abutment base (berm crews plus compaction crew)'''
# Compact
# [output/hr CCY, cost $/hr, workers, total equipment weight lb]
B10G = [162.5, 269.9, 1.5, 49652, '815 sheep-foot roller'] # line 32 23 23.24 0300 (p. 619)
# Define alternative methods for a4_abutment_base
a4_alternative_0 = [B12B, B34E, B10W, B10G]
a4_alternative_1 = [B12C, B34F, B10B, B10G]
a4_alternative_2 = [B12D, B34G, B10X, B10G]
a4_alternatives = [a4_alternative_0, a4_alternative_1, a4_alternative_2]
a7_alternatives = [a4_alternative_0, a4_alternative_1, a4_alternative_2]
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Piles'''
# Driven prestressed, precast concrete piles 50' long, 12" diameter, 2-3/8" wall
# [output/hr VLF, cost $/hr, workers, total equipment weight: 1 crawler crane 40 ton, 1 lead 90' high, 1 diesel hammer 22k ft-lb]
B19_CONCRETE = [90, 827, 8, 96000+8055, 'SCC400TB 40 Ton crane, I-12V2 diesel hummer with lead'] # line 31 62 13.23 2200 (p.624)
#  Fixed end caisson piles 50' long, 18" diameter
#  Open style; machine drilled in wet ground; productivity includes excavation, concrete, 50 lb/CY reinforcing;
#  not includes boulder removal
# [output/hr VLF, cost $/hr, workers, equipment: 6" water pump, 1 truck-mounted drill rig, 1 suction and 1 discharge hoses]
B48_CAST_IN = [20, 843, 7, 44000, 'CAT-50 drill'] # line 31 63 26.13 1300 (p. 626)
# Off-road, mobile self-loading concrete mixer
# [output/hr CY of ready mix concrete (5 per truck), cost $/hr, operators, CARMIX 3500 truck weight]
CARMIX_3500 = [10, 400, 2, 2*16300, 'CARMIX 3500 self-loading concrete truck']
# Steel driven piles "H" section 50' long, HP 12x53 (53 lb/ft, width = 12", depth = 11.8")
# [output/hr VLF, cost $/hr, workers, equipment: 1 crawler crane 40 ton, 1 lead 90' high, 1 diesel hammer 22k ft-lb]
B19_STEEL = [74, 827, 8, 96000+8055, 'SCC400TB 40 Ton crane, I-12V2 diesel hummer with lead']
# Define alternative methods for a2_install_piles
a2_alternative_0 = [B19_CONCRETE]
a2_alternative_1 = [B48_CAST_IN, CARMIX_3500]
a2_alternative_2 = [B19_STEEL]
a2_alternatives = [a2_alternative_0, a2_alternative_1, a2_alternative_2]
a11_alternatives = [a2_alternative_0, a2_alternative_1, a2_alternative_2]
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Cast-in-place pier and abutment'''
# Pile cap and pier wall
# [output/hr CY, cost $/hr, workers, total pump weight lb, pump output 45 CY/hr]
C14A = [2.91, 1287, 25, 7300, 'Schwing SP 500 concrete pump']
# [output/hr SFCA, cost $/hr, workers, wall, job-built plywood, over 16 feet high, 2 use]
C2 = [36.25, 413, 6, 0] # line 03 11 13.85 2750 (p. 57)
# [output/hr Ton, cost $/hr, workers, columns reiforc. #8 to #18, potentially add unloading crew C5]
C4A = [0.15, 165, 2, 0]  # line 03 21 11.60 2750 (p. 71)
k = 8 # number of C4A crews
C4A_adjusted = list(np.array(C4A) * k)
# [output/hr CY, cost $/hr, workers, total pump weight lb, place concrete with pump, output 45 CY/hr]
C20 = [110, 588, 8, 7300, 'Schwing SP 500 concrete pump']  # line 03 31 13.70 5100 (p. 79)
# [output/hr CY, cost $/hr, workers, total crane weight lb, place concrete with crane]
C7 = [90, 716, 9, 77000, 'Challenger 3160 55 Ton crane']  # line 03 31 13.70 5200 (p. 79)
# Define alternative methods for a3_cast_in_place_piers
a3_alternative_0 = [C14A, CARMIX_3500]
a3_alternative_1 = [C2, C4A_adjusted, C20, CARMIX_3500]
a3_alternative_2 = [C2, C4A_adjusted, C7, CARMIX_3500]
a3_alternatives = [a3_alternative_0, a3_alternative_1, a3_alternative_2]
# Define alternative methods for a5_cast_in_place_abutment
a5_alternative_0 = [C14A, CARMIX_3500]
a5_alternative_1 = [C2, C4A_adjusted, C20, CARMIX_3500]
a5_alternative_2 = [C2, C4A_adjusted, C7, CARMIX_3500]
a5_alternatives = [a5_alternative_0, a5_alternative_1, a5_alternative_2]
a8_alternatives = [a5_alternative_0, a5_alternative_1, a5_alternative_2]
a12_alternatives = [a5_alternative_0, a5_alternative_1, a5_alternative_2]
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Girder installation'''
# Crane method
# [output/hr Ton, cost $/hr, workers, total crane weight lb]
E5 = [1.61, 1101, 10, 115919, 'TEREX RT 100 90 ton crane']
# Incremental Launching method
# [output/hr Ton, cost $/hr, workers, total crane and lunging equipment weight lb] output calculated as 450m bridge/2 =
# = 225/(25m lunging per week cycle) x 1.152 ton/m weight of girders
E6 = [2.06, 1653 + 125, 16, 30000 + 115919, 'TEREX RT 100 90 ton crane'] # added $1000 per day for lunging equipment rental cost, and 30k of weight to account for lunging equipment
# Define alternative methods for a6_install_girders
a6_alternative_0 = [E5]
a6_alternative_1 = [E6]
a6_alternatives = [a6_alternative_0, a6_alternative_1]
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# NOTES
# Cost of moving equipment from Hay River to Tulita by Winter road (max speed - 50km/hr, distance 900 km, total of 4.5 days there and back assuming 8 hr/day travel time)
mobilize_duration = 4.5
B34N_cost = 1084.52 # $/hr
B34K_cost = 1516.82 # $/hr
# Ticket from Hay River to Tulita one way - $1255 (Hay River - Yellowknife - Tulita)
air_ticket_cost = 1255
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# EMPTY LISTS FOR DATA MANAGEMENT
a1_alternative_list, a1_duration_list, a1_cost_list, a1_crews_list, a1_prod_list = [], [], [], [], []
a2_alternative_list, a2_duration_list, a2_cost_list, a2_crews_list, a2_prod_list = [], [], [], [], []
a3_alternative_list, a3_duration_list, a3_cost_list, a3_crews_list, a3_prod_list = [], [], [], [], []
a4_alternative_list, a4_duration_list, a4_cost_list, a4_crews_list, a4_prod_list = [], [], [], [], []
a5_alternative_list, a5_duration_list, a5_cost_list, a5_crews_list, a5_prod_list = [], [], [], [], []
a6_alternative_list, a6_duration_list, a6_cost_list, a6_crews_list, a6_prod_list = [], [], [], [], []
a7_alternative_list, a7_duration_list, a7_cost_list, a7_crews_list, a7_prod_list = [], [], [], [], []
a8_alternative_list, a8_duration_list, a8_cost_list, a8_crews_list, a8_prod_list = [], [], [], [], []
a9_alternative_list, a9_duration_list, a9_cost_list, a9_crews_list, a9_prod_list = [], [], [], [], []
a10_alternative_list, a10_duration_list, a10_cost_list, a10_crews_list, a10_prod_list = [], [], [], [], []
a11_alternative_list, a11_duration_list, a11_cost_list, a11_crews_list, a11_prod_list = [], [], [], [], []
a12_alternative_list, a12_duration_list, a12_cost_list, a12_crews_list, a12_prod_list = [], [], [], [], []
a13_alternative_list, a13_duration_list, a13_cost_list, a13_crews_list, a13_prod_list = [], [], [], [], []
a14_alternative_list, a14_duration_list, a14_cost_list, a14_crews_list, a14_prod_list = [], [], [], [], []
a15_alternative_list, a15_duration_list, a15_cost_list, a15_crews_list, a15_prod_list = [], [], [], [], []
work_duration_list = []
idle_time_list = []
temp_cost_list = []
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# SIMULATION PROGRESS FEATURE
run = 0
bar = pyprind.ProgBar(number_of_runs, monitor=True, bar_char='■')
print('Running', format(number_of_runs,',d'), 'iterations')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# SIMULATION
while run != number_of_runs:
    bar.update() # progress update
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW WINTER ROAD 2022-2023
    tw0_start_rand = random.randint(20, 20)
    tw0_stop_rand = random.randint(1, 1)
    # tw0_start_rand = random.randint(10, 30)
    # tw0_stop_rand = random.randint(1, 20)
    tw0_start = datetime.date(2022, 12, tw0_start_rand)
    tw0_stop = datetime.date(2023, 4, tw0_stop_rand)
    tw0_duration = tw0_stop - tw0_start
    tw0 = gantt.Task(name='tw0_winter_road',
                     start=tw0_start,
                     stop=tw0_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW TEMPERATURE ABOVE ZERO 2023
    tw1_start_rand = random.randint(1, 1)
    tw1_stop_rand = random.randint(15, 15)
    # tw1_start_rand = random.randint(5, 25)
    # tw1_stop_rand = random.randint(1, 20)
    tw1_start = datetime.date(2023, 5, tw1_start_rand)
    tw1_stop = datetime.date(2023, 10, tw1_stop_rand)
    tw1_duration = tw1_stop - tw1_start
    tw1 = gantt.Task(name='tw1_temperature_>0C°',
                     start=tw1_start,
                     stop=tw1_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW IN-RIVER ACTIVITY 2023
    tw2_start_rand = random.randint(16, 16)
    tw2_stop_rand = random.randint(14, 14)
    # tw2_start_rand = random.randint(5, 25)
    # tw2_stop_rand = random.randint(1, 20)
    tw2_start = datetime.date(2023, 7, tw2_start_rand)
    tw2_stop = datetime.date(2023, 9, tw2_stop_rand)
    tw2_duration = tw2_stop - tw2_start
    tw2 = gantt.Task(name='tw2_in_river_activity',
                     start=tw2_start,
                     stop=tw2_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW WINTER ROAD 2023-2024
    tw3_start_rand = random.randint(20, 20)
    tw3_stop_rand = random.randint(1, 1)
    # tw3_start_rand = random.randint(10, 30)
    # tw3_stop_rand = random.randint(1, 20)
    tw3_start = datetime.date(2023, 12, tw3_start_rand)
    tw3_stop = datetime.date(2024, 4, tw3_stop_rand)
    tw3_duration = tw3_stop - tw3_start
    tw3 = gantt.Task(name='tw3_winter_road',
                     start=tw3_start,
                     stop=tw3_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW TEMPERATURE ABOVE ZERO 2024
    tw4_start_rand = random.randint(1, 1)
    tw4_stop_rand = random.randint(15, 15)
    # tw4_start_rand = random.randint(5, 25)
    # tw4_stop_rand = random.randint(1, 20)
    tw4_start = datetime.date(2024, 5, tw4_start_rand)
    tw4_stop = datetime.date(2024, 10, tw4_stop_rand)
    tw4_duration = tw4_stop - tw4_start
    tw4 = gantt.Task(name='tw4_temperature_>0C°',
                     start=tw4_start,
                     stop=tw4_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW IN-RIVER ACTIVITY 2024
    tw5_start_rand = random.randint(16, 16)
    tw5_stop_rand = random.randint(14, 14)
    # tw5_start_rand = random.randint(5, 25)
    # tw5_stop_rand = random.randint(1, 20)
    tw5_start = datetime.date(2024, 7, tw5_start_rand)
    tw5_stop = datetime.date(2024, 9, tw5_stop_rand)
    tw5_duration = tw5_stop - tw5_start
    tw5 = gantt.Task(name='tw5_in_river_activity',
                     start=tw5_start,
                     stop=tw5_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # MOBILIZE JOB SITE
    a0_start = tw0_start
    a0_stop = None
    a0_duration = random.randint(30,30)#tw0_2023_duration.days/2
    a0 = gantt.Task(name='a0_mobilize_job_site',
                    start=a0_start,
                    stop=a0_stop,
                    duration=a0_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # BUILD BERM 1
    a1_x = random.randint(0,len(a1_alternatives)-1)
    a1_working_hours = 8
    a1_quantity = 88752  # BCY
    a1_allowable_duration = tw0_duration.days - a0_duration
    a1_productivity = min(a1_alternatives[a1_x][0][0], a1_alternatives[a1_x][2][0])
    a1_truck_crews = math.ceil(a1_productivity / (a1_alternatives[a1_x][1][0] / 1.25)) # 1.25 - bank to loose conversion factor
    a1_hourly_cost = (a1_alternatives[a1_x][0][1] + a1_truck_crews * a1_alternatives[a1_x][1][1] + a1_alternatives[a1_x][2][1])
    a1_initial_duration = a1_quantity / a1_productivity / a1_working_hours
    if a1_initial_duration < a1_allowable_duration:
        a1_crews = 1
        a1_duration = math.ceil(a1_initial_duration)
    else:
        a1_crews = math.ceil(a1_initial_duration/a1_allowable_duration)
        a1_duration = math.ceil(a1_quantity / a1_productivity / a1_working_hours / a1_crews)
    a1_ppl = math.ceil(a1_alternatives[a1_x][0][2] + a1_alternatives[a1_x][1][2] * a1_truck_crews + a1_alternatives[a1_x][2][2]) * a1_crews
    a1_ticket_cost = a1_ppl * air_ticket_cost * 2
    a1_equip_weight = math.ceil(a1_alternatives[a1_x][0][3] + a1_alternatives[a1_x][1][3] * a1_truck_crews + a1_alternatives[a1_x][2][3]) * a1_crews
    if a1_equip_weight <= 80000: a1_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a1_equip_weight <= 150000: a1_weight_cost = mobilize_duration * B34K_cost
    else: a1_weight_cost = mobilize_duration * B34K_cost * math.ceil(a1_equip_weight/150000)
    a1_cost = a1_crews * a1_duration * a1_working_hours * a1_hourly_cost + a1_ticket_cost + a1_weight_cost
    a1_start = a0_start + datetime.timedelta(a0_duration)
    a1_stop = None
    a1 = gantt.Task(name='a1_build_berm_depends_of_[a0]',
                    start=a1_start,
                    stop=a1_stop,
                    duration=a1_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a0)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # INSTALL PILES 1
    a2_x = random.randint(0, len(a2_alternatives) - 1)
    a2_working_hours = 8
    a2_quantity = 6200  # VLF (64 piles x 50')
    a2_allowable_duration = (tw1_start - tw0_stop).days
    a2_productivity = a2_alternatives[a2_x][0][0]
    a2_hourly_cost = 0
    for i in range(len(a2_alternatives[a2_x])):
        a2_hourly_cost += a2_alternatives[a2_x][i][1]
    a2_initial_duration = a2_quantity / a2_productivity / a2_working_hours
    if a2_initial_duration < a2_allowable_duration:
        a2_crews = 1
        a2_duration = math.ceil(a2_initial_duration)
    else:
        a2_crews = math.ceil(a2_initial_duration / a2_allowable_duration)
        a2_duration = math.ceil(a2_quantity / a2_productivity / a2_working_hours / a2_crews)
    a2_ppl = 0
    for n in range(len(a2_alternatives[a2_x])):
        a2_ppl += a2_crews * math.ceil(a2_alternatives[a2_x][n][2])
    a2_ticket_cost = a2_ppl * air_ticket_cost * 2
    a2_equip_weight = 0
    for m in range(len(a2_alternatives[a2_x])):
        a2_equip_weight += a2_crews * a2_alternatives[a2_x][m][3]
    if a2_equip_weight <= 80000: a2_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a2_equip_weight <= 150000: a2_weight_cost = mobilize_duration * B34K_cost
    else: a2_weight_cost = mobilize_duration * B34K_cost * math.ceil(a2_equip_weight/150000)
    a2_cost = a2_crews * a2_duration * a2_working_hours * a2_hourly_cost + a2_ticket_cost + a2_weight_cost
    a2_start = tw0_stop
    a2_stop = None
    a2 = gantt.Task(name='a2_install_piles_depends_of_[a1]',
                    start=a2_start,
                    stop=a2_stop,
                    duration=a2_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # CAST-IN-PLACE PIERS 1
    a3_x = random.randint(0, len(a3_alternatives) - 1)
    a6_x = random.randint(0, len(a6_alternatives) - 1) # Need to know this to define activity sequence.
    a3_working_hours = 8
    a3_quantity = 2*1674.18  # CY
    a3_quantity_SFCA = 2*10979.19 # SFCA
    a3_quantity_Ton = 2*219.8 # Ton
    if a6_x == 0: a3_allowable_duration = tw1_duration.days
    else: a3_allowable_duration = (tw2_start - tw1_start).days
    # Productivity
    if len(a3_alternatives[a3_x]) == 2: a3_productivity = a3_alternatives[a3_x][0][0]
    else: a3_productivity = a3_quantity/((a3_quantity_SFCA/a3_alternatives[a3_x][0][0] + a3_quantity_Ton/a3_alternatives[a3_x][1][0] + a3_quantity/a3_alternatives[a3_x][2][0])/a3_working_hours)/a3_working_hours
    a3_hourly_cost = 0
    for i in range(len(a3_alternatives[a3_x])):
        a3_hourly_cost += a3_alternatives[a3_x][i][1]
    a3_initial_duration = a3_quantity / a3_productivity / a3_working_hours
    if a3_initial_duration < a3_allowable_duration:
        a3_crews = 1
        a3_duration = math.ceil(a3_initial_duration)
    else:
        a3_crews = math.ceil(a3_initial_duration / a3_allowable_duration)
        a3_duration = math.ceil(a3_quantity / a3_productivity / a3_working_hours / a3_crews)
    a3_ppl = 0
    for n in range(len(a3_alternatives[a3_x])):
        a3_ppl += a3_crews * math.ceil(a3_alternatives[a3_x][n][2])
    a3_ticket_cost = a3_ppl * air_ticket_cost * 2
    a3_equip_weight = 0
    for m in range(len(a3_alternatives[a3_x])):
        a3_equip_weight += a3_crews * a3_alternatives[a3_x][m][3]
    if a3_equip_weight <= 80000: a3_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a3_equip_weight <= 150000: a3_weight_cost = mobilize_duration * B34K_cost
    else: a3_weight_cost = mobilize_duration * B34K_cost * math.ceil(a3_equip_weight/150000)
    a3_cost = a3_crews * a3_duration * a3_working_hours * a3_hourly_cost + a3_ticket_cost + a3_weight_cost
    a3_start = tw1_start
    a3_stop = None
    a3 = gantt.Task(name='a3_cast-in-place_piers_depends_of_[a2]',
                    start=a3_start,
                    stop=a3_stop,
                    duration=a3_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a2)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ABUTMENT BASE 1
    a4_x = random.randint(0, len(a4_alternatives) - 1)
    a4_working_hours = 8
    a4_quantity = 20631  # BCY
    a4_allowable_duration = tw1_duration.days/2
    a4_productivity = min(a4_alternatives[a4_x][0][0], a4_alternatives[a4_x][2][0])
    a4_truck_crews = math.ceil(a4_productivity / (a4_alternatives[a4_x][1][0] / 1.25))
    a4_roller_crews = math.ceil(a4_productivity / (a4_alternatives[a4_x][3][0] / 0.9))
    a4_hourly_cost = ((a4_alternatives[a4_x][0][1] + a4_truck_crews * a4_alternatives[a4_x][1][1] + a4_alternatives[a4_x][2][1]) +
                      a4_roller_crews * a4_alternatives[a4_x][3][1]) # 0.9 - compacted to bank conversion factor; 1.25 -  bank to loose conversion factor
    a4_initial_duration = a4_quantity / a4_productivity / a4_working_hours
    if a4_initial_duration < a4_allowable_duration:
        a4_crews = 1
        a4_duration = math.ceil(a4_initial_duration)
    else:
        a4_crews = math.ceil(a4_initial_duration / a4_allowable_duration)
        a4_duration = math.ceil(a4_quantity / a4_productivity / a4_working_hours / a4_crews)
    a4_ppl = math.ceil(a4_alternatives[a4_x][0][2]+a4_alternatives[a4_x][1][2]*a4_truck_crews + a4_alternatives[a4_x][2][2] + a4_alternatives[a4_x][3][2]*a4_roller_crews) * a4_crews
    a4_ticket_cost = a4_ppl * air_ticket_cost * 2
    a4_equip_weight = math.ceil(a4_alternatives[a4_x][0][3]+a4_alternatives[a4_x][1][3]*a4_truck_crews + a4_alternatives[a4_x][2][3] + a4_alternatives[a4_x][3][3]*a4_roller_crews) * a4_crews
    if a4_equip_weight <= 80000: a4_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a4_equip_weight <= 150000: a4_weight_cost = mobilize_duration * B34K_cost
    else: a4_weight_cost = mobilize_duration * B34K_cost * math.ceil(a4_equip_weight / 150000)
    a4_cost = a1_crews * a4_duration * a4_working_hours * a4_hourly_cost + a4_ticket_cost + a4_weight_cost
    a4_start = tw1_start
    a4_stop = a4_start + datetime.timedelta(a4_duration)
    a4 = gantt.Task(name='a4_abutment_base_depends_of_[a1]',
                    start=a4_start,
                    stop=None,
                    duration=a4_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # CAST-IN-PLACE ABUTMENT 1
    a5_x = random.randint(0, len(a5_alternatives) - 1)
    a5_working_hours = 8
    a5_quantity = 978.21  # CY
    a5_quantity_SFCA = 3790.17  # SFCA
    a5_quantity_Ton = 75  # Ton
    a5_allowable_duration = (tw2_start - a4_stop).days
    # Productivity
    if len(a5_alternatives[a5_x]) == 2: a5_productivity = a5_alternatives[a5_x][0][0]
    else: a5_productivity = a5_quantity / ((a5_quantity_SFCA / a5_alternatives[a5_x][0][0] + a5_quantity_Ton / a5_alternatives[a5_x][1][0] +
                                            a5_quantity / a5_alternatives[a5_x][2][0]) / a5_working_hours) / a5_working_hours
    a5_hourly_cost = 0
    for i in range(len(a5_alternatives[a5_x])):
        a5_hourly_cost += a5_alternatives[a5_x][i][1]
    a5_initial_duration = a5_quantity / a5_productivity / a5_working_hours
    if a5_initial_duration < a5_allowable_duration:
        a5_crews = 1
        a5_duration = math.ceil(a5_initial_duration)
    else:
        a5_crews = math.ceil(a5_initial_duration / a5_allowable_duration)
        a5_duration = math.ceil(a5_quantity / a5_productivity / a5_working_hours / a5_crews)
    a5_ppl = 0
    for n in range(len(a5_alternatives[a5_x])):
        a5_ppl += a5_crews * math.ceil(a5_alternatives[a5_x][n][2])
    a5_ticket_cost = a5_ppl * air_ticket_cost * 2
    a5_equip_weight = 0
    for m in range(len(a5_alternatives[a5_x])):
        a5_equip_weight += a5_crews * a5_alternatives[a5_x][m][3]
    if a5_equip_weight <= 80000: a5_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a5_equip_weight <= 150000: a5_weight_cost = mobilize_duration * B34K_cost
    else: a5_weight_cost = mobilize_duration * B34K_cost * math.ceil(a5_equip_weight / 150000)
    a5_cost = a5_crews * a5_duration * a5_working_hours * a5_hourly_cost + a5_ticket_cost + a5_weight_cost
    a5_start = a4_start + datetime.timedelta(a4_duration)
    a5_stop = a5_start + datetime.timedelta(a5_duration)
    a5 = gantt.Task(name='a5_cast-in-place_abutment_depends_of_[a4]',
                    start=a5_start,
                    stop=None,
                    duration=a5_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a4)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # INSTALL GIRDERS
    a6_start = None
    a6_working_hours = 8
    if a6_x == 0:
        a6_quantity = 1296 # Imperial ton (half of the bridge)
        a6_crews = 2 # Need minimum 2 crews to install girders with cranes
    else:
        a6_quantity = 1296 * 2 # Full bridge in case of incremental launching
        a6_crews = 1
    a6_productivity = a6_alternatives[a6_x][0][0]
    a6_hourly_cost = 0
    for i in range(len(a6_alternatives[a6_x])):
        a6_hourly_cost += a6_alternatives[a6_x][i][1]
    a6_duration = a6_quantity / a6_productivity /a6_crews / a6_working_hours
    a6_ppl = 0
    for n in range(len(a6_alternatives[a6_x])):
        a6_ppl += a6_crews * math.ceil(a6_alternatives[a6_x][n][2])
    a6_ticket_cost = a6_ppl * air_ticket_cost * 2
    a6_equip_weight = 0
    for m in range(len(a6_alternatives[a6_x])):
        a6_equip_weight += a6_crews * a6_alternatives[a6_x][m][3]
    if a6_equip_weight <= 80000: a6_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a6_equip_weight <= 150000: a6_weight_cost = mobilize_duration * B34K_cost
    else: a6_weight_cost = mobilize_duration * B34K_cost * math.ceil(a6_equip_weight/150000)
    a6_cost = a6_crews * a6_duration * a6_working_hours * a6_hourly_cost + a6_ticket_cost + a6_weight_cost
    a6_stop = None
    a6 = gantt.Task(name='a6_install_girders_depends_of_[a3, a5]',
                    start=a6_start,
                    stop=None,
                    duration=a6_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=[a3, a5])
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ABUTMENT BASE 2
    a7_x = random.randint(0, len(a7_alternatives) - 1)
    a7_working_hours = 8
    a7_quantity = 20631  # BCY
    a7_allowable_duration = (tw1_stop - a5_stop).days / 2
    a7_productivity = min(a7_alternatives[a7_x][0][0], a7_alternatives[a7_x][2][0])
    a7_truck_crews = math.ceil(a7_productivity / (a7_alternatives[a7_x][1][0] / 1.25))
    a7_roller_crews = math.ceil(a7_productivity / (a7_alternatives[a7_x][3][0] / 0.9))
    a7_hourly_cost = ((a7_alternatives[a7_x][0][1] + a7_truck_crews * a7_alternatives[a7_x][1][1] +
                        a7_alternatives[a7_x][2][1]) +
                       a7_roller_crews * a7_alternatives[a7_x][3][
                           1])  # 0.9 - compacted to bank conversion factor; 1.25 -  bank to loose conversion factor
    a7_initial_duration = a7_quantity / a7_productivity / a7_working_hours
    if a7_initial_duration < a7_allowable_duration:
        a7_crews = 1
        a7_duration = math.ceil(a7_initial_duration)
    else:
        a7_crews = math.ceil(a7_initial_duration / a7_allowable_duration)
        a7_duration = math.ceil(a7_quantity / a7_productivity / a7_working_hours / a7_crews)
    a7_ppl = math.ceil(
        a7_alternatives[a7_x][0][2] + a7_alternatives[a7_x][1][2] * a7_truck_crews + a7_alternatives[a7_x][2][
            2] +
        a7_alternatives[a7_x][3][2] * a7_roller_crews) * a7_crews
    a7_ticket_cost = a7_ppl * air_ticket_cost * 2
    a7_equip_weight = math.ceil(
        a7_alternatives[a7_x][0][3] + a7_alternatives[a7_x][1][3] * a7_truck_crews + a7_alternatives[a7_x][2][
            3] +
        a7_alternatives[a7_x][3][3] * a7_roller_crews) * a7_crews
    if a7_equip_weight <= 80000:
        a7_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a7_equip_weight <= 150000:
        a7_weight_cost = mobilize_duration * B34K_cost
    else:
        a7_weight_cost = mobilize_duration * B34K_cost * math.ceil(a7_equip_weight / 150000)
    a7_cost = a1_crews * a7_duration * a7_working_hours * a7_hourly_cost + a7_ticket_cost + a7_weight_cost
    a7_start = a5_stop
    a7_stop = a7_start + datetime.timedelta(a7_duration)
    a7 = gantt.Task(name='a7_abutment_base_depends_of_[a5]',
                     start=a7_start,
                     stop=None,
                     duration=a7_duration,
                     percent_done=None,
                     resources=None,
                     color="#f4aa80",
                     depends_of=a5)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # CAST-IN-PLACE ABUTMENT 1
    a8_x = random.randint(0, len(a8_alternatives) - 1)
    a8_working_hours = 8
    a8_quantity = 978.21  # CY
    a8_quantity_SFCA = 3790.17  # SFCA
    a8_quantity_Ton = 75  # Ton
    a8_allowable_duration = (tw1_stop - a7_stop).days  # tw1_duration.days - a4_duration
    # Productivity
    if len(a8_alternatives[a8_x]) == 2:
        a8_productivity = a8_alternatives[a8_x][0][0]
    else:
        a8_productivity = a8_quantity / (
                (a8_quantity_SFCA / a8_alternatives[a8_x][0][0] + a8_quantity_Ton / a8_alternatives[a8_x][1][0] +
                 a8_quantity / a8_alternatives[a8_x][2][0]) / a8_working_hours) / a8_working_hours
    a8_hourly_cost = 0
    for i in range(len(a8_alternatives[a8_x])):
        a8_hourly_cost += a8_alternatives[a8_x][i][1]
    a8_initial_duration = a8_quantity / a8_productivity / a8_working_hours
    if a8_initial_duration < a8_allowable_duration:
        a8_crews = 1
        a8_duration = math.ceil(a8_initial_duration)
    else:
        a8_crews = math.ceil(a8_initial_duration / a8_allowable_duration)
        a8_duration = math.ceil(a8_quantity / a8_productivity / a8_working_hours / a8_crews)
    a8_ppl = 0
    for n in range(len(a8_alternatives[a8_x])):
        a8_ppl += a8_crews * math.ceil(a8_alternatives[a8_x][n][2])
    a8_ticket_cost = a8_ppl * air_ticket_cost * 2
    a8_equip_weight = 0
    for m in range(len(a8_alternatives[a8_x])):
        a8_equip_weight += a8_crews * a8_alternatives[a8_x][m][3]
    if a8_equip_weight <= 80000:
        a8_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a8_equip_weight <= 150000:
        a8_weight_cost = mobilize_duration * B34K_cost
    else:
        a8_weight_cost = mobilize_duration * B34K_cost * math.ceil(a8_equip_weight / 150000)
    a8_cost = a8_crews * a8_duration * a8_working_hours * a8_hourly_cost + a8_ticket_cost + a8_weight_cost
    a8_start = a7_stop
    a8_stop = a8_start + datetime.timedelta(a8_duration)
    a8 = gantt.Task(name='a8_cast-in-place_abutment_depends_of_[a7]',
                     start=a8_start,
                     stop=None,
                     duration=a8_duration,
                     percent_done=None,
                     resources=None,
                     color="#f4aa80",
                     depends_of=a7)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # REMOVE BERM 1
    a9_x = random.randint(0, len(a9_alternatives) - 1)
    a9_working_hours = 8
    a9_quantity = 88752  # BCY
    if a6_x == 1:  # In case of incremental launching
        a9_dependence = a3
        a9_name = 'a9_remove_berm_depends_of_[a3]'
        a9_allowable_duration = tw2_duration.days/2
        a9_start = tw2_start
    else:
        a9_dependence = a6
        a9_name = 'a9_remove_berm_depends_of_[a6]'
        a9_allowable_duration = tw3_duration.days/2
        a9_start = tw3_start
    a9_productivity = min(a9_alternatives[a9_x][0][0], a9_alternatives[a9_x][2][0])
    a9_truck_crews = math.ceil(a9_productivity / (a9_alternatives[a9_x][1][0] / 1.25)) # 1.25 - bank to loose conversion factor
    a9_hourly_cost = (a9_alternatives[a9_x][0][1] + a9_truck_crews * a9_alternatives[a9_x][1][1] + a9_alternatives[a9_x][2][1])
    a9_initial_duration = a9_quantity / a9_productivity / a9_working_hours
    if a9_initial_duration < a9_allowable_duration:
        a9_crews = 1
        a9_duration = math.ceil(a9_initial_duration)
    else:
        a9_crews = math.ceil(a9_initial_duration / a9_allowable_duration)
        a9_duration = math.ceil(a9_quantity / a9_productivity / a9_working_hours / a9_crews)
    a9_ppl = math.ceil(a9_alternatives[a9_x][0][2] + a9_alternatives[a9_x][1][2] * a9_truck_crews + a9_alternatives[a9_x][2][2]) * a9_crews
    a9_ticket_cost = a9_ppl * air_ticket_cost * 2
    a9_equip_weight = math.ceil(
        a9_alternatives[a9_x][0][3] + a9_alternatives[a9_x][1][3] * a9_truck_crews + a9_alternatives[a9_x][2][3]) * a9_crews
    if a9_equip_weight <= 80000:  # Crew B-34N
        a9_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a9_equip_weight <= 150000:  # Crew B-34K
        a9_weight_cost = mobilize_duration * B34K_cost
    else:
        a9_weight_cost = mobilize_duration * B34K_cost * math.ceil(a9_equip_weight / 150000)
    a9_cost = a9_crews * a9_duration * a9_working_hours * a9_hourly_cost + a9_ticket_cost + a9_weight_cost
    a9_stop = a9_start + datetime.timedelta(a9_duration)
    a9 = gantt.Task(name=a9_name,
                    start=a9_start,
                    stop=None,
                    duration=a9_duration,
                    percent_done=None,
                    resources=None,
                    color="#f4aa80",
                    depends_of=a9_dependence)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # BUILD BERM 2
    a10_x = random.randint(0, len(a10_alternatives) - 1)
    a10_working_hours = 8
    a10_quantity = 88752  # BCY
    if a6_x == 1: a10_allowable_duration = tw2_duration.days - a7_duration # In case of incremental launching
    else: a10_allowable_duration = tw3_duration.days - a7_duration
    a10_productivity = min(a10_alternatives[a10_x][0][0], a10_alternatives[a10_x][2][0])
    a10_truck_crews = math.ceil(a10_productivity / (a10_alternatives[a10_x][1][0] / 1.25))  # 1.25 - bank to loose conversion factor
    a10_hourly_cost = (a10_alternatives[a10_x][0][1] + a10_truck_crews * a10_alternatives[a10_x][1][1] + a10_alternatives[a10_x][2][1])
    a10_initial_duration = a10_quantity / a10_productivity / a10_working_hours
    if a10_initial_duration < a10_allowable_duration:
        a10_crews = 1
        a10_duration = math.ceil(a10_initial_duration)
    else:
        a10_crews = math.ceil(a10_initial_duration / a10_allowable_duration)
        a10_duration = math.ceil(a10_quantity / a10_productivity / a10_working_hours / a10_crews)
    a10_ppl = math.ceil(
        a10_alternatives[a10_x][0][2] + a10_alternatives[a10_x][1][2] * a10_truck_crews + a10_alternatives[a10_x][2][2]) * a10_crews
    a10_ticket_cost = a10_ppl * air_ticket_cost * 2
    a10_equip_weight = math.ceil(a10_alternatives[a10_x][0][3] + a10_alternatives[a10_x][1][3] * a10_truck_crews + a10_alternatives[a10_x][2][3]) * a10_crews
    if a10_equip_weight <= 80000:  # Crew B-34N
        a10_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a10_equip_weight <= 150000:  # Crew B-34K
        a10_weight_cost = mobilize_duration * B34K_cost
    else:
        a10_weight_cost = mobilize_duration * B34K_cost * math.ceil(a10_equip_weight / 150000)
    a10_cost = a10_crews * a10_duration * a10_working_hours * a10_hourly_cost + a10_ticket_cost + a10_weight_cost
    a10_start = a9_stop
    a10_stop = a10_start + datetime.timedelta(a10_duration)
    a10 = gantt.Task(name='a10_build_berm_depends_of_[a9]',
                    start=a10_start,
                    stop=None,
                    duration=a10_duration,
                    percent_done=None,
                    resources=None,
                    color="#f4aa80",
                    depends_of=a9)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # INSTALL PILES 2
    a11_x = random.randint(0, len(a11_alternatives) - 1)
    a11_working_hours = 8
    a11_quantity = 6200  # VLF (64 piles x 50')
    if a6_x == 1: a11_allowable_duration = (tw3_start - a10_stop).days # In case of incremental launching
    else: a11_allowable_duration = (tw4_start - a10_stop).days
    a11_productivity = a11_alternatives[a11_x][0][0]
    a11_hourly_cost = 0
    for i in range(len(a11_alternatives[a11_x])):
        a11_hourly_cost += a11_alternatives[a11_x][i][1]
    a11_initial_duration = a11_quantity / a11_productivity / a11_working_hours
    if a11_initial_duration < a11_allowable_duration:
        a11_crews = 1
        a11_duration = math.ceil(a11_initial_duration)
    else:
        a11_crews = math.ceil(a11_initial_duration / a11_allowable_duration)
        a11_duration = math.ceil(a11_quantity / a11_productivity / a11_working_hours / a11_crews)
    a11_ppl = 0
    for n in range(len(a11_alternatives[a11_x])):
        a11_ppl += a11_crews * math.ceil(a11_alternatives[a11_x][n][2])
    a11_ticket_cost = a11_ppl * air_ticket_cost * 2
    a11_equip_weight = 0
    for m in range(len(a11_alternatives[a11_x])):
        a11_equip_weight += a11_crews * a11_alternatives[a11_x][m][3]
    if a11_equip_weight <= 80000:
        a11_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a11_equip_weight <= 150000:
        a11_weight_cost = mobilize_duration * B34K_cost
    else:
        a11_weight_cost = mobilize_duration * B34K_cost * math.ceil(a11_equip_weight / 150000)
    a11_cost = a11_crews * a11_duration * a11_working_hours * a11_hourly_cost + a11_ticket_cost + a11_weight_cost
    a11_start = a10_stop
    a11_stop = a11_start + datetime.timedelta(a11_duration)
    a11 = gantt.Task(name='a11_install_piles_depends_of_[a10]',
                    start=a11_start,
                    stop=None,
                    duration=a11_duration,
                    percent_done=None,
                    resources=None,
                    color="#f4aa80",
                    depends_of=a10)
    # CAST-IN-PLACE PIERS 1
    a12_x = random.randint(0, len(a12_alternatives) - 1)
    a12_working_hours = 8
    a12_quantity = 2 * 1674.18  # CY
    a12_quantity_SFCA = 2 * 10979.19  # SFCA
    a12_quantity_Ton = 2 * 219.8  # Ton
    if a6_x == 0:
        a12_allowable_duration = (tw5_start - tw4_start).days
        a12_start = tw4_start
    else:
        a12_allowable_duration = (tw3_start - a11_stop).days
        a12_start = None
    # Productivity
    if len(a12_alternatives[a12_x]) == 2:
        a12_productivity = a12_alternatives[a12_x][0][0]
    else:
        a12_productivity = a12_quantity / ((a12_quantity_SFCA / a12_alternatives[a12_x][0][0] + a12_quantity_Ton /
                                          a12_alternatives[a12_x][1][0] + a12_quantity / a12_alternatives[a12_x][2][
                                              0]) / a12_working_hours) / a12_working_hours
    a12_hourly_cost = 0
    for i in range(len(a12_alternatives[a12_x])):
        a12_hourly_cost += a12_alternatives[a12_x][i][1]
    a12_initial_duration = a12_quantity / a12_productivity / a12_working_hours
    if a12_initial_duration < a12_allowable_duration:
        a12_crews = 1
        a12_duration = math.ceil(a12_initial_duration)
    else:
        a12_crews = math.ceil(a12_initial_duration / a12_allowable_duration)
        a12_duration = math.ceil(a12_quantity / a12_productivity / a12_working_hours / a12_crews)
    a12_ppl = 0
    for n in range(len(a12_alternatives[a12_x])):
        a12_ppl += a12_crews * math.ceil(a12_alternatives[a12_x][n][2])
    a12_ticket_cost = a12_ppl * air_ticket_cost * 2
    a12_equip_weight = 0
    for m in range(len(a12_alternatives[a12_x])):
        a12_equip_weight += a12_crews * a12_alternatives[a12_x][m][3]
    if a12_equip_weight <= 80000:
        a12_weight_cost = mobilize_duration * B34N_cost
    elif 80000 < a12_equip_weight <= 150000:
        a12_weight_cost = mobilize_duration * B34K_cost
    else:
        a12_weight_cost = mobilize_duration * B34K_cost * math.ceil(a12_equip_weight / 150000)
    a12_cost = a12_crews * a12_duration * a12_working_hours * a12_hourly_cost + a12_ticket_cost + a12_weight_cost
    a12_stop = None
    a12 = gantt.Task(name='a12_cast-in-place_piers_depends_of_[a11]',
                    start=a12_start,
                    stop=a12_stop,
                    duration=a12_duration,
                    percent_done=None,
                    resources=None,
                    color="#f4aa80",
                    depends_of=a11)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   # Total duration estimation
    work_duration = 0#(a6_start + datetime.timedelta(a6_duration) - a0_start).days #TODO
    working_days = 0#a0_duration + a1_duration + a2_duration + a3_duration + a6_duration # only activities on critical path
    idle_time = 0#work_duration - working_days
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add time-windows to schedule
    time_windows = gantt.Project(name='Time windows')
    time_windows.add_task(tw0)
    time_windows.add_task(tw1)
    time_windows.add_task(tw2)
    time_windows.add_task(tw3)
    time_windows.add_task(tw4)
    time_windows.add_task(tw5)
    # Add activities to schedule
    bridge_side_1 = gantt.Project(name='Side 1')
    bridge_side_1.add_task(a0)
    bridge_side_1.add_task(a1)
    bridge_side_1.add_task(a4)
    bridge_side_1.add_task(a5)
    bridge_side_1.add_task(a2)
    bridge_side_1.add_task(a3)
    bridge_side_1.add_task(a6)
    bridge_side_2 = gantt.Project(name='Side 2')
    bridge_side_2.add_task(a7)
    bridge_side_2.add_task(a8)
    bridge_side_2.add_task(a9)
    bridge_side_2.add_task(a10)
    bridge_side_2.add_task(a11)
    bridge_side_2.add_task(a12)
    # bridge_side_2.add_task(a13)
    # bridge_side_2.add_task(a14)
    # bridge_side_2.add_task(a15)
    # Create schedule
    schedule = gantt.Project(name='Bridge')
    schedule.add_task(time_windows)
    schedule.add_task(bridge_side_1)
    schedule.add_task(bridge_side_2)
    # Draw schedule
    if run <= 9:
        schedule.make_svg_for_tasks(filename='run ' + str(run+1) + '.svg',
                                today=None,
                                start=datetime.date(2022, 12, 1),
                                end=datetime.date(2024, 11, 1),
                                scale=gantt.DRAW_WITH_WEEKLY_SCALE)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    a1_alternative_list.append(a1_x), a1_duration_list.append(a1_duration), a1_cost_list.append(round(a1_cost, 0)), a1_crews_list.append(a1_crews), a1_prod_list.append(a1_productivity)
    a2_alternative_list.append(a2_x), a2_duration_list.append(a2_duration), a2_cost_list.append(round(a2_cost, 0)), a2_crews_list.append(a2_crews), a2_prod_list.append(a2_productivity)
    a3_alternative_list.append(a3_x), a3_duration_list.append(a3_duration), a3_cost_list.append(round(a3_cost, 0)), a3_crews_list.append(a3_crews), a3_prod_list.append(a3_productivity)
    a4_alternative_list.append(a4_x), a4_duration_list.append(a4_duration), a4_cost_list.append(round(a4_cost, 0)), a4_crews_list.append(a4_crews), a4_prod_list.append(a4_productivity)
    a5_alternative_list.append(a5_x), a5_duration_list.append(a5_duration), a5_cost_list.append(round(a5_cost, 0)), a5_crews_list.append(a5_crews), a5_prod_list.append(a5_productivity)
    a6_alternative_list.append(a6_x), a6_duration_list.append(a6_duration), a6_cost_list.append(round(a6_cost, 0)), a6_crews_list.append(a6_crews), a6_prod_list.append(a6_productivity)
    a7_alternative_list.append(a7_x), a7_duration_list.append(a7_duration), a7_cost_list.append(round(a7_cost, 0)), a7_crews_list.append(a7_crews), a7_prod_list.append(a7_productivity)
    a8_alternative_list.append(a8_x), a8_duration_list.append(a8_duration), a8_cost_list.append(round(a8_cost, 0)), a8_crews_list.append(a8_crews), a8_prod_list.append(a8_productivity)
    a9_alternative_list.append(a9_x), a9_duration_list.append(a9_duration), a9_cost_list.append(round(a9_cost, 0)), a9_crews_list.append(a9_crews), a9_prod_list.append(a9_productivity)
    a10_alternative_list.append(a10_x), a10_duration_list.append(a10_duration), a10_cost_list.append(round(a10_cost, 0)), a10_crews_list.append(a10_crews), a10_prod_list.append(a10_productivity)
    a11_alternative_list.append(a11_x), a11_duration_list.append(a11_duration), a11_cost_list.append(round(a11_cost, 0)), a11_crews_list.append(a11_crews), a11_prod_list.append(a11_productivity)
    a12_alternative_list.append(a12_x), a12_duration_list.append(a12_duration), a12_cost_list.append(round(a12_cost, 0)), a12_crews_list.append(a12_crews), a12_prod_list.append(a12_productivity)
    idle_time_list.append(idle_time)
    work_duration_list.append(work_duration)
    # Cost of temporary facilities
    if max(a1_ppl, a2_ppl, a3_ppl+a4_ppl,a3_ppl+a5_ppl, a6_ppl) <= 9: # 9 man bunk house trailer $42,900 to buy (p. 17 line 015213.200910)TODO
        temp_cost_list.append(42900)
    else: # 18 man bunk house trailer $55,000 to buy
        temp_cost_list.append(math.ceil(max(a1_ppl, a2_ppl, a3_ppl+a4_ppl,a3_ppl+a5_ppl, a6_ppl)/18) * 55000)
    run = run + 1
print(bar)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
list = list(zip(a1_alternative_list, a1_duration_list, a1_cost_list, a1_crews_list, a1_prod_list,
                a2_alternative_list, a2_duration_list, a2_cost_list, a2_crews_list, a2_prod_list,
                a3_alternative_list, a3_duration_list, a3_cost_list, a3_crews_list, a3_prod_list,
                a4_alternative_list, a4_duration_list, a4_cost_list, a4_crews_list, a4_prod_list,
                a5_alternative_list, a5_duration_list, a5_cost_list, a5_crews_list, a5_prod_list,
                a6_alternative_list, a6_duration_list, a6_cost_list, a6_crews_list, a6_prod_list,
                a7_alternative_list, a7_duration_list, a7_cost_list, a7_crews_list, a7_prod_list,
                a8_alternative_list, a8_duration_list, a8_cost_list, a8_crews_list, a8_prod_list,
                a9_alternative_list, a9_duration_list, a9_cost_list, a9_crews_list, a9_prod_list,
                a10_alternative_list, a10_duration_list, a10_cost_list, a10_crews_list, a10_prod_list,
                a11_alternative_list, a11_duration_list, a11_cost_list, a11_crews_list, a11_prod_list,
                a12_alternative_list, a12_duration_list, a12_cost_list, a12_crews_list, a12_prod_list,
                work_duration_list, idle_time_list, temp_cost_list))
df = pd.DataFrame(list, columns=["a1_berm", "a1_t", "a1_$", "a1_c", "a1_p",
                                 "a2_piles", "a2_t", "a2_$", "a2_c", "a2_p",
                                 "a3_piers", "a3_t", "a3_$", "a3_c", "a3_p",
                                 "a4_abutment_base", "a4_t", "a4_$", "a4_c", "a1_p",
                                 "a5_abutment", "a5_t", "a5_$", "a5_c", "a5_p",
                                 "a6_girders", "a6_t", "a6_$", "a6_c", "a6_p",
                                 "a7_abutment_base2", "a7_t", "a7_$", "a7_c", "a7_p",
                                 "a8_abutment2", "a8_t", "a8_$", "a8_c", "a8_p",
                                 "a9_remove_berm", "a9_t", "a9_$", "a9_c", "a9_p",
                                 "a10_berm2", "a10_t", "a10_$", "a10_c", "a10_p",
                                 "a11_piles2", "a11_t", "a11_$", "a11_c", "a11_p",
                                 "a12_piers2", "a12_t", "a12_$", "a12_c", "a12_p",
                                 "total_t", "idle_t", "temp_$"])

df["total_$"] = df["a1_$"] + df["a2_$"] + df["a3_$"] + df["a4_$"] + df["a5_$"] + df["a6_$"] + df['a7_$'] + df["temp_$"]
cost_a = 1
cost_b = 0
df["total_$_norm"] = cost_a + ((df["total_$"] - df["total_$"].min()) * (cost_b - cost_a))/(df["total_$"].max()-df["total_$"].min())
time_a = 1 # - cost_a
time_b = 0 - cost_b
df["total_t_norm"] = time_a + ((df["total_t"] - df["total_t"].min()) * (time_b - time_a))/(df["total_t"].max()-df["total_t"].min())
df["reward"] = df["total_$_norm"]/2 + df["total_t_norm"]/2

if number_of_runs <= 100:
    print(df.to_string())
# df.to_csv('data.csv')
print('-----------------------------------------------------------------------')
print('Unique duration scenarios =', format(df.nunique()["total_t"], ',d'))
print('Unique cost scenarios =', format(df.nunique()["total_$"], ',d'))
print('Total unique scenarios =', format(df.nunique()["reward"], ',d'))
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# REWARD VALUES FOR EACH alternative
print('-----------------------------------------------------------------------')
a1_average_rewards = []

for i in range(len(a1_alternatives)):
    a1_average_rewards.append(df.loc[df["a1_berm"] == i,]["reward"].mean())
    a1_productivity = min(a1_alternatives[i][0][0], a1_alternatives[i][2][0])
    a1_truck_crews = math.ceil(a1_productivity / (a1_alternatives[i][1][0] / 1.25))
    a1_hourly_cost = (a1_alternatives[i][0][1] + a1_truck_crews * a1_alternatives[i][1][1] + a1_alternatives[i][2][1])
    print('a1 berm alternative', i, '| average reward =', round(a1_average_rewards[i], 3), '| hourly crew cost =',
          round(a1_hourly_cost, 2),'$/hr| productivity =', round(a1_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a2_average_rewards = []
for i in range(len(a2_alternatives)):
    a2_average_rewards.append(df.loc[df["a2_piles"] == i,]["reward"].mean())
    a2_productivity = a2_alternatives[i][0][0]
    a2_hourly_cost = 0
    for j in range(len(a2_alternatives[i])):
        a2_hourly_cost += a2_alternatives[i][j][1]
    print('a2 piles alternative', i, '| average reward =', round(a2_average_rewards[i], 3), '| hourly crew cost =',
          round(a2_hourly_cost, 2), '$/hr | productivity =', round(a2_productivity, 2), 'VLF/hr')
print('-----------------------------------------------------------------------')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
a3_average_rewards = []
for i in range(len(a3_alternatives)):
    a3_average_rewards.append(df.loc[df["a3_piers"] == i,]["reward"].mean())
    if len(a3_alternatives[i]) == 2:
        a3_productivity = a3_alternatives[i][0][0]
    else:
        a3_productivity = a3_quantity / (
                    (a3_quantity_SFCA / a3_alternatives[i][0][0] + a3_quantity_Ton / a3_alternatives[i][1][0] +
                     a3_quantity / a3_alternatives[i][2][0]) / a3_working_hours) / a3_working_hours
    a3_hourly_cost = 0
    for j in range(len(a3_alternatives[i])):
        a3_hourly_cost += a3_alternatives[i][j][1]
    print('a3 cast-in piers alternative', i, '| average reward =', round(a3_average_rewards[i], 3), '| hourly crew cost =',
          round(a3_hourly_cost, 2), '$/hr', '| productivity =', round(a3_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a4_average_rewards = []
for i in range(len(a4_alternatives)):
    a4_average_rewards.append(df.loc[df["a4_abutment_base"] == i,]["reward"].mean())
    a4_productivity = min(a4_alternatives[i][0][0], a4_alternatives[i][2][0])
    a4_truck_crews = math.ceil(a4_productivity / (a4_alternatives[i][1][0] / 1.25))
    a4_roller_crews = math.ceil(a4_productivity / (a4_alternatives[i][3][0] / 0.9))
    a4_hourly_cost = ((a4_alternatives[i][0][1] + a4_truck_crews * a4_alternatives[i][1][1] + a4_alternatives[i][2][1]) +
                      a4_roller_crews * a4_alternatives[i][3][1])
    print('a4 abutment base alternative', i, '| average reward =', round(a4_average_rewards[i], 3), '| hourly crew cost =',
          round(a4_hourly_cost, 2), '$/hr', '| productivity =', round(a4_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a5_average_rewards = []
for i in range(len(a5_alternatives)):
    a5_average_rewards.append(df.loc[df["a5_abutment"] == i,]["reward"].mean())
    if len(a5_alternatives[i]) == 2:
        a5_productivity = a5_alternatives[i][0][0]
    else:
        a5_productivity = a5_quantity / (
                    (a5_quantity_SFCA / a5_alternatives[i][0][0] + a5_quantity_Ton / a5_alternatives[i][1][0]
                     + a5_quantity / a5_alternatives[i][2][0]) / a5_working_hours) / a5_working_hours
    a5_hourly_cost = 0
    for j in range(len(a5_alternatives[i])):
        a5_hourly_cost += a5_alternatives[i][j][1]
    print('a5 cast-in abutment alternative', i, '| average reward =', round(a5_average_rewards[i], 3), '| hourly crew cost =',
          round(a5_hourly_cost, 2), '$/hr', '| productivity =', round(a5_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a6_average_rewards = []
for i in range(len(a6_alternatives)):
    a6_average_rewards.append(df.loc[df["a6_girders"] == i,]["reward"].mean())

    a6_productivity = a6_alternatives[i][0][0]
    a6_hourly_cost = 0
    for j in range(len(a6_alternatives[i])):
        a6_hourly_cost += a6_alternatives[i][j][1]
    print('a6 girder alternative', i, '| average reward =', round(a6_average_rewards[i], 3),
          '| hourly crew cost =', round(a6_hourly_cost, 2), '$/hr', '| productivity =', round(a6_productivity, 2), 'Ton/hr')
print('-----------------------------------------------------------------------')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



