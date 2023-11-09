import datetime
import gantt
import math
import random
import pandas as pd
import numpy as np
number_of_runs = 1000000
pd.set_option('display.max_columns', None)
# Formatting
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")

gantt.define_not_worked_days([])  # list_of_days -- list of integer (0: Monday ... 6: Sunday) - default [5, 6]
# CREWS
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Berm'''
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Abutment base'''
'''Berm crews plus compaction crew'''
# Compact
# [output/hr CCY, cost $/hr, workers, total equipment weight lb]
B10G = [162.5, 269.9, 1.5, 49652, '815 sheep-foot roller'] # line 32 23 23.24 0300 (p. 619)
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Cast-in-place piers'''
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Cast-in-place abutment'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Girder installation'''
#Crane method
# [output/hr Ton, cost $/hr, workers, total crane weight lb]
E5 = [1.61, 1101, 10, 115919, 'TEREX RT 100 90 ton crane']
# Incremental Launching method
# [output/hr Ton, cost $/hr, workers, total crane and lunging equipment weight lb] output calculated as 450m bridge/2 =
# = 225/(25m lunging per week cycle) x 1.152 ton/m weight of girders
E6 = [4.11, 1653 + 125, 16, 30000 + 115919, 'TEREX RT 100 90 ton crane'] # added $1000 per day for lunging equipment rental cost, and 30k of weight to account for lunging equipment
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# DATA MANAGEMENT
a1_option_list = []
a1_duration_list = []
a1_cost_list = []
a2_option_list = []
a2_duration_list = []
a2_cost_list = []
a3_option_list = []
a3_duration_list = []
a3_cost_list = []
a4_option_list = []
a4_duration_list = []
a4_cost_list = []
a5_option_list = []
a5_duration_list = []
a5_cost_list = []
a6_option_list = []
a6_duration_list = []
a6_cost_list = []
work_duration_list = []
idle_time_list = []
temp_cost_list = []
run = 0
while run != number_of_runs:
    #run_number.append(run+1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW WINTER ROAD 2022-2023
    tw0_start_rand = random.randint(10, 30)
    tw0_stop_rand = random.randint(1, 20)
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
    tw1_start_rand = random.randint(5, 25)
    tw1_stop_rand = random.randint(1, 20)
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
    # TIME-WINDOW WINTER ROAD 2023-2024
    tw2_start_rand = random.randint(10, 30)
    tw2_stop_rand = random.randint(1, 20)
    tw2_start = datetime.date(2023, 12, tw2_start_rand)
    tw2_stop = datetime.date(2024, 4, tw2_stop_rand)
    tw2_duration = tw2_stop - tw2_start
    tw2 = gantt.Task(name='tw2_winter_road',
                     start=tw2_start,
                     stop=tw2_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
    # BUILD BERM
    # Crew options
    a1_option_0 = [B12B, B34E, B10W]
    a1_option_1 = [B12C, B34F, B10B]
    a1_option_2 = [B12D, B34G, B10X]
    a1_options = [a1_option_0, a1_option_1, a1_option_2]
    a1_x = random.randint(0,len(a1_options)-1)
    a1_working_hours = 8
    a1_quantity = 88752  # BCY
    a1_allowable_duration = tw0_duration.days - a0_duration
    a1_productivity = min(a1_options[a1_x][0][0], a1_options[a1_x][2][0])
    a1_truck_crews = math.ceil(a1_productivity / (a1_options[a1_x][1][0] / 1.25)) # 1.25 - bank to loose conversion factor
    a1_hourly_cost = (a1_options[a1_x][0][1] + a1_truck_crews * a1_options[a1_x][1][1] + a1_options[a1_x][2][1])
    a1_initial_duration = a1_quantity / a1_productivity / a1_working_hours
    if a1_initial_duration < a1_allowable_duration:
        a1_crews = 1
        a1_duration = math.ceil(a1_initial_duration)
    else:
        a1_crews = math.ceil(a1_initial_duration/a1_allowable_duration)
        a1_duration = math.ceil(a1_quantity / a1_productivity / a1_working_hours / a1_crews)
    a1_ppl = math.ceil(a1_options[a1_x][0][2] + a1_options[a1_x][1][2] * a1_truck_crews + a1_options[a1_x][2][2]) * a1_crews
    a1_ticket_cost = a1_ppl * 1080 * 2
    a1_equip_weight = math.ceil(a1_options[a1_x][0][3] + a1_options[a1_x][1][3] * a1_truck_crews + a1_options[a1_x][2][3]) * a1_crews
    if a1_equip_weight <= 80000: # Crew B-34N
        a1_weight_cost = 4.5 * 1084.52
    elif 80000 < a1_equip_weight <= 150000: # Crew B-34K
        a1_weight_cost = 4.5 * 1516.82
    else:
        a1_weight_cost = 4.5 * 1516.82 * math.ceil(a1_equip_weight/150000)
    a1_cost = a1_crews * a1_duration * a1_working_hours * a1_hourly_cost + a1_ticket_cost + a1_weight_cost
    a1_start = a0_start + datetime.timedelta(a0_duration)
    a1_stop = None
    a1 = gantt.Task(name='a1_build_berm',
                    start=a1_start,
                    stop=a1_stop,
                    duration=a1_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a0)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # INSTALL PILES
    a2_option_0 = [B19_CONCRETE]
    a2_option_1 = [B48_CAST_IN, CARMIX_3500]
    a2_option_2 = [B19_STEEL]
    a2_options = [a2_option_0, a2_option_1, a2_option_2]
    a2_x = random.randint(0, len(a2_options) - 1)
    a2_working_hours = 8
    a2_quantity = 6200  # VLF (64 piles x 50')
    a2_allowable_duration = (tw1_start - tw0_stop).days - 1
    a2_productivity = a2_options[a2_x][0][0]
    # Hourly cost
    a2_hourly_cost = 0
    for i in range(len(a2_options[a2_x])):
        a2_hourly_cost += a2_options[a2_x][i][1]
    a2_initial_duration = a2_quantity / a2_productivity / a2_working_hours
    if a2_initial_duration < a2_allowable_duration:
        a2_crews = 1
        a2_duration = math.ceil(a2_initial_duration)
    else:
        a2_crews = math.ceil(a2_initial_duration / a2_allowable_duration)
        a2_duration = math.ceil(a2_quantity / a2_productivity / a2_working_hours / a2_crews)
    a2_ppl = 0
    for n in range(len(a2_options[a2_x])):
        a2_ppl += a2_crews * math.ceil(a2_options[a2_x][n][2])
    a2_ticket_cost = a2_ppl * 1080 * 2
    a2_equip_weight = 0
    for m in range(len(a2_options[a2_x])):
        a2_equip_weight += a2_crews * a2_options[a2_x][m][3]
    if a2_equip_weight <= 80000: # Crew B-34N
        a2_weight_cost = 4.5 * 1084.52
    elif 80000 < a2_equip_weight <= 150000: # Crew B-34K
        a2_weight_cost = 4.5 * 1516.82
    else:
        a2_weight_cost = 4.5 * 1516.82 * math.ceil(a2_equip_weight/150000)
    a2_cost = a2_crews * a2_duration * a2_working_hours * a2_hourly_cost + a2_ticket_cost + a2_weight_cost
    a2_start = tw0_stop + datetime.timedelta(1)
    a2_stop = None
    a2 = gantt.Task(name='a2_install_piles',
                    start=a2_start,
                    stop=a2_stop,
                    duration=a2_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # CAST-IN-PLACE PIERS
    # Crew options
    a3_option_0 = [C14A, CARMIX_3500]
    a3_option_1 = [C2, C4A_adjusted, C20, CARMIX_3500]
    a3_option_2 = [C2, C4A_adjusted, C7, CARMIX_3500]
    a3_options = [a3_option_0, a3_option_1, a3_option_2]
    a3_x = random.randint(0, len(a3_options) - 1)
    a3_working_hours = 8
    a3_quantity = 2*1674.18  # CY
    a3_quantity_SFCA = 2*10979.19 # SFCA
    a3_quantity_Ton = 2*219.8 # Ton
    a3_allowable_duration = tw1_duration.days
    # Productivity
    if len(a3_options[a3_x]) == 2:
        a3_productivity = a3_options[a3_x][0][0]
    else:
        a3_productivity = a3_quantity/((a3_quantity_SFCA/a3_options[a3_x][0][0] + a3_quantity_Ton/a3_options[a3_x][1][0] +
                                        a3_quantity/a3_options[a3_x][2][0])/a3_working_hours)/a3_working_hours # manipulate number of crews here
    # Hourly cost
    a3_hourly_cost = 0
    for i in range(len(a3_options[a3_x])):
        a3_hourly_cost += a3_options[a3_x][i][1]
    a3_initial_duration = a3_quantity / a3_productivity / a3_working_hours
    if a3_initial_duration < a3_allowable_duration:
        a3_crews = 1
        a3_duration = math.ceil(a3_initial_duration)
    else:
        a3_crews = math.ceil(a3_initial_duration / a3_allowable_duration)
        a3_duration = math.ceil(a3_quantity / a3_productivity / a3_working_hours / a3_crews)
    a3_ppl = 0
    for n in range(len(a3_options[a3_x])):
        a3_ppl += a3_crews * math.ceil(a3_options[a3_x][n][2])
    a3_ticket_cost = a3_ppl * 1080 * 2
    a3_equip_weight = 0
    for m in range(len(a3_options[a3_x])):
        a3_equip_weight += a3_crews * a3_options[a3_x][m][3]
    if a3_equip_weight <= 80000: # Crew B-34N
        a3_weight_cost = 4.5 * 1084.52
    elif 80000 < a3_equip_weight <= 150000: # Crew B-34K
        a3_weight_cost = 4.5 * 1516.82
    else:
        a3_weight_cost = 4.5 * 1516.82 * math.ceil(a3_equip_weight/150000)
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
    # ABUTMENT BASE
    a4_option_0 = [B12B, B34E, B10W, B10G]
    a4_option_1 = [B12C, B34F, B10B, B10G]
    a4_option_2 = [B12D, B34G, B10X, B10G]
    a4_options = [a4_option_0, a4_option_1, a4_option_2]
    a4_x = random.randint(0, len(a4_options) - 1)
    a4_working_hours = 8
    a4_quantity = 20631  # BCY
    a4_allowable_duration = tw1_duration.days/2
    a4_productivity = min(a4_options[a4_x][0][0], a4_options[a4_x][2][0])
    a4_truck_crews = math.ceil(a4_productivity / (a4_options[a4_x][1][0] / 1.25))
    a4_roller_crews = math.ceil(a4_productivity / (a4_options[a4_x][3][0] / 0.9))
    a4_hourly_cost = ((a4_options[a4_x][0][1] + a4_truck_crews * a4_options[a4_x][1][1] + a4_options[a4_x][2][1]) +
                      a4_roller_crews * a4_options[a4_x][3][1]) # 0.9 - compacted to bank conversion factor; 1.25 -  bank to loose conversion factor
    a4_initial_duration = a4_quantity / a4_productivity / a4_working_hours
    if a4_initial_duration < a4_allowable_duration:
        a4_crews = 1
        a4_duration = math.ceil(a4_initial_duration)
    else:
        a4_crews = math.ceil(a4_initial_duration / a4_allowable_duration)
        a4_duration = math.ceil(a4_quantity / a4_productivity / a4_working_hours / a4_crews)
    a4_ppl = math.ceil(a4_options[a4_x][0][2]+a4_options[a4_x][1][2]*a4_truck_crews + a4_options[a4_x][2][2] + a4_options[a4_x][3][2]*a4_roller_crews) * a4_crews
    a4_ticket_cost = a4_ppl * 1080 * 2
    a4_equip_weight = math.ceil(a4_options[a4_x][0][3]+a4_options[a4_x][1][3]*a4_truck_crews + a4_options[a4_x][2][3] + a4_options[a4_x][3][3]*a4_roller_crews) * a4_crews
    if a4_equip_weight <= 80000:  # Crew B-34N
        a4_weight_cost = 4.5 * 1084.52
    elif 80000 < a4_equip_weight <= 150000:  # Crew B-34K
        a4_weight_cost = 4.5 * 1516.82
    else:
        a4_weight_cost = 4.5 * 1516.82 * math.ceil(a4_equip_weight / 150000)
    a4_cost = a1_crews * a4_duration * a4_working_hours * a4_hourly_cost + a4_ticket_cost + a4_weight_cost
    a4_start = tw1_start
    a4_stop = None
    a4 = gantt.Task(name='a4_abutment_base_depends_of_[a1]',
                    start=a4_start,
                    stop=a4_stop,
                    duration=a4_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # CAST-IN-PLACE ABUTMENT
    a5_option_0 = [C14A, CARMIX_3500]
    a5_option_1 = [C2, C4A_adjusted, C20, CARMIX_3500]
    a5_option_2 = [C2, C4A_adjusted, C7, CARMIX_3500]
    a5_options = [a5_option_0, a5_option_1, a5_option_2]
    a5_x = random.randint(0, len(a5_options) - 1)
    a5_working_hours = 8
    a5_quantity = 978.21  # CY
    a5_quantity_SFCA = 3790.17  # SFCA
    a5_quantity_Ton = 75  # Ton
    a5_allowable_duration = tw1_duration.days - a4_duration
    # Productivity
    if len(a5_options[a5_x]) == 2:
        a5_productivity = a5_options[a5_x][0][0]
    else:
        a5_productivity = a5_quantity / ((a5_quantity_SFCA / a5_options[a5_x][0][0] + a5_quantity_Ton / a5_options[a5_x][1][0]
                                          + a5_quantity / a5_options[a5_x][2][0]) / a5_working_hours) / a5_working_hours
    # Hourly cost
    a5_hourly_cost = 0
    for i in range(len(a5_options[a5_x])):
        a5_hourly_cost += a5_options[a5_x][i][1]
    a5_initial_duration = a5_quantity / a5_productivity / a5_working_hours
    if a5_initial_duration < a5_allowable_duration:
        a5_crews = 1
        a5_duration = math.ceil(a5_initial_duration)
    else:
        a5_crews = math.ceil(a5_initial_duration / a5_allowable_duration)
        a5_duration = math.ceil(a5_quantity / a5_productivity / a5_working_hours / a5_crews)
    a5_ppl = 0
    for n in range(len(a5_options[a5_x])):
        a5_ppl += a5_crews * math.ceil(a5_options[a5_x][n][2])
    a5_ticket_cost = a5_ppl * 1080 * 2
    a5_equip_weight = 0
    for m in range(len(a5_options[a5_x])):
        a5_equip_weight += a5_crews * a5_options[a5_x][m][3]
    if a5_equip_weight <= 80000:  # Crew B-34N
        a5_weight_cost = 4.5 * 1084.52
    elif 80000 < a5_equip_weight <= 150000:  # Crew B-34K
        a5_weight_cost = 4.5 * 1516.82
    else:
        a5_weight_cost = 4.5 * 1516.82 * math.ceil(a5_equip_weight / 150000)
    a5_cost = a5_crews * a5_duration * a5_working_hours * a5_hourly_cost + a5_ticket_cost + a5_weight_cost
    a5_start = a4_start + datetime.timedelta(a4_duration)
    a5_stop = None
    a5 = gantt.Task(name='a5_cast-in-place_abutment',
                    start=a5_start,
                    stop=a5_stop,
                    duration=a5_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a4)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # INSTALL GIRDERS
    a6_option_0 = [E5]
    a6_option_1 = [E6]
    a6_options = [a6_option_0, a6_option_1]
    a6_x = random.randint(0, len(a6_options) - 1)
    a6_working_hours = 8
    a6_quantity = 1296  # Imperial ton
    a6_start = a3_start + datetime.timedelta(a3_duration)
    a6_allowable_duration = (tw2_start - a6_start).days
    a6_productivity = a6_options[a6_x][0][0]
    # Hourly cost
    a6_hourly_cost = 0
    for i in range(len(a6_options[a6_x])):
        a6_hourly_cost += a6_options[a6_x][i][1]
    a6_initial_duration = a6_quantity / a6_productivity / a6_working_hours
    if a6_initial_duration < a6_allowable_duration:
        a6_crews = 1
        a6_duration = math.ceil(a6_initial_duration)
    else:
        a6_crews = math.ceil(a6_initial_duration / a6_allowable_duration)
        a6_duration = math.ceil(a6_quantity / a6_productivity / a6_working_hours / a6_crews)
    a6_ppl = 0
    for n in range(len(a6_options[a6_x])):
        a6_ppl += a6_crews * math.ceil(a6_options[a6_x][n][2])
    a6_ticket_cost = a6_ppl * 1080 * 2
    a6_equip_weight = 0
    for m in range(len(a6_options[a6_x])):
        a6_equip_weight += a6_crews * a6_options[a6_x][m][3]
    if a6_equip_weight <= 80000: # Crew B-34N
        a6_weight_cost = 4.5 * 1084.52
    elif 80000 < a6_equip_weight <= 150000: # Crew B-34K
        a6_weight_cost = 4.5 * 1516.82
    else:
        a6_weight_cost = 4.5 * 1516.82 * math.ceil(a6_equip_weight/150000)
    a6_cost = a6_crews * a6_duration * a6_working_hours * a6_hourly_cost + a6_ticket_cost + a6_weight_cost
    a6_stop = a6_start + datetime.timedelta(a6_duration)
    a6 = gantt.Task(name='a6_install_girders_depends_of_[a3, a5]',
                    start=a6_start,
                    stop=None,
                    duration=a6_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=[a3, a5])
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   # Total duration estimation
    work_duration = (a6_start + datetime.timedelta(a6_duration) - a0_start).days
    working_days = a0_duration + a1_duration + a2_duration + a3_duration + a6_duration # only activities on critical path
    idle_time = work_duration - working_days
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add time-windows to schedule
    time_windows = gantt.Project(name='Time windows')
    time_windows.add_task(tw0)
    time_windows.add_task(tw1)
    time_windows.add_task(tw2)
    # Add activities to schedule
    bridge_side_1 = gantt.Project(name='Side 1')
    bridge_side_1.add_task(a0)
    bridge_side_1.add_task(a1)
    bridge_side_1.add_task(a2)
    bridge_side_1.add_task(a3)
    bridge_side_1.add_task(a4)
    bridge_side_1.add_task(a5)
    bridge_side_1.add_task(a6)
    # Create schedule
    schedule = gantt.Project(name='Bridge')
    schedule.add_task(time_windows)
    schedule.add_task(bridge_side_1)
    # Draw schedule
    if number_of_runs <= 5:
        schedule.make_svg_for_tasks(filename='run ' + str(run+1) + '.svg',
                                today=None,
                                start=datetime.date(2022, 12, 1),
                                end=datetime.date(2024, 1, 15),
                                scale=gantt.DRAW_WITH_WEEKLY_SCALE)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    a1_option_list.append(a1_x)
    a1_duration_list.append(a1_duration)
    a1_cost_list.append(a1_cost)
    a2_option_list.append(a2_x)
    a2_duration_list.append(a2_duration)
    a2_cost_list.append(a2_cost)
    a3_option_list.append(a3_x)
    a3_duration_list.append(a3_duration)
    a3_cost_list.append(a3_cost)
    a4_option_list.append(a4_x)
    a4_duration_list.append(a4_duration)
    a4_cost_list.append(a4_cost)
    a5_option_list.append(a5_x)
    a5_duration_list.append(a5_duration)
    a5_cost_list.append(a5_cost)
    a6_option_list.append(a6_x)
    a6_duration_list.append(a6_duration)
    a6_cost_list.append(a6_cost)
    idle_time_list.append(idle_time)
    work_duration_list.append(work_duration)
    # Cost of temporary facilities
    if max(a1_ppl, a2_ppl, a3_ppl+a4_ppl,a3_ppl+a5_ppl, a6_ppl) <= 9: # 9 man bunk house trailer $42,900 to buy (p. 17 line 015213.200910)
        temp_cost_list.append(42900)
    else: # 18 man bunk house trailer $55,000 to buy
        temp_cost_list.append(math.ceil(max(a1_ppl, a2_ppl, a3_ppl+a4_ppl,a3_ppl+a5_ppl, a6_ppl)/18) * 55000)
    run = run + 1
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# NOTES
# Cost of moving equipment from Hay River to Tulita by Winter road (max speed - 50km/hr, distance 900 km, total of 4.5 days there and back)
# Ticket from Yellowknife to Tulita one way - $1080
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
list = list(zip(a1_option_list, a1_duration_list, a1_cost_list, a2_option_list, a2_duration_list, a2_cost_list, a3_option_list,
                a3_duration_list, a3_cost_list, a4_option_list, a4_duration_list, a4_cost_list, a5_option_list, a5_duration_list,
                a5_cost_list, a6_option_list, a6_duration_list, a6_cost_list, work_duration_list, idle_time_list, temp_cost_list))
df = pd.DataFrame(list, columns=["a1_berm", "a1_t", "a1_$", "a2_piles", "a2_t", "a2_$", "a3_piers", "a3_t", "a3_$",
                                 "a4_abutment_base", "a4_t", "a4_$", "a5_abutment", "a5_t", "a5_$", "a6_girders", "a6_t", "a6_$",
                                 "total_t", "idle_t", "temp_$"])

df["total_$"] = df["a1_$"] + df["a2_$"] + df["a3_$"] + df["a4_$"] + df["a5_$"] + df["a6_$"] + df["temp_$"]
cost_a = 1
cost_b = 0
df["total_$_norm"] = cost_a + ((df["total_$"] - df["total_$"].min()) * (cost_b - cost_a))/(df["total_$"].max()-df["total_$"].min())
time_a = 1 # - cost_a
time_b = 0 - cost_b
df["total_t_norm"] = time_a + ((df["total_t"] - df["total_t"].min()) * (time_b - time_a))/(df["total_t"].max()-df["total_t"].min())
df["reward"] = df["total_$_norm"]/2 + df["total_t_norm"]/2

if number_of_runs <= 100:
    print(df.to_string())
#df.to_csv('data.csv')
print('-----------------------------------------------------------------------')
print('Unique duration scenarios ', df.nunique()["total_t_norm"])
print('Unique cost scenarios', df.nunique()["total_$_norm"])
print('Total unique scenarios =', df.nunique()["reward"])
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# REWARD VALUES FOR EACH OPTION
print('-----------------------------------------------------------------------')
a1_average_rewards = []

for i in range(len(a1_options)):
    a1_average_rewards.append(df.loc[df["a1_berm"] == i,]["reward"].mean())
    a1_productivity = min(a1_options[i][0][0], a1_options[i][2][0])
    a1_truck_crews = math.ceil(a1_productivity / (a1_options[i][1][0] / 1.25))
    a1_hourly_cost = (a1_options[i][0][1] + a1_truck_crews * a1_options[i][1][1] + a1_options[i][2][1])
    print('a1 berm option', i, '| average reward =', round(a1_average_rewards[i], 3), '| hourly crew cost =',
          round(a1_hourly_cost, 2),'$/hr| productivity =', round(a1_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a2_average_rewards = []
for i in range(len(a2_options)):
    a2_average_rewards.append(df.loc[df["a2_piles"] == i,]["reward"].mean())
    a2_productivity = a2_options[i][0][0]
    a2_hourly_cost = 0
    for j in range(len(a2_options[i])):
        a2_hourly_cost += a2_options[i][j][1]
    print('a2 piles option', i, '| average reward =', round(a2_average_rewards[i], 3), '| hourly crew cost =',
          round(a2_hourly_cost, 2), '$/hr | productivity =', round(a2_productivity, 2), 'VLF/hr')
print('-----------------------------------------------------------------------')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
a3_average_rewards = []
for i in range(len(a3_options)):
    a3_average_rewards.append(df.loc[df["a3_piers"] == i,]["reward"].mean())
    if len(a3_options[i]) == 2:
        a3_productivity = a3_options[i][0][0]
    else:
        a3_productivity = a3_quantity / (
                    (a3_quantity_SFCA / a3_options[i][0][0] + a3_quantity_Ton / a3_options[i][1][0] +
                     a3_quantity / a3_options[i][2][0]) / a3_working_hours) / a3_working_hours
    a3_hourly_cost = 0
    for j in range(len(a3_options[i])):
        a3_hourly_cost += a3_options[i][j][1]
    print('a3 cast-in piers option', i, '| average reward =', round(a3_average_rewards[i], 3), '| hourly crew cost =',
          round(a3_hourly_cost, 2), '$/hr', '| productivity =', round(a3_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a4_average_rewards = []
for i in range(len(a4_options)):
    a4_average_rewards.append(df.loc[df["a4_abutment_base"] == i,]["reward"].mean())
    a4_productivity = min(a4_options[i][0][0], a4_options[i][2][0])
    a4_truck_crews = math.ceil(a4_productivity / (a4_options[i][1][0] / 1.25))
    a4_roller_crews = math.ceil(a4_productivity / (a4_options[i][3][0] / 0.9))
    a4_hourly_cost = ((a4_options[i][0][1] + a4_truck_crews * a4_options[i][1][1] + a4_options[i][2][1]) +
                      a4_roller_crews * a4_options[i][3][1])
    print('a4 abutment base option', i, '| average reward =', round(a4_average_rewards[i], 3), '| hourly crew cost =',
          round(a4_hourly_cost, 2), '$/hr', '| productivity =', round(a4_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a5_average_rewards = []
for i in range(len(a5_options)):
    a5_average_rewards.append(df.loc[df["a5_abutment"] == i,]["reward"].mean())
    if len(a5_options[i]) == 2:
        a5_productivity = a5_options[i][0][0]
    else:
        a5_productivity = a5_quantity / (
                    (a5_quantity_SFCA / a5_options[i][0][0] + a5_quantity_Ton / a5_options[i][1][0]
                     + a5_quantity / a5_options[i][2][0]) / a5_working_hours) / a5_working_hours
    a5_hourly_cost = 0
    for j in range(len(a5_options[i])):
        a5_hourly_cost += a5_options[i][j][1]
    print('a5 cast-in abutment option', i, '| average reward =', round(a5_average_rewards[i], 3), '| hourly crew cost =',
          round(a5_hourly_cost, 2), '$/hr', '| productivity =', round(a5_productivity, 2), 'CY/hr')
print('-----------------------------------------------------------------------')
a6_average_rewards = []
for i in range(len(a6_options)):
    a6_average_rewards.append(df.loc[df["a6_girders"] == i,]["reward"].mean())

    a6_productivity = a6_options[i][0][0]
    a6_hourly_cost = 0
    for j in range(len(a6_options[i])):
        a6_hourly_cost += a6_options[i][j][1]
    print('a6 girder option', i, '| average reward =', round(a6_average_rewards[i], 3),
          '| hourly crew cost =', round(a6_hourly_cost, 2), '$/hr', '| productivity =', round(a6_productivity, 2), 'Ton/hr')
print('-----------------------------------------------------------------------')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



