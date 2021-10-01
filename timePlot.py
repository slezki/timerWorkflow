import matplotlib.pyplot as plt
import json
import numpy as np
import os
import pandas as pd
import itertools
#import ROOT
#from ROOT import TFile

color_cycle = itertools.cycle('grcmyk')

times = {}
names = {}
times_real={}

P = os.getcwd()
#print(P)
P=P + "/"
files = os.listdir(P)
files = [f for f in files if os.path.isfile(P+f) and f.endswith("json")]

S=P+"JSON/"
compfiles = os.listdir(S)
compfiles = [f for f in compfiles if os.path.isfile(S+f) and f.endswith("json")]

for thisfile in files:

    with open(P+thisfile) as f:
        timing = json.load(f)
        f.close()
    print("\nJSON file opened.\n")
    F = thisfile       
    TYPE = thisfile[:-5] #using filename as key for the dict
    
   
    times[TYPE] = []
    names[TYPE] = []
    times_real[TYPE]=[]
    
    E = timing["modules"][0]["events"]
   
    skip=True
    for f in timing["modules"]:

        times[TYPE].append(f["time_thread"]/E)
        times_real[TYPE].append(f["time_real"]/E)
        names[TYPE].append(f["label"])


for compthisfile in compfiles:

    with open(S+compthisfile) as f:
        comptiming = json.load(f)
        f.close()
    D = compthisfile       
    TYPE = compthisfile[:-5] #using filename as key for the dict
    
    compKeys=comptiming.keys()
#    print(compKeys)
#    print(type(compKeys))

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
compAnahtar=list(compKeys)
#print(len(compAnahtar))

sozluk={}
for i in anahtarliste:
    if i in compAnahtar:
        for n in degerliste:
            sozluk[i]=n
            degerliste.remove(n)
            break

sozlukreal={}
for i in anahtarliste:
    if i in compAnahtar:
        for n in degerrealliste:
            sozlukreal[i]=n
            degerrealliste.remove(n)
            break

print("\tDrawing process started...")

listX=sozluk.items()
listX=sorted(listX)
y,x=zip(*listX)

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
    label="{:.5f}".format(x_value)
    plt.annotate(label,(x_value,y_value),xytext=(space,0),textcoords="offset points",va='center',ha=ha)

#plt.axvline(1, color = 'magenta', linestyle = '-')
plt.barh(y,x, color=colors)
plt.xscale("log")
print("\tThe drawing is successful for Label vs Time!")
#plt.show()
plt.savefig('Label_vs_Time.pdf')
print("\n\tThe PDF version of the file has been saved.")
plt.savefig('Label_vs_Time.png')
print("\n\tThe PNG version of the file has been saved.\n")
#plt.savefig('Label_vs_Time.jpeg')
#print("\n\tThe JPEG version of the file has been saved.\n")


print("#####################################################\n")

listXreal=sozlukreal.items()
listXreal=sorted(listXreal)
y,x=zip(*listXreal) 

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
    label="{:.5f}".format(x_value)
    plt.annotate(label,(x_value,y_value),xytext=(space,0),textcoords="offset points",va='center',ha=ha)

#plt.axvline(1, color = 'magenta', linestyle = '-')
plt.barh(y,x, color=colors)
plt.xscale("log")
print("\tThe drawing is successful for Label vs Time_Real!")
#plt.show()
plt.savefig('Label_vs_Time_Real.pdf')
print("\n\tThe PDF version of the file has been saved.")
plt.savefig('Label_vs_Time_Real.png')
print("\n\tThe PNG version of the file has been saved.\n\n")
#plt.savefig('Label_vs_Time_Real.jpeg')
#print("\n\tThe JPEG version of the file has been saved.\n\n")




