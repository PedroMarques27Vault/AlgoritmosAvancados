import math
import sys
import time
import os, re ,string
import random
import pandas as pd
from CsurosCounterState import CsurosCounterState


#Counter value X =2**d × t + u is used to estimate the actual count
#Estimate is (M + u) × 2**t – M
def main():

    args = sys.argv[1:]
    if len(args)!=3:
        raise Exception('Not Enoguh Arguments, run with arguments d, fraction_fixed_probability and number_of_trials\nExample: python3 counter.py 4 1/32 1000')
    prob = float(args[1].split('/')[0])/float(args[1].split('/')[1])

    d = int(args[0])
    n_trials = int(args[2])


   
    text_files = [f for f in os.listdir('text') if f.endswith('.txt')]

    for _file in text_files:
        data = read_file(_file)
        _chars = sorted(set(data))



        
        t= time.time()
        ex = exact_counter(data)
        _t = time.time()-t
        write_results_to_file(_chars, [ex], f'{_file[:-4]}ExactCount',1,_t)
        print('Finished Exact, Starting FP')

        t = time.time()
        calc = [fixed_counter(data, prob = prob) for _ in range(n_trials)]
        _t = time.time()-t
        write_results_to_file(_chars, calc, f'{_file[:-4]}FixedProbability',  n_trials,_t/n_trials)
        

        print('Finished FP, Starting Csuros')
        t = time.time()
        calc = [csuros_counter(data, d= d) for i in range(n_trials)]
        _t = time.time()-t
        write_results_to_file(_chars, calc, f'{_file[:-4]}CsurosCounter', n_trials, _t/n_trials)
        

        exact, fixed, csuros = load_data(lang = _file[11:-4])

        mean_values = mean_val(fixed, 'FP')
        _devs = deviations(mean_values, fixed, 'FP')
        est_erros = estimation_error(exact,fixed, prob, 'FP')
        est_real = estimation_real_val_error(exact,fixed,prob,'FP')
        write_statistics_to_files(mean_values,_devs,est_erros, est_real,f'{_file[:-4]}FP')

        mean_values = mean_val(csuros, 'CS')
        _devs = deviations(mean_values, csuros, 'CS')
        est_erros = estimation_error(exact,csuros, prob = d,_type = 'CS')
        est_real = estimation_real_val_error(exact,csuros,d,'CS')
        write_statistics_to_files(mean_values,_devs,est_erros, est_real,f'{_file[:-4]}CS')
        print('Finished '+_file)

def write_statistics_to_files(mean_values, _devs, est_erros, est_real, _type = 'FP'):
    open(f'results/{_type}Statistics.csv','w')
    f = open(f'results/{_type}Statistics.csv','a+', encoding='utf-8')
    _chars = mean_values.keys()
    f.write(f'{",".join(_chars)}')
    f.write(f'{",".join([str(mean_values[_char]) for _char in _chars ])}\n')
    f.write(f'{",".join([str(_devs[_char]) for _char in _chars ])}\n')
    f.write(f'{",".join([str(est_erros[_char]) for _char in _chars ])}\n')
    f.write(f'{",".join([str(est_real[_char]) for _char in _chars ])}\n')


def estimation_error(exact_values,calc_values,prob=1/32,_type = 'FP'):
    #_char: min, max, mean
    est_values = dict()
    if _type == 'FP':
        for _char in exact_values:
            est = exact_values[_char]*prob
            errors = [(abs(calc[_char]-est)/est)*100 for calc in calc_values]
            est_values[_char] = (min(errors),max(errors), sum(errors)/len(errors))
    else:
        for _char in exact_values:
            errors = [(abs(calc[_char].x-calc_values[0][_char].estimate_x(d=prob))/calc_values[0][_char].estimate_x(d=prob))*100 for calc in calc_values]
            est_values[_char] = (min(errors),max(errors), sum(errors)/len(errors))
    return est_values

def estimation_real_val_error(exact_values,calc_values,prob=1/32,_type = 'FP'):
    #_char: min, max, mean
    est_values = dict()
    if _type == 'FP':
        for _char in exact_values:
            est = exact_values[_char]
            errors = [(abs(calc[_char]*(prob**-1)-est)/est)*100 for calc in calc_values]
            est_values[_char] = (min(errors),max(errors), sum(errors)/len(errors))
    else:
        for _char in exact_values:
            errors = [(abs(calc[_char].estimate_real(d = prob)-exact_values[_char])/exact_values[_char])*100 for calc in calc_values]
            est_values[_char] = (min(errors),max(errors), sum(errors)/len(errors))
    return est_values
def deviations(mean_values, calc_values,_type = 'FP'):
    #_char: min, max, mad, standard
    dev_values = dict()
    if _type == 'FP':
        for _char in mean_values:
            diffs = [(calc[_char]-mean_values[_char]) for calc in calc_values]
            abs_diffs = [abs(x) for x in diffs]
            std_dev = math.sqrt(sum([x**2 for x in diffs])/len(diffs))
            dev_values[_char] = (min(abs_diffs),max(abs_diffs), sum(abs_diffs)/len(abs_diffs),std_dev)
    else:
        for _char in mean_values:
            diffs = [(calc[_char].x-mean_values[_char][0]) for calc in calc_values]
            abs_diffs = [abs(x) for x in diffs]
            std_dev = math.sqrt(sum([x**2 for x in diffs])/len(diffs))
            dev_values[_char] = (min(abs_diffs),max(abs_diffs), sum(abs_diffs)/len(abs_diffs),std_dev)
    return dev_values

def load_data(lang = 'En'):
    files = os.listdir(os.getcwd()+'/results')
    ex = load_exact([('results/'+fname) for fname in files if  lang+'Exact' in fname][0])
    fixed = load_fixed([('results/'+fname) for fname in files if  lang+'Fixed' in fname][0])
    csuros = load_csuros([('results/'+fname) for fname in files if  lang+'Csuros' in fname][0])
    return ex, fixed, csuros

def load_exact(filename):
    f = open(filename,'r', encoding='utf-8')
    keys = f.readline().split(',')
    values = f.readline().split(',')
    return {keys[i]:int(values[i]) for i in range(len(keys))}

def load_fixed(filename):
    f = open(filename, 'r', encoding='utf-8')
    keys = f.readline().split(',')
    final_list = []
    for row in f.readlines()[1:]:
        values = row.split(',')
        final_list.append({keys[i]:int(values[i]) for i in range(len(keys))})
    return final_list

def load_csuros(filename):
    f = open(filename, 'r', encoding='utf-8')
    keys = f.readline().split(',')
    final_list = []
    for row in f.readlines()[1:]:
        values =re.sub("[()]", "", row)
        data = values.split(',')
        data_arr = []
        [data_arr.append(CsurosCounterState(int(x.split(':')[0]),int(x.split(':')[1]), int(x.split(':')[2]),int(x.split(':')[3]))) for x in data]
        final_list.append({keys[i]:data_arr[i] for i in range(len(keys))})
    return final_list

def write_results_to_file(_chars, calculated, counter = 'Fixed', n=1,avg_time = 0.0):
    open(f'results/{n}{counter}Results{round(avg_time,3)}.csv','w', encoding='utf-8')
    f = open(f'results/{n}{counter}Results{round(avg_time,3)}.csv','a+', encoding='utf-8')
    char_list = [k for k in _chars]

    f.write(f"{','.join(char_list)}\n")
    for row in calculated:
        f.write(f"{','.join([str(row[k]) for k in char_list])}\n")

def csuros_counter(data, d):
    counter = {k: CsurosCounterState(d) for k in sorted(set(data))}
    #Return [Value]
    for _char in sorted(data):
        counter[_char] = csuros_incrementer(counter[_char],d)
    return counter

def csuros_incrementer(cs_counter,d):
    t = math.floor(cs_counter.x/(2**d))
    cs_counter.t = t
    cs_counter.increment_u()
    while t>0:
        if random.randint(0,1) == 1:
            return cs_counter
        t-=1
    return cs_counter.increment()

def exact_counter(data):
    counter = {k:0 for k in sorted(set(data))}
    for _char in sorted(data):
        counter[_char]+=1
    return counter
def fixed_counter(data, prob= 1/32):
    counter = {k: 0 for k in sorted(set(data))}
    #Return [Value]
    for _char in sorted(data):
        if random.random()<prob:
            counter[_char] += 1
    return counter

def mean_val(array_of_results, _type ='FP'):
    k = len(array_of_results)
    _chars = [k for k in array_of_results[0]]
    mean_dic = dict()
    if _type != 'FP':
        for _char in _chars:
            mean_dic[_char] =(sum([i[_char].x for i in array_of_results])/k,round( sum([i[_char].t for i in array_of_results])/k), sum([i[_char].u for i in array_of_results])/k)
    else:
        for _char in _chars:
            mean_dic[_char] =sum([x[_char] for x in array_of_results])/k
    return mean_dic


def variance(ex, calc, n_observations = 1000):
    #sum(xi - x:mean)square/n_observations-1
    variance = {k:0 for k in ex}
    for _char in ex:
        mean= (sum([x[_char] for x in calc])/n_observations)
        summation = sum([(x[_char] - mean)**2 for x in calc])
        variance[_char] = round(summation/(n_observations-1),2)
    return variance

def estimations(ex, prob=1/32):
    #sum(xi - x:meansquare)/n_observations-1
    est = {k:0 for k in ex}
    for _char in ex:
        est[_char] = ex[_char]*prob
    return est

def standard_deviation(ex,p=1/32):
    deviation = {k: 0 for k in ex}
    for _char in ex:
        deviation[_char] = math.sqrt(ex[_char]*p*(1-p))
    return deviation

def read_file(filename):

    f = open(f'text/{filename}', 'r', encoding='utf-8')
    data = f.read().upper()
    return re.sub(r'[^a-zA-Z]', '', data)




if __name__ == "__main__":
    main()