import matplotlib.pyplot as plt
import json
import numpy as np
import os
import pandas as pd
import itertools
import ROOT
from ROOT import TFile

color_cycle = itertools.cycle('grcmyk')

times = {}
names = {}
times_real={}

P = os.getcwd()
#print(P)
P=P + "/"
files = os.listdir(P)
files = [f for f in files if os.path.isfile(P+f) and f.endswith("json")]

#print(P)
#print(files)
'''files=open("/home/umit/Desktop/hackathon_gnn/cpu.json","r")

#print(files.read())
#files.close()'''

for thisfile in files:

    with open(P+thisfile) as f:
        timing = json.load(f)
        f.close()
    print("\nJSON file opened.\n")
    F = thisfile       
    TYPE = thisfile[:-5] #using filename as key for the dict
    
    # json keys
#    print(timing.keys())
    # module keys == metrics
#    print("metrics:")
#    print(timing["modules"][0].keys())
    
    times[TYPE] = []
    names[TYPE] = []
    times_real[TYPE]=[]
    
    E = timing["modules"][0]["events"]
   
#    print("Num events %d"%E)
    skip=True
    for f in timing["modules"]:

        times[TYPE].append(f["time_thread"]/E)
        times_real[TYPE].append(f["time_real"]/E)
        names[TYPE].append(f["label"])

#print(times["cpu"])
#print(type(times))
degerliste=times["cpu"]
#print("\n\n")
#print(names["cpu"])
anahtarliste=names["cpu"]
#print(type(anahtarliste))
#print(anahtarliste)
#print("\n\n")
#print(times_real["cpu"])
degerrealliste=times_real["cpu"]
#print(type(degerrealliste))
#print(degerrealliste)

_dict={}
for m in anahtarliste:
    for n in degerliste:
        _dict[m]=n
        degerliste.remove(n)
        break
_dict_real={}
for m in anahtarliste:
    for n in degerrealliste:
        _dict_real[m]=n
        degerrealliste.remove(n)
        break
        
print("\tDrawing process started...")

umit=_dict.items()
umit=sorted(umit)
y,x=zip(*umit)

x_series=pd.Series(x)
plt.figure(figsize=(30,60))
ax=x_series.plot(kind='barh')
ax.set_xlabel("Time (s)")
ax.set_title("Label vs Time")
ax.set_yticklabels(y)
colors = ["blue" if i < 1 else "red" for i in x]

rects=ax.patches
for rect in rects:
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2
    space=5
    ha='left'
    if x_value<0:
        space *=-1
        ha='right'
    label="{:.1f}".format(x_value)
    plt.annotate(label,(x_value,y_value),xytext=(space,0),textcoords="offset points",va='center',ha=ha)

plt.axvline(1, color = 'magenta', linestyle = '-')
plt.barh(y,x, color=colors)
plt.xscale("log")
print("\tThe drawing is successful for Label vs Time_Thread!")
#plt.show()
plt.savefig('plots/Label_vs_Time_Thread.pdf')
print("\n\tThe PDF version of the file has been saved.")
plt.savefig('plots/Label_vs_Time_Thread.png')
print("\n\tThe PNG version of the file has been saved.\n")
#plt.savefig('Label_vs_Time.jpeg')
#print("\n\tThe JPEG version of the file has been saved.\n")

print("#####################################################\n")

umitreal=_dict_real.items()
umitreal=sorted(umitreal)
y,x=zip(*umitreal) 

x_series=pd.Series(x)
plt.figure(figsize=(30,60))
ax=x_series.plot(kind='barh')
ax.set_xlabel("Time (s)")
ax.set_title("Label vs Time_Real")
ax.set_yticklabels(y)
colors = ["blue" if i < 1 else "red" for i in x]

rects=ax.patches
for rect in rects:
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2
    space=5
    ha='left'
    if x_value<0:
        space *=-1
        ha='right'
    label="{:.1f}".format(x_value)
    plt.annotate(label,(x_value,y_value),xytext=(space,0),textcoords="offset points",va='center',ha=ha)

plt.axvline(1, color = 'magenta', linestyle = '-')
plt.barh(y,x, color=colors)
plt.xscale("log")
print("\tThe drawing is successful for Label vs Time_Real!")
#plt.show()
plt.savefig('plots/Label_vs_Time_Real.pdf')
print("\n\tThe PDF version of the file has been saved.")
plt.savefig('plots/Label_vs_Time_Real.png')
print("\n\tThe PNG version of the file has been saved.\n\n")
#plt.savefig('Label_vs_Time_Real.jpeg')
#print("\n\tThe JPEG version of the file has been saved.\n\n")

rootfile = TFile.Open("DQM_V0001_R000000001__HLT__FastTimerService__All.root")
#print("Root file opened-checked")

DIR = rootfile.Get("DQMData/Run 1;1/HLT;1/")
DIR = DIR.Get("HLT;1/Run summary;1/")
DIR = DIR.Get("Run summary;1/TimerService;1/")
DIR.Get("TimerService;1").ls()
