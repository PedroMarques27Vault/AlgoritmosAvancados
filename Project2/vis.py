import random
import matplotlib.pyplot as plt
import os, re
from counter import load_fixed, load_csuros, load_exact
from CsurosCounterState import CsurosCounterState


def open_stats(filename,_type = 'FPEX'):
    f = open(f'results/{filename}','r')
    _chars = f.readline().replace("\n","").split(',')
    if _type == 'CS':
        data = {k:None for k in _chars}
        mean_values = f.readline().replace("\n","").split('),(')
        for i in range(len(_chars)) :
            string = re.sub("[()]","", mean_values[i]).split(',')

            _cs = CsurosCounterState(8, round(float(string[0]),2),round(float(string[1])),round(float(string[2])) )
            data[_chars[i]] = _cs
    else:

        mean_values = f.readline().replace("\n","").split(',')
        data = {_chars[i]:round(float(mean_values[i]),2) for i in range(len(_chars))}



    f.readline()
    line = f.readline().replace("\n","").split("),(")
    print(line)
    min_e, max_e,mean_e  = [],[],[]
    for _ in line:
        string = re.sub("[()]", "", _).split(',')
        min_e.append(round(float(string[0]),2))
        max_e.append(round(float(string[1]),2))
        mean_e.append(round(float(string[2]),2))

    return min_e,max_e,mean_e,_chars, data


arr = []



for i in ['En','Fr','Ge','Ne']:
    files = [f'OliverTwist{i}CSStatistics.csv']

    min_e,max_e,mean_e,keys, cs = open_stats(files[0],'CS')

    plt.plot(keys, min_e, label = 'Min Error', color = 'blue')
    plt.plot(keys, mean_e, label = 'Mean Error', color = 'green')
    plt.plot(keys, max_e, label = 'Max Error', color = 'red')

    plt.legend(loc='upper right',fontsize=12)

    plt.xlabel('Alphabet')

    plt.ylabel('Error (%)')
    plt.title(f'{i} Estimated Csurös Counter Value Error, avg_error {round(sum(mean_e)/len(mean_e),2)}%')
    plt.savefig(f'{i}ErrorPredictCs.png')
    plt.show()

