import csv
import sys
import ROOT
import numpy as np
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TColor, TLegend, gStyle, TGraph, gROOT

if len(sys.argv) != 2:
    print('EXITING', file=sys.stderr)
    sys.exit (1)

V = []
I = []
count = 0
firstline= True

path = './IVScans/IVDataFiles/5th/' + sys.argv [1]
file = open(path)
reader = csv.reader(file, delimiter='\t')
next(reader)

def skip_last(iterator):
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item

for row in skip_last(reader):
    #print(row, file=sys.stderr)
    I.append(abs(float(row[1])))
    V.append(abs(float(row[0])))
    count += 1

print(I, file=sys.stderr)
print(V, file=sys.stderr)
V = np.array(V)
I = np.array(I)
length = len(V)
canvas = TCanvas('canvas', 'IV Scan', 200, 10, 700, 500)
g = TGraph(length, V, I)
g.GetXaxis().SetTitle('Voltage (V)')
g.GetYaxis().SetTitle('Current (uA)')
g.GetXaxis().SetNdivisions(length+2)
g.Draw('AL')
canvas.Update()
canvas.SaveAs('./IVScans/IVPlots_NoFit/' + str(sys.argv [1]) + '.pdf')

