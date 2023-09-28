##
import datetime
import gantt
import math
import random
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
# Formatting
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")

gantt.define_not_worked_days([])  # list_of_days -- list of integer (0: Monday ... 6: Sunday) - default [5, 6]
# DATA MANAGEMENT
#run_number = []
a2_option_list = []
a2_duration_list = []
a2_cost_list = []
a2_ppl_list = []
a2_weight_list = []
a3_option_list = []
a3_duration_list = []
a3_cost_list = []
a3_ppl_list = []
a3_weight_list = []
a4_option_list = []
a4_duration_list = []
a4_cost_list = []
a4_ppl_list = []
a4_weight_list = []
a5_option_list = []
a5_duration_list = []
a5_cost_list = []
a5_ppl_list = []
a5_weight_list = []
work_duration_list = []
idle_time_list = []
ppl_cost = []
mobilize_cost = []
run = 0
while run != 10:
    #run_number.append(run+1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW WINTER ROAD 2022-2023
    tw1_start = datetime.date(2022, 12, 20)
    tw1_stop = datetime.date(2023, 4, 1)
    tw1_duration = tw1_stop - tw1_start
    tw1 = gantt.Task(name='tw1_winter_road',
                     start=tw1_start,
                     stop=tw1_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # MOBILIZE JOB SITE
    a1_start = tw1_start
    a1_stop = None
    a1_duration = random.randint(30,30)#tw1_2023_duration.days/2
    a1 = gantt.Task(name='a1_mobilize_job_site',
                    start=a1_start,
                    stop=a1_stop,
                    duration=a1_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # BUILD BERM S1
    # Excavate (p. 603, added 15% to cost for loading onto trucks)
    # [output/hr BCY, cost $/hr, workers, equipment weight lb, excavator capacity, CAT model]
    B12B = [125, 316, 2, 49600, '1.5 CY', '320 4F excavator'] # line 31 23 16.42 0250
    B12C = [165, 339, 2, 67900, '2 CY', '330 GC excavator'] # line 31 23 16.42 0260
    B12D = [260, 539, 2, 83100, '3.5 CY', '340 excavator'] # line 31 23 16.42 0300
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
    # Crew options
    a2_option_0 = [B12B, B34E, B10W]
    a2_option_1 = [B12C, B34F, B10B]
    a2_option_2 = [B12D, B34G, B10X]
    a2_options = [a2_option_0, a2_option_1, a2_option_2]
    a2_x = random.randint(0,len(a2_options)-1)
    a2_working_hours = 8
    a2_quantity = 88752  # BCY
    a2_allowable_duration = tw1_duration.days - a1_duration
    a2_productivity = min(a2_options[a2_x][0][0], a2_options[a2_x][2][0])
    a2_hourly_cost = (
            a2_options[a2_x][0][1] + math.ceil(a2_productivity / a2_options[a2_x][1][0] / 1.25) *
            a2_options[a2_x][1][1] + a2_options[a2_x][2][1])
    a2_initial_duration = a2_quantity / a2_productivity / a2_working_hours
    if a2_initial_duration < a2_allowable_duration:
        a2_crews = 1
        a2_duration = math.ceil(a2_initial_duration)
    else:
        a2_crews = math.ceil(a2_initial_duration/a2_allowable_duration)
        a2_duration = math.ceil(a2_quantity / a2_productivity / a2_working_hours / a2_crews)
    a2_ppl = 0
    for n in range(len(a2_options[a2_x])):
        a2_ppl += a2_crews * math.ceil(a2_options[a2_x][n][2])
    a2_equip_weight = 0
    for m in range(len(a2_options[a2_x])):
        a2_equip_weight += a2_crews * a2_options[a2_x][m][3]
    # Cost of moving equipment from Hay River to Tulita by Winter road (max speed - 50km/hr, distance 900 km, total of 4.5 days there and back)
    if a2_equip_weight <= 80000: # Crew B-34N
        a2_weight_cost = 4.5 * 1084.52
    elif 80000 < a2_equip_weight <= 150000: # Crew B-34K
        a2_weight_cost = 4.5 * 1516.82
    else:
        a2_weight_cost = 4.5 * 1516.82 * math.ceil(a2_equip_weight/150000)
    a2_cost = a2_crews * a2_duration * a2_working_hours * a2_hourly_cost
    a2_start = a1_start + datetime.timedelta(a1_duration)
    a2_stop = None
    a2 = gantt.Task(name='a2_build_berm',
                    start=a2_start,
                    stop=a2_stop,
                    duration=a2_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a1)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW TEMPERATURE ABOVE ZERO 2023
    tw2_start = datetime.date(2023, 5, 1)
    tw2_stop = datetime.date(2023, 10, 15)
    tw2_duration = tw2_stop - tw2_start
    tw2 = gantt.Task(name='tw2_temperature_>0C°',
                     start=tw2_start,
                     stop=tw2_stop,
                     duration=None,
                     percent_done=None,
                     resources=None,
                     color="#ADD8E6",
                     depends_of=None)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # INSTALL PILES S1
    # Driven prestressed, precast concrete piles 50' long, 12" diameter, 2-3/8" wall
    # [output/hr VLF, cost $/hr, workers, total equipment weight: 1 crawler crane 40 ton, 1 lead 90' high, 1 diesel hammer 22k ft-lb]
    B19_CONCRETE = [90, 827, 8, 96000+8055, 'SCC400TB 40 Ton crane, I-12V2 diesel hummer with lead'] # line 31 62 13.23 2200 (p.624) TODO
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
    a3_option_0 = [B19_CONCRETE]
    a3_option_1 = [B48_CAST_IN, CARMIX_3500]
    a3_option_2 = [B19_STEEL]
    a3_options = [a3_option_0, a3_option_1, a3_option_2]
    a3_x = random.randint(0, len(a3_options) - 1)
    a3_working_hours = 8
    a3_quantity = 6200  # VLF (64 piles x 50')
    a3_allowable_duration = (tw2_start - tw1_stop).days - 1
    a3_productivity = a3_options[a3_x][0][0]
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
    a3_equip_weight = 0
    for m in range(len(a3_options[a3_x])):
        a3_equip_weight += a3_crews * a3_options[a3_x][m][3]
    if a3_equip_weight <= 80000: # Crew B-34N
        a3_weight_cost = 4.5 * 1084.52
    elif 80000 < a3_equip_weight <= 150000: # Crew B-34K
        a3_weight_cost = 4.5 * 1516.82
    else:
        a3_weight_cost = 4.5 * 1516.82 * math.ceil(a3_equip_weight/150000)
    a3_cost = a3_crews * a3_duration * a3_working_hours * a3_hourly_cost
    a3_start = tw1_stop + datetime.timedelta(1)
    #a2_idle_time = (a3_start-a2_start).days - a2_duration
    a3_stop = None
    a3 = gantt.Task(name='a3_install_piles',
                    start=a3_start,
                    stop=a3_stop,
                    duration=a3_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a2)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # CAST-INPLACE PIERS S1
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
    # Crew options
    a4_option_0 = [C14A, CARMIX_3500]
    a4_option_1 = [C2, C4A_adjusted, C20, CARMIX_3500]
    a4_option_2 = [C2, C4A_adjusted, C7, CARMIX_3500]
    a4_options = [a4_option_0, a4_option_1, a4_option_2]
    a4_x = random.randint(0, len(a4_options) - 1)
    a4_working_hours = 8
    a4_quantity = 2*1674.18  # CY
    a4_quantity_SFCA = 2*10979.19 # SFCA
    a4_quantity_Ton = 2*219.8 # Ton
    a4_allowable_duration = tw2_duration.days
    # Productivity
    if len(a4_options[a4_x]) == 2:
        a4_productivity = a4_options[a4_x][0][0]
    else:
        a4_productivity = a4_quantity/((a4_quantity_SFCA/a4_options[a4_x][0][0] + a4_quantity_Ton/a4_options[a4_x][1][0] +
                                        a4_quantity/a4_options[a4_x][2][0])/a4_working_hours)/a4_working_hours # manipulate number of crews here
    # Hourly cost
    a4_hourly_cost = 0
    for i in range(len(a4_options[a4_x])):
        a4_hourly_cost += a4_options[a4_x][i][1]
    a4_initial_duration = a4_quantity / a4_productivity / a4_working_hours
    if a4_initial_duration < a4_allowable_duration:
        a4_crews = 1
        a4_duration = math.ceil(a4_initial_duration)
    else:
        a4_crews = math.ceil(a4_initial_duration / a4_allowable_duration)
        a4_duration = math.ceil(a4_quantity / a4_productivity / a4_working_hours / a4_crews)
    a4_ppl = 0
    for n in range(len(a4_options[a4_x])):
        a4_ppl += a4_crews * math.ceil(a4_options[a4_x][n][2])
    a4_equip_weight = 0
    for m in range(len(a4_options[a4_x])):
        a4_equip_weight += a4_crews * a4_options[a4_x][m][3]
    if a4_equip_weight <= 80000: # Crew B-34N
        a4_weight_cost = 4.5 * 1084.52
    elif 80000 < a4_equip_weight <= 150000: # Crew B-34K
        a4_weight_cost = 4.5 * 1516.82
    else:
        a4_weight_cost = 4.5 * 1516.82 * math.ceil(a4_equip_weight/150000)
    a4_cost = a4_crews * a4_duration * a4_working_hours * a4_hourly_cost
    a4_start = tw2_start
    #a3_idle_time = (a4_start - a3_start).days - a3_duration
    a4_stop = None
    a4 = gantt.Task(name='a4_cast-in-place_piers',
                    start=a4_start,
                    stop=a4_stop,
                    duration=a4_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a3)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # TIME-WINDOW WINTER ROAD 2023-2024
    tw3_start = datetime.date(2023, 12, 20)
    tw3_stop = datetime.date(2024, 4, 1)
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
    # INSTALL GIRDERS
    # Crane method
    # [output/hr Ton, cost $/hr, workers, total crane weight lb]
    E5 = [1.61, 1101, 10, 115919, 'TEREX RT 100 90 ton crane']
    # Incremental Launching method
    # [output/hr Ton, cost $/hr, workers, total crane and lunging equipment weight lb] output calculated as 450m bridge/2 = 225/(25m lunging per week cycle) x
    # --------------------------------------------------------------------  x 1.152 ton/m weight of girders
    E6 = [4.11, 1653+125, 16, 30000+115919, 'TEREX RT 100 90 ton crane'] # added $1000 per day for lunging equipment rental cost, and 30k of weight to account for lunging equipment
    a5_option_0 = [E5]
    a5_option_1 = [E6]
    a5_options = [a5_option_0, a5_option_1]
    a5_x = random.randint(0, len(a5_options) - 1)
    a5_working_hours = 8
    a5_quantity = 1296  # Imperial ton
    a5_start = a4_start + datetime.timedelta(a4_duration)
    a5_allowable_duration = (tw3_start - a5_start).days
    a5_productivity = a5_options[a5_x][0][0]
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
    a5_equip_weight = 0
    for m in range(len(a5_options[a5_x])):
        a5_equip_weight += a5_crews * a5_options[a5_x][m][3]
    if a5_equip_weight <= 80000: # Crew B-34N
        a5_weight_cost = 4.5 * 1084.52
    elif 80000 < a5_equip_weight <= 150000: # Crew B-34K
        a5_weight_cost = 4.5 * 1516.82
    else:
        a5_weight_cost = 4.5 * 1516.82 * math.ceil(a5_equip_weight/150000)
    a5_cost = a5_crews * a5_duration * a5_working_hours * a5_hourly_cost
    a5_stop = a5_start + datetime.timedelta(a5_duration)
    a5 = gantt.Task(name='a5_install_girders',
                    start=a5_start,
                    stop=None,
                    duration=a5_duration,
                    percent_done=None,
                    resources=None,
                    color="#FF8080",
                    depends_of=a4)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   # Total duration estimation
    work_duration = (a5_start + datetime.timedelta(a5_duration) - a1_start).days
    working_days = a1_duration + a2_duration + a3_duration + a4_duration + a5_duration
    idle_time = work_duration - working_days
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Add time-windows to schedule
    time_windows = gantt.Project(name='Time windows')
    time_windows.add_task(tw1)
    time_windows.add_task(tw2)
    time_windows.add_task(tw3)
    # Add activities to schedule
    bridge_side_1 = gantt.Project(name='Bridge side 1')
    bridge_side_1.add_task(a1)
    bridge_side_1.add_task(a2)
    bridge_side_1.add_task(a3)
    bridge_side_1.add_task(a4)
    bridge_side_1.add_task(a5)
    # Create schedule
    schedule = gantt.Project(name='Mobile cranes method')
    schedule.add_task(time_windows)
    schedule.add_task(bridge_side_1)
    # Draw schedule
    # schedule.make_svg_for_tasks(filename='run ' + str(run+1) + '.svg',
    #                             today=None,
    #                             start=datetime.date(2022, 12, 1),
    #                             end=datetime.date(2024, 4, 1),
    #                             scale=gantt.DRAW_WITH_DAILY_SCALE)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    a2_option_list.append(a2_x)
    a2_duration_list.append(a2_duration)
    a2_cost_list.append(a2_cost)
    a2_ppl_list.append(a2_ppl)
    a2_weight_list.append(a2_equip_weight)
    a3_option_list.append(a3_x)
    a3_duration_list.append(a3_duration)
    a3_cost_list.append(a3_cost)
    a3_ppl_list.append(a3_ppl)
    a3_weight_list.append(a3_equip_weight)
    a4_option_list.append(a4_x)
    a4_duration_list.append(a4_duration)
    a4_cost_list.append(a4_cost)
    a4_ppl_list.append(a4_ppl)
    a4_weight_list.append(a4_equip_weight)
    a5_option_list.append(a5_x)
    a5_duration_list.append(a5_duration)
    a5_cost_list.append(a5_cost)
    a5_ppl_list.append(a5_ppl)
    a5_weight_list.append(a5_equip_weight)
    idle_time_list.append(idle_time)
    work_duration_list.append(work_duration)
    mobilize_cost.append(a2_weight_cost + a3_weight_cost + a4_weight_cost + a5_weight_cost)
    run = run + 1
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Cost of temporary facilities and flight tickets to fly workers in and out
    if max(a2_ppl, a3_ppl, a4_ppl, a5_ppl) <= 9: # 9 man bunk house trailer $42,900 to buy (p. 17 line 015213.200910)
        ppl_cost.append(42900 + (a2_ppl + a3_ppl + a4_ppl + a5_ppl) * 21600) # $1080 one way ticket from Yellowknife to Tulita
    else: # 18 man bunk house trailer $55,000 to buy
        ppl_cost.append(math.ceil(max(a2_ppl, a3_ppl, a4_ppl, a5_ppl)/18) * 55000 + (a2_ppl + a3_ppl + a4_ppl + a5_ppl) * 2160)
    # Cost of moving equipment from Hay River to Tulita by Winter road (max speed - 50km/hr)
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
list = list(zip(a2_option_list, a2_duration_list, a2_cost_list, a2_ppl_list, a2_weight_list, a3_option_list, a3_duration_list, a3_cost_list, a3_ppl_list,
                a3_weight_list, a4_option_list, a4_duration_list, a4_cost_list, a4_ppl_list, a4_weight_list, a5_option_list, a5_duration_list, a5_cost_list,
                a5_ppl_list, a5_weight_list, work_duration_list, idle_time_list, ppl_cost, mobilize_cost))
df = pd.DataFrame(list, columns=["a2_berm", "a2_t", "a2_$", "a2_ppl", "a2_weight", "a3_piles", "a3_t", "a3_$", "a3_ppl", "a3_weight", "a4_piers", "a4_t",
                                 "a4_$", "a4_ppl", "a4_weight", "a5_girders", "a5_t", "a5_$", "a5_ppl", "a5_weight", "total_t", "idle_t", "ppl_$", "mobilize_$"])

df["total_$"] = df["a2_$"] + df["a3_$"] + df["a4_$"] + df["a5_$"] + df["ppl_$"] + df["mobilize_$"]
cost_a = -0.5
cost_b = 0.5
df["total_$_norm"] = cost_a + ((df["total_$"] - df["total_$"].min()) * (cost_b - cost_a))/(df["total_$"].max()-df["total_$"].min())
time_a = -1 - cost_a
time_b = 1 - cost_b
df["total_t_norm"] = time_a + ((df["total_t"] - df["total_t"].min()) * (time_b - time_a))/(df["total_t"].max()-df["total_t"].min())
df["reward"] = df["total_$_norm"] + df["total_t_norm"]

print(df.to_string())
print('Total unique cost scenarious =', df.nunique()["reward"])
##


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
df_a2_0 = df.loc[df["a2_berm"] == 0, ["a2_t", "a2_$", "total_t", "total_$"]]
a2_0_time = df_a2_0["total_t"].mean()
a2_0_cost = df_a2_0["total_$"].mean()
df_a2_1 = df.loc[df["a2_berm"] == 1, ["a2_t", "a2_$", "total_t", "total_$"]]
a2_1_time = df_a2_1["total_t"].mean()
a2_1_cost = df_a2_1["total_$"].mean()
df_a2_2 = df.loc[df["a2_berm"] == 2, ["a2_t", "a2_$", "total_t", "total_$"]]
a2_2_time = df_a2_2["total_t"].mean()
a2_2_cost = df_a2_2["total_$"].mean()
print(a2_0_time)
print(a2_0_cost)
print(a2_1_time)
print(a2_1_cost)
print(a2_2_time)
print(a2_2_cost)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#print(df.sort_values("a2_berm").to_string())



