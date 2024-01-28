import datetime
import gantt
gantt.define_not_worked_days([])  # list_of_days -- list of integer (0: Monday ... 6: Sunday) - default [5, 6]
# Change font default
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")
# Create some tasks
# t11 = gantt.Task(name='Course Work',
#                 start=datetime.date(2020, 9, 1),
#                 duration=4,
#                 percent_done=100,
#                 resources=[rANO],
#                 color="#FF8080")
# Resources
Dr_Lu = gantt.Resource('Dr_Lu')
Dr_Hamzeh = gantt.Resource('Dr_Hamzeh')
Dr_Braun = gantt.Resource('Dr_Braun')
Dr_Gonzalez = gantt.Resource('Dr_Gonzalez')
Dr_Mohsen = gantt.Resource('Dr_Mohsen')

TA = gantt.Project(name='TA work')
t1_1 = gantt.Task(name='CIVE_406_2020',
                start=datetime.date(2020, 9, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t1_2 = gantt.Task(name='CIVE_607_2021',
                start=datetime.date(2021, 1, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t2_1 = gantt.Task(name='CIVE_406_2021',
                start=datetime.date(2021, 9, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t2_2 = gantt.Task(name='CIVE_607_2022',
                start=datetime.date(2022, 1, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t3_1 = gantt.Task(name='CIVE_406_2022',
                start=datetime.date(2022, 9, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t3_2 = gantt.Task(name='CIVE_607_2023',
                start=datetime.date(2023, 1, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t3_3 = gantt.Task(name='CIVE_240_2023',
                start=datetime.date(2023, 1, 1),
                duration=120,
                resources=[Dr_Braun],
                color="#FF8080")
t3_4 = gantt.Task(name='CIVE_601_2022',
                start=datetime.date(2022, 9, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#FF8080")
t4_1 = gantt.Task(name='CIVE_406_2023',
                start=datetime.date(2023, 9, 1),
                duration=120,
                resources=[Dr_Lu,Dr_Gonzalez],
                color="#FF8080")
t4_2 = gantt.Task(name='CIVE_789_2023',
                start=datetime.date(2023, 9, 1),
                duration=120,
                resources=[Dr_Braun],
                color="#FF8080")
t4_3 = gantt.Task(name='CIVE_409_2024',
                start=datetime.date(2024, 1, 1),
                duration=120,
                resources=[Dr_Lu,Dr_Gonzalez],
                color="#FF8080")
t4_4 = gantt.Task(name='CIVE_240_2024',
                start=datetime.date(2024, 1, 1),
                duration=120,
                resources=[Dr_Braun],
                color="#FF8080")
TA.add_task(t1_1)
TA.add_task(t1_2)
TA.add_task(t2_1)
TA.add_task(t2_2)
TA.add_task(t3_1)
TA.add_task(t3_4)
TA.add_task(t3_2)
TA.add_task(t3_3)
TA.add_task(t4_1)
TA.add_task(t4_2)
TA.add_task(t4_3)
TA.add_task(t4_4)
Course = gantt.Project(name='Course work')
c1 = gantt.Task(name='CIVE_709_Lean',
                start=datetime.date(2023, 1, 1),
                duration=120,
                resources=[Dr_Hamzeh],
                color="#3498DB")
c2 = gantt.Task(name='CIVE_789_Rhetoric',
                start=datetime.date(2023, 1, 1),
                duration=120,
                resources=[Dr_Braun],
                color="#3498DB")
c3 = gantt.Task(name='CIVE_709_Special',
                start=datetime.date(2023, 5, 1),
                duration=120,
                resources=[Dr_Lu],
                color="#3498DB")
Course.add_task(c1)
Course.add_task(c2)
Course.add_task(c3)

Research = gantt.Project(name='Research work')
r1 = gantt.Task(name='Time-Windows planning method',
                start=datetime.date(2020, 9, 1),
                stop=datetime.date(2022, 9, 20),
                resources=[Dr_Lu],
                color="#2ECC71")
r2 = gantt.Task(name='Time-Windows cost optimization and reward function',
                start=datetime.date(2022, 9, 20),
                stop=datetime.date(2024, 12, 31),
                depends_of=r1,
                resources=[Dr_Lu],
                color="#2ECC71")
r3 = gantt.Task(name='Lean curriculum simulation in civil engineering',
                start=datetime.date(2021, 1, 1),
                stop=datetime.date(2022, 5, 15),
                resources=[Dr_Hamzeh,Dr_Mohsen],
                color="#2ECC71")


ms1 = gantt.Milestone(name='Written Candidacy', depends_of=None, start=datetime.date(2021, 6, 1))
ms2 = gantt.Milestone(name='Oral Candidacy', depends_of=None, start=datetime.date(2024, 2, 1))
ms3 = gantt.Milestone(name='Journal paper published (Naumets et al. 2022)', depends_of=r1)
ms4 = gantt.Milestone(name='IGLC conference (Mohsen et al. 2022)', depends_of=r3)
ms5 = gantt.Milestone(name='NSERC Doctoral Scholarship', start=datetime.date(2022, 4, 23))
ms6 = gantt.Milestone(name='Journal paper to be submitted to Aut. in Constr.', start=datetime.date(2024, 3, 1), depends_of=ms2, color="#F5B7B1")
ms7 = gantt.Milestone(name='Conference paper to be submitted to Winter. Sim.', start=datetime.date(2024, 7, 1), depends_of=ms6, color="#F5B7B1")
ms8 = gantt.Milestone(name='PhD defence', start=datetime.date(2025, 3, 15), depends_of=[ms7,r2], color="#F5B7B1")
ms9 = gantt.Milestone(name='Alberta Innovates Graduate Scholarship', start=datetime.date(2024, 1, 15))

Research.add_task(r1)
Research.add_task(ms3)
Research.add_task(r2)
Research.add_task(ms6)
Research.add_task(ms7)
Research.add_task(r3)
Research.add_task(ms4)

PhD = gantt.Project(name='PhD')
PhD.add_task(ms1)
PhD.add_task(ms5)
PhD.add_task(ms9)
PhD.add_task(ms2)
PhD.add_task(ms8)
PhD.add_task(Research)
PhD.add_task(TA)
PhD.add_task(Course)
PhD.make_svg_for_tasks(filename='Time_table.svg',
                      today=datetime.date(2024, 2, 1),
                      start=datetime.date(2020, 8, 1),
                      end=datetime.date(2025, 5, 1),
                      scale=gantt.DRAW_WITH_MONTHLY_SCALE)