import csv
import sys
import ROOT
import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TColor, TLegend, gStyle, TGraph, gROOT, TMultiGraph, TGraphPainter, gPad

if len(sys.argv) != 8:
    print('EXITING', file=sys.stderr)
    sys.exit (1)

V_1 = []
I_1 = []
V_2 = []
I_2 = []
V_3 = []
I_3 = []
V_4 = []
I_4 = []
V_5 = []
I_5 = []
V_6 = []
I_6 = []
V_7 = []
I_7 = []

path1 = './IVScans/IVDataFiles/3rd/' + sys.argv [1]
path2 = './IVScans/IVDataFiles/3rd/' + sys.argv [2]
path3 = './IVScans/IVDataFiles/3rd/' + sys.argv [3]
path4 = './IVScans/IVDataFiles/3rd/' + sys.argv [4]
path5 = './IVScans/IVDataFiles/3rd/' + sys.argv [5]
path6 = './IVScans/IVDataFiles/3rd/' + sys.argv [6]
path7 = './IVScans/IVDataFiles/3rd/' + sys.argv [7]

file1 = open(path1)
reader1 = csv.reader(file1, delimiter='\t')
next(reader1)

file2 = open(path2)
reader2 = csv.reader(file2, delimiter='\t')
next(reader2)

file3 = open(path3)
reader3 = csv.reader(file3, delimiter='\t')
next(reader3)

file4 = open(path4)
reader4 = csv.reader(file4, delimiter='\t')
next(reader4)

file5 = open(path5)
reader5 = csv.reader(file5, delimiter='\t')
next(reader5)

file6 = open(path6)
reader6 = csv.reader(file6, delimiter='\t')
next(reader6)

file7 = open(path7)
reader7 = csv.reader(file7, delimiter='\t')
next(reader7)

def skip_last(iterator):
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item

for row in skip_last(reader1):
    print(row, file=sys.stderr)
    I_1.append(abs(float(row[1])))
    V_1.append(abs(float(row[0])))

for row in skip_last(reader2):
    #print(row, file=sys.stderr)
    I_2.append(abs(float(row[1])))
    V_2.append(abs(float(row[0])))

for row in skip_last(reader3):
    #print(row, file=sys.stderr)
    I_3.append(abs(float(row[1])))
    V_3.append(abs(float(row[0])))

for row in skip_last(reader4):
    #print(row, file=sys.stderr)
    I_4.append(abs(float(row[1])))
    V_4.append(abs(float(row[0])))

for row in skip_last(reader5):
    #print(row, file=sys.stderr)
    I_5.append(abs(float(row[1])))
    V_5.append(abs(float(row[0])))

for row in skip_last(reader6):
    #print(row, file=sys.stderr)
    I_6.append(abs(float(row[1])))
    V_6.append(abs(float(row[0])))

for row in skip_last(reader7):
    #print(row, file=sys.stderr)
    I_7.append(abs(float(row[1])))
    V_7.append(abs(float(row[0])))

V_1 = np.array(V_1)
I_1 = np.array(I_1)
V_2 = np.array(V_2)
I_2 = np.array(I_2)
V_3 = np.array(V_3)
I_3 = np.array(I_3)
V_4 = np.array(V_4)
I_4 = np.array(I_4)
V_5 = np.array(V_5)
I_5 = np.array(I_5)
V_6 = np.array(V_6)
I_6 = np.array(I_6)
V_7 = np.array(V_7)
I_7 = np.array(I_7)

length = len(V_1)

canvas = TCanvas('canvas', '03/03/2021 IV Scans', 200, 10, 700, 500)

g = TMultiGraph()
legend = TLegend(0.98,0.75,0.78,0.62)
g1 = TGraph(length, V_1, I_1)
g1.SetLineColor(1)
#g1.SetTitle(str(sys.argv [1]))
g1.Draw('ALSame')

g2 = TGraph(length, V_2, I_2)
g2.SetLineColor(2)
#g2.SetTitle(str(sys.argv [2]))

g3 = TGraph(length, V_3, I_3)
g3.SetLineColor(3)
#g3.SetTitle(str(sys.argv [3]))

g4 = TGraph(length, V_4, I_4)
g4.SetLineColor(4)
#g4.SetTitle(str(sys.argv [4]))

g5 = TGraph(length, V_5, I_5)
g5.SetLineColor(5)
#g5.SetTitle(str(sys.argv [5]))

g6 = TGraph(length, V_6, I_6)
g6.SetLineColor(6)
#g6.SetTitle(str(sys.argv [6]))

g7 = TGraph(length, V_7, I_7)
g7.SetLineColor(7)
#g7.SetTitle(str(sys.argv [7]))


g.Add(g1, 'AL')
g.Add(g2, 'AL')
g.Add(g3, 'AL')
g.Add(g4, 'AL')
g.Add(g5, 'AL')
g.Add(g6, 'AL')
g.Add(g7, 'AL')
g.GetXaxis().SetTitle('Voltage (V)')
g.GetYaxis().SetTitle('Current (uA)')
g.Draw('A')

legend.SetHeader('Legend','C')
legend.AddEntry(g1, str(sys.argv [1]))
legend.AddEntry(g2, str(sys.argv [2]))
legend.AddEntry(g3, str(sys.argv [3]))
legend.AddEntry(g4, str(sys.argv [4]))
legend.AddEntry(g5, str(sys.argv [5]))
legend.AddEntry(g6, str(sys.argv [6]))
legend.AddEntry(g7, str(sys.argv [7]))

legend.Draw()

canvas.Update()
canvas.SaveAs('./IVScans/multi_plots/' + str(sys.argv [1]) + '.pdf')

