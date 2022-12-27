import numpy as np
import scipy
import numpy as np
import matplotlib.pyplot as plt
file = open("shtuka.dat", "r")
file_with_lines = file.readlines()[1:267]

allall = []
for line in file_with_lines:
    a = line.split("   ")
    f_st = line.split("   ")[:1]
    t_st = line.split("    ")[1:2]
    tt_st = line.split("    ")[2:3]
    v_st = line.split("    ")[3:4]
    allall.append(f_st+t_st+tt_st+v_st)
    name = []
    lume = []
    date_hjd = []
    for j in range(0, len(allall)):  #тут я крошу созданный список списков allall на списки
        name.append(allall[j][0])    #с названиями объектов (но там еще и фильтры, я думал, что это меня спасёт),
        name.append(allall[j][2])    #звездной величиной (я думал,
        lume.append(allall[j][3])    #что это светимость, Серега сказал, что это lume...) и датой.
        date_hjd.append(allall[j][1])
name = [_.replace("su hor", "SU_Hor") for _ in name]  #танцы с бубнами ради того, чтобы все su hor, SU Hor и прочие нечисти стали SU_Hor
name = [_.replace("SU Hor", "SU_Hor") for _ in name]
name = [_.replace("RZ Lyr", "RZ_Lyr") for _ in name]
name = [_.replace("rzlyr", "RZ_Lyr") for _ in name]
name = [_.replace("RZLyr", "RZ_Lyr") for _ in name]
name = [_.replace("b", "B") for _ in name]
name = [_.replace("v", "V") for _ in name]
name = [x.strip(" ") for x in name] #удалил пробелы из списка name
lume = [x.strip(" ") for x in lume]
lume = [x.strip("\n") for x in lume]
date_hjd = [x.strip(" ") for x in date_hjd]
Obj = []
for j in range(0, len(name)):   #делаю список с объектами
    if (j+1)%2 == 1:
        Obj.append(name[j])

filt_SU_Hor = []
for i in range(0, len(name)): #делаем список из фильтров для SU_Hor
    if i%2 == 1 and name[i-1] == name[0]:
        filt_SU_Hor.append(name[i])

filt_RZ_Lyr = []
for i in range(0, len(name)): #делаем список из фильтров для RZ_Lyr
    if i%2 == 1 and name[i-1] == name[462]:
        filt_RZ_Lyr.append(name[i])

filt = []                      #список всех фильтров
for i in range(0, len(name)):
    if i%2 == 1:
        filt.append(name[i])

from collections import OrderedDict #убираем дубли, трибли, и тд
OBJ = list(OrderedDict.fromkeys(Obj))

f_SU = list(OrderedDict.fromkeys(filt_SU_Hor))

f_RZ = list(OrderedDict.fromkeys(filt_RZ_Lyr))

print(f"\n \t Объекты: {OBJ} \n \t Фильтры для SU_Hor: {f_SU} \n \t Фильтры для RZ_Lyr: {f_RZ} ")

HJD_SU_Hor_B = []                       #выделяем из списка только даты для SU_Hor и B, а потом зв величину для них же
lume_S_B =[]
for i in range(0, len(allall)):
    if Obj[i] == OBJ[0] and filt_SU_Hor[i] == f_SU[0]:
        HJD_SU_Hor_B.append(allall[i][1])
        lume_S_B.append(lume[i])
HJD_SU_Hor_Ic = []
lume_S_Ic = []
for i in range(0, len(allall)):
    if Obj[i] == OBJ[0] and filt_SU_Hor[i] == f_SU[1]:
        HJD_SU_Hor_Ic.append(allall[i][1])
        lume_S_Ic.append(lume[i])
HJD_SU_Hor_V = []
lume_S_V = []
for i in range(0, len(allall)):
    if Obj[i] == OBJ[0] and filt_SU_Hor[i] == f_SU[2]:
        HJD_SU_Hor_V.append(allall[i][1])
        lume_S_V.append(lume[i])
HJD_RZ_Lyr_B = []
lume_R_B = []
for i in range(0, len(allall)):
    if Obj[i] == OBJ[1] and filt[i] == f_RZ[0]:
        HJD_RZ_Lyr_B.append(allall[i][1])
        lume_R_B.append(lume[i])
HJD_RZ_Lyr_V = []
lume_R_V = []
for i in range(0, len(filt)):
    if Obj[i] == OBJ[1] and filt[i] == f_RZ[1]:
        HJD_RZ_Lyr_V.append(allall[i][1])
        lume_R_V.append(lume[i])
list_HJD_SU = []
list_HJD_SU.extend([HJD_SU_Hor_B, HJD_SU_Hor_Ic, HJD_SU_Hor_V])
list_lume_SU = []
list_lume_SU.extend([lume_S_B, lume_S_Ic, lume_S_V])
list_HJD_RZ = []
list_HJD_RZ.extend([HJD_RZ_Lyr_B, HJD_RZ_Lyr_V])
list_lume_RZ = []
list_lume_RZ.extend([lume_R_B, lume_R_V])
i_obj = input("Введите название объекта:" )
i_filt = input("Введите названия фильтров через запятую:" )
i_f = i_filt.split(",")

for i in range (0, len(date_hjd)): #подписываем 24..
    d = float(date_hjd[i])
    d += 2400000
    date_hjd[i] = str(d)

date_g = []
for i in range (0, len(date_hjd)):
    hjd = float(date_hjd[i]) + 0.5
    jd = int(hjd)
    dt = hjd - jd
    a = jd + 32044           #религиозная википедия говорит использовать такие букавки,чиселки и формулы
    b = (4*a + 3) // 146097
    c = a - (146097*b // 4)
    d = (4*c + 3)//1461
    e = c - (1461*d)//4
    m = (5*e + 2)//153
    day = e - (153*m + 2)//5 + 1
    month = m + 3 - 12 * (m//10)
    year = 100*b + d - 4800 + (m//10)

    h = dt*24
    mins = (h-int(h))*60
    sec = (mins-int(mins))*60
    g_date = f'{day}.{month}.{year} {int(h)}:{int(mins)}:{int(sec)}'
    date_g.append(g_date)

new_file = open(f'{i_obj}.dat', 'w')
inpfilt = i_filt.split(",")
filt0, filt1, filt2 = None, None, None
if len(inpfilt) == 1:
    filt0 = i_filt
    new_file.write(f"Date\t\t\t\t HJD\t\t\t Magn in {filt0}\n")
elif len(inpfilt) == 2:
    filt0, filt1 = inpfilt[0], inpfilt[1]
    new_file.write(f"Date\t\t\t\t HJD\t\t\t Magn in {filt0}\t Magn in {filt1}\n")
elif len(inpfilt) == 3:
    filt0, filt1, filt2 = inpfilt[0], inpfilt[1], inpfilt[2]
    new_file.write(f"Date\t\t\t\t HJD\t\t\t Magn in {filt0}\t Magn in {filt1}\t Magn in {filt2}\n")

lume0, lume1, lume2, Hjd, data = [], [], [], [], []
for i in range(0, len(allall)):
    if Obj[i] == str(i_obj):
        if filt[i] == filt0:
            Hjd.append(date_hjd[i])
            lume0.append(lume[i])
            data.append(date_g[i])
            lume1.append(f'\t\t')
            lume2.append(f'\t\t')
        elif filt[i] == filt1:
            Hjd.append(date_hjd[i])
            lume0.append(f'\t\t')
            data.append(date_g[i])
            lume1.append(lume[i])
            lume2.append(f'\t\t')
        elif filt[i] == filt2:
            Hjd.append(date_hjd[i])
            lume0.append(f'\t\t')
            data.append(date_g[i])
            lume1.append(f'\t\t')
            lume2.append(lume[i])

for k in range(0, len(Hjd)):
    min_Hjd = min(Hjd)
    ind = Hjd.index(min_Hjd)
    new_file.write(f"{data[ind]}\t {min_Hjd}\t {lume0[ind]}\t {lume1[ind]}\t {lume2[ind]}\n")
    del Hjd[ind], data[ind], lume0[ind], lume1[ind], lume2[ind]

new_file.close()

new_file = open(f'{i_obj}.dat', 'r')
file_with_lines2 = new_file.readlines()

for_grx = []
for_gry = []
for line in file_with_lines2:
    ox = line.split(" ")[2:3]
    oy = line.split(" ")[3:4]
    ox = [x.strip(" \t") for x in ox]
    oy = [x.strip(" \t") for x in oy]

    for_grx.append(float(ox[0]))
    for_gry.append(oy[0])

del for_grx[0], for_gry[0]

fig = plt.figure()
ax = fig.add_subplot(111)
fig.set_facecolor('green')
ax.set(facecolor='white')
ax.set_title("График 1")
ax.set_xlabel('Дата, HJD')
ax.set_ylabel('Звездная величина')
# ax.set_xlim([2455896, 2455907])
# ax.set_ylim([13, 15])
# plt.show()
## Настроим заголовок
ax.title.set_color('white')  # снова используем set
ax.title.set_size(20)

ax.plot(for_grx, for_gry)
plt.show()
print(for_grx)
print(for_gry)
print("mm")