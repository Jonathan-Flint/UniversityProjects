#!/usr/bin/python
import ROOT
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TColor, TLegend, gStyle
import sys
import numpy as np
import os
import math

if len(sys.argv) != 3:
    print("USAGE: %s <input  file > <output  file >"%(sys.argv [0]))
    sys.exit (1)

inFileName   = './Data/RootFiles/November2020SS03/' + sys.argv [1]#when run, makes system ask for a file name for code to be executed on
outFileName = sys.argv [2]#asks for output file name
print(inFileName)
print(outFileName)

# Get all data files in specific directory
# Iterate over the files calling the process function

# Make below here a function, arg = input file path
inFile = ROOT.TFile.Open(inFileName ,"READ")#opens the input ROOT file
hist1 = inFile.Get("h_scan0;1")#gets all the lines starting with h_scan0, ie, hybrid 1
hist2 = inFile.Get("h_scan1;1")#gets all the lines starting with h_scan1, ie, hybrid 2
#nEntries1 = hist1.GetEntries()#sets nEntries1 equal to number of lines for hybrid 1
#nEntries2 = hist2.GetEntries()#sets nEntries2 equal to number of lines for hybrid 2

nEntries1X = hist1.GetNbinsX()#gets the number of bins in x direction (1280) for hybrid 1
nEntries1Y = hist1.GetNbinsY()#gets the number of bins in y direction (64) for hybrid 1
nEntries2X = hist2.GetNbinsX()#gets the number of bins in x direction (1280) for hybrid 2
nEntries2Y = hist2.GetNbinsY()#gets the number of bins in y direction (64) for hybrid 2 

#Create Directory in the Final Plots dump for the data set being analysed

#if not os.path.exists('./Final Plots/' + str(sys.argv [1])):
 #  os.makedirs('./Final Plots/' + str(sys.argv [1]))

channels = 1280 #sets a custom amount of channels' data to analyse

#Start by creating and customizing the canvas

canvas = TCanvas('canvas', 'individual channel plot', 200, 10, 700, 500)
#canvas.SetFillColor(632)

#Create a histogram where we add 1 to each bin representing each time interval, for every channel that displays an output at that time
#For single channel plot this will create a perfect step function

f = open("./TextFiles/Analysis_" + sys.argv [1] + ".txt", "w+")            #creates a text file with name dead_channels and the data set being analysed 
f.write("Stream 0 Info:\n")
#f1 = open("./TextFiles/Dipped_channels_" + sys.argv [1] + ".txt", "w+")         #creates text file to store channels that have dips in plateau
#f1.write("Stream 0 Dipped Channels:\n")
#f3 = open("./TextFiles/Anomalous Channels" + sys.argv [1] + ".txt", "w+")
all_data_stream_0 = []
all_data_stream_1 = []
all_sd_stream_0 = []
all_sd_stream_1 = []
leading_edge_stream_0 = []
trailing_edge_stream_0 = []
leading_edge_stream_1 = []
trailing_edge_stream_1 = []
stream_0_dead_channels = 0
stream_1_dead_channels = 0
stream_0_dipped_channels = 0
stream_1_dipped_channels = 0
stream_0_trailing_anomalies = 0
stream_1_trailing_anomalies = 0
stream_0_channels_dead = []
stream_1_channels_dead = []
stream_0_channels_dipped = []
stream_1_channels_dipped = []
stream_0_anomalies = []
stream_1_anomalies = []

#loop through input file and fill the data into the histogram

#print(channel)
channel = 0                  #variable to keep track of which channel is being plotted, and for naming purposes

for  entryNumX  in  range(0,channels):         #loops through each channel
   
   h = TH1F('h', 'Stream 0 channel ' + str(entryNumX) +  sys.argv [1] + ' histogram', 64, 0, 63)
   h.GetXaxis().SetNdivisions(32)
   leading_start_found = False            #Sets variable = false again for each channel
   leading_start = -1111
   trailing_end_found = False
   trailing_end = -1111
   trailing_start = -1111
   max_value = -1111
   value = -1111
   data_array = []
   anomaly = False

   for i in range(63):            #loops through each bin/time interval
      h.SetBinContent(i, 0)         #sets all bin contents back to 0 before adding the data for next channel
   
   for  entryNumY  in  range(0,nEntries1Y):   #loops through each time interval 
      prev_value = value
      value = hist1.GetBinContent(entryNumX,entryNumY)   #sets value equal to the output value of that channel at that time interval
      data_array.append(value)
      
      
      #print(value, entryNumY, channel)         #prints the time interval and output value for debugging
      
                        #STEEPENESS FITTING COMMENTS
                        
                        #First fitting task is arbitrary steepness fit
                        #find first and last maxima of plateau
                        #calculate average difference between the bin contents between the 0 and first max, and last max and next 0
                        #add to legend
      
      if prev_value < value and value >= max_value:         #checks to see if the next value is greater than the previous
         #print(str(value))
         max_value = value         #If true, sets the max value equal to the current value
         leading_end = entryNumY         #sets the max_bin variable equal to the bin number where the new maximum occured
                        #This should work to find the first maximum and where it occurs
                        #Need to find the first non-zero bin
      if value == max_value:
          #print(str(entryNumY))
          trailing_start = entryNumY    
          
      if (leading_start_found == False):
         if value != 0:
            leading_start = entryNumY
            leading_start_found = True
            #print("leading start:" + str(leading_start))

      if (value > 0):
         trailing_end = entryNumY
         #print('trailing end:' + str(trailing_end))
         
                        #Need to do something similar for finding the final maximum, but need to account for dips in the plateau
                        #So can't just reverse the < sign and define new variables
      
                        #ERROR FUNCTION COMMENTS
                        
                        #Somewhere in here need to find a mid point in the plateau
                        #Then stop the addition of data and fit the leading edge
                        #Add the data for the trailing edge seperately
                        #Fit trailing edge
                        #Put the two together with fits
      
      if(entryNumY == trailing_start + 5 and value != 0):
         anomaly = True
         stream_0_trailing_anomalies += 1
         stream_0_anomalies.append(channel)

      if value != 0:
         h.SetBinContent(entryNumY, value)
      
   if np.sum(data_array) == 0:
      leading_start = 0
      leading_end = 0
      trailing_start = 0
      trailing_end = 0
      dead_channel = str(channel)
      stream_0_channels_dead.append(channel)
      dead = True
      stream_0_dead_channels += 1
      
   for i in data_array[leading_end:trailing_start]:
      if i < max_value:          #Checks to see if there are any points between the end of the leading and start of the trailing edges that fall below the maximum value, if so, add to text file
         stream_0_channels_dipped.append(channel)      
         stream_0_dipped_channels += 1
   #print('Trailing edge start:' + str(trailing_end))
   
   #for x in range(leading_start, leading_end):
   leading_edge_values = np.diff(data_array[leading_start:leading_end+1])
   leading_edge_steepness = np.average(leading_edge_values)
   trailing_edge_values = np.diff(data_array[trailing_start:trailing_end+1])   
   #print(trailing_edge_values)
   trailing_edge_steepness = np.average(trailing_edge_values)
   width = trailing_start - leading_end
   
   if np.average(data_array) == 0:
      sd = 0
   else:
      sd = leading_end + (0.6*width)
      sd = round(sd,0)
   legend = TLegend(0.98,0.75,0.78,0.62)
   legend.AddEntry(h, "width: " + str(width))
   legend.AddEntry(h, "Leading edge steepness: " + str(leading_edge_steepness))
   legend.AddEntry(h, "Traling edge steepness: " + str(trailing_edge_steepness))
   legend.AddEntry(h, "Strobe Delay Value SD: " + str(sd))
   all_data_stream_0.append(data_array)
   all_sd_stream_0.append(sd)
   leading_edge_stream_0.append([leading_start, leading_end])
   trailing_edge_stream_0.append([trailing_start, trailing_end])
   h.Draw()
   legend.Draw()
   canvas.Update()                                             #updates the canvas
   #canvas.SaveAs('./Final Plots/November2020SS03/ChannelPlots/stream_0_'+ str(channel) + str(sys.argv [1]) + '_hist.pdf')     #saves the canvas for the current channel once all the data has been added
   del h
   channel += 1                          #updates channel variable ready for next channel

f.write('Number Dead Channels: ' + str(stream_0_dead_channels) + "\r\n")
f.write('Number Dipped Channels: ' + str(stream_0_dipped_channels) + "\r\n")
f.write("Number Stream 0 Anomalies: " + str(stream_0_trailing_anomalies) + "\r\n")
canvas1 = TCanvas('Canvas 1', 'stream 0 2D all data histogram')            #Stream 0 2D histogram code
h1=TH2F('h1', sys.argv [1] + " stream 0 histogram", 1280, 0, 1279, 64, 0, 63)
h1.SetContour(1000)
h1.GetXaxis().SetTitle("Channels")
h1.GetYaxis().SetTitle("time")
h1.GetZaxis().SetTitle("Output Value")

channel = 0

for entryNumX in range(0,channels):                         #loop through each channel and each time interval, retrieve value and set relavent bin content in 2D hist equal to value
   value = -1111
   for entryNumY in range(0,nEntries1Y):
      value = hist1.GetBinContent(entryNumX, entryNumY)
      if value != 0:
         h1.SetBinContent(channel, entryNumY, value)
   channel += 1
   #print(channel)
   
h1.Draw('colz')
canvas1.Update()
canvas1.SaveAs('./Final Plots/November2020SS03/' + str(sys.argv [1]) + '_Stream_0_2D_hist.pdf')

def averageTime(channels):
   results = []
   for i in range(63):                   #sums all the output values for the channels in each chip and divides by 128
      time = []
      for j in range(127):
         time.append(channels[j][i])
      results.append(np.average(time))
   return results

stream_0_chip_0_data = averageTime(np.array(all_data_stream_0[0:127]))
stream_0_chip_1_data = averageTime(np.array(all_data_stream_0[128:255]))
stream_0_chip_2_data = averageTime(np.array(all_data_stream_0[256:383]))
stream_0_chip_3_data = averageTime(np.array(all_data_stream_0[384:511]))
stream_0_chip_4_data = averageTime(np.array(all_data_stream_0[512:639]))
stream_0_chip_5_data = averageTime(np.array(all_data_stream_0[640:767]))
stream_0_chip_6_data = averageTime(np.array(all_data_stream_0[768:895]))
stream_0_chip_7_data = averageTime(np.array(all_data_stream_0[896:1023]))
stream_0_chip_8_data = averageTime(np.array(all_data_stream_0[1024:1151]))
stream_0_chip_9_data = averageTime(np.array(all_data_stream_0[1152:1279]))

sd_stream_0_chip_0 = round(np.array(all_sd_stream_0[0:127]).sum()/128,0)
sd_stream_0_chip_1 = round(np.array(all_sd_stream_0[128:255]).sum()/128,0)
sd_stream_0_chip_2 = round(np.array(all_sd_stream_0[256:383]).sum()/128,0)
sd_stream_0_chip_3 = round(np.array(all_sd_stream_0[384:511]).sum()/128,0)
sd_stream_0_chip_4 = round(np.array(all_sd_stream_0[512:639]).sum()/128,0)
sd_stream_0_chip_5 = round(np.array(all_sd_stream_0[640:767]).sum()/128,0)
sd_stream_0_chip_6 = round(np.array(all_sd_stream_0[768:895]).sum()/128,0)
sd_stream_0_chip_7 = round(np.array(all_sd_stream_0[896:1023]).sum()/128,0)
sd_stream_0_chip_8 = round(np.array(all_sd_stream_0[1024:1151]).sum()/128,0)
sd_stream_0_chip_9 = round(np.array(all_sd_stream_0[1152:1279]).sum()/128,0)

stream_0_chip_0_leading = leading_edge_stream_0[0:127]
stream_0_chip_1_leading = leading_edge_stream_0[128:255]
stream_0_chip_2_leading = leading_edge_stream_0[256:383]
stream_0_chip_3_leading = leading_edge_stream_0[384:511]
stream_0_chip_4_leading = leading_edge_stream_0[512:639]
stream_0_chip_5_leading = leading_edge_stream_0[640:767]
stream_0_chip_6_leading = leading_edge_stream_0[768:895]
stream_0_chip_7_leading = leading_edge_stream_0[896:1023]
stream_0_chip_8_leading = leading_edge_stream_0[1024:1151]
stream_0_chip_9_leading = leading_edge_stream_0[1152:1279]

stream_0_chip_0_trailing = trailing_edge_stream_0[0:127]
stream_0_chip_1_trailing = trailing_edge_stream_0[128:255]
stream_0_chip_2_trailing = trailing_edge_stream_0[256:383]
stream_0_chip_3_trailing = trailing_edge_stream_0[384:511]
stream_0_chip_4_trailing = trailing_edge_stream_0[512:639]
stream_0_chip_5_trailing = trailing_edge_stream_0[640:767]
stream_0_chip_6_trailing = trailing_edge_stream_0[768:895]
stream_0_chip_7_trailing = trailing_edge_stream_0[896:1023]
stream_0_chip_8_trailing = trailing_edge_stream_0[1024:1151]
stream_0_chip_9_trailing = trailing_edge_stream_0[1152:1279]

def findEdgeMidpoint(chipNum, edge):
   #print(str(chipNum), file=sys.stderr)
   #print(edge, file=sys.stderr)
   for index, i in enumerate(edge):                           #loop through the start and end values of leading edge in each channel  
      edge[index] = np.average(i)                             #set each 2x1 entry to the average of itself
   #print(edge, file=sys.stderr)
   return np.average(edge)  #average all these averages for all 128 channels

stream_0_chip_0_leading_midpoint_final = findEdgeMidpoint(0, stream_0_chip_0_leading)
stream_0_chip_1_leading_midpoint_final = findEdgeMidpoint(1,stream_0_chip_1_leading)
stream_0_chip_2_leading_midpoint_final = findEdgeMidpoint(2,stream_0_chip_2_leading)
stream_0_chip_3_leading_midpoint_final = findEdgeMidpoint(3,stream_0_chip_3_leading)
stream_0_chip_4_leading_midpoint_final = findEdgeMidpoint(4,stream_0_chip_4_leading)
stream_0_chip_5_leading_midpoint_final = findEdgeMidpoint(5,stream_0_chip_5_leading)
stream_0_chip_6_leading_midpoint_final = findEdgeMidpoint(6,stream_0_chip_6_leading)
stream_0_chip_7_leading_midpoint_final = findEdgeMidpoint(7,stream_0_chip_7_leading)
stream_0_chip_8_leading_midpoint_final = findEdgeMidpoint(8,stream_0_chip_8_leading)
stream_0_chip_9_leading_midpoint_final = findEdgeMidpoint(9,stream_0_chip_9_leading)
stream_0_chip_0_trailing_midpoint_final = findEdgeMidpoint(0,stream_0_chip_0_trailing)
stream_0_chip_1_trailing_midpoint_final = findEdgeMidpoint(1,stream_0_chip_1_trailing)
stream_0_chip_2_trailing_midpoint_final = findEdgeMidpoint(2,stream_0_chip_2_trailing)
stream_0_chip_3_trailing_midpoint_final = findEdgeMidpoint(3,stream_0_chip_3_trailing)
stream_0_chip_4_trailing_midpoint_final = findEdgeMidpoint(4,stream_0_chip_4_trailing)
stream_0_chip_5_trailing_midpoint_final = findEdgeMidpoint(5,stream_0_chip_5_trailing)
stream_0_chip_6_trailing_midpoint_final = findEdgeMidpoint(6,stream_0_chip_6_trailing)
stream_0_chip_7_trailing_midpoint_final = findEdgeMidpoint(7,stream_0_chip_7_trailing)
stream_0_chip_8_trailing_midpoint_final = findEdgeMidpoint(8,stream_0_chip_8_trailing)
stream_0_chip_9_trailing_midpoint_final = findEdgeMidpoint(9,stream_0_chip_9_trailing)


#WRITE IMPORTANT VALUES TO TEXT FILE

#f = open(str(sys.argv [1]) + ' Chip_SD_and_Edge_Midpoint_Values.txt', "w")
f.write(str(sys.argv [1]) + 'Chip SD and Average Leading and Trailing Edge Midpoints\n')
f.write('#################\n')
f.write('Stream 0 Chip 0:\n')
f.write('SD: ' + str(sd_stream_0_chip_0) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_0_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_0_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 1:\n')
f.write('SD: ' + str(sd_stream_0_chip_1) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_1_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_1_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 2:\n')
f.write('SD: ' + str(sd_stream_0_chip_2) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_2_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_2_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 3:\n')
f.write('SD: ' + str(sd_stream_0_chip_3) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_3_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_3_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 4:\n')
f.write('SD: ' + str(sd_stream_0_chip_4) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_4_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_4_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 5:\n')
f.write('SD: ' + str(sd_stream_0_chip_5) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_5_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_5_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 6:\n')
f.write('SD: ' + str(sd_stream_0_chip_6) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_6_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_6_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 7:\n')
f.write('SD: ' + str(sd_stream_0_chip_7) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_7_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_7_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 8:\n')
f.write('SD: ' + str(sd_stream_0_chip_8) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_8_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_8_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 0 Chip 9:\n')
f.write('SD: ' + str(sd_stream_0_chip_9) + '\n')
f.write('Leading Midpoint: ' + str(stream_0_chip_9_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_0_chip_9_trailing_midpoint_final) + '\n')
f.write('###############################################################\n')
f.write('###############################################################\n')
f.write('Stream 1 Info\n')
f.write('###############################################################\n')
f.write('###############################################################\n')
def createCanvas(streamNum, canvasId, chipNum, chipData):
   methodCanvas = TCanvas('Canvas ' + str(canvasId), 'Chip ' + str(chipNum))
   hist = TH1F('h' + str(canvasId), sys.argv [1] + ' stream ' + str(streamNum) + ' chip ' + str(chipNum), 64, 0, 63)
   for i in range(63):
      hist.SetBinContent(i, chipData[i])
   hist.Draw()
   methodCanvas.Update()
   methodCanvas.SaveAs('./Final Plots/November2020SS03/' + str(sys.argv [1] + '_stream_' + str(streamNum) + '_chip_' + str(chipNum) + '_hist.pdf'))
   methodCanvas.Close()
   del methodCanvas

createCanvas(0, 2, 0, stream_0_chip_0_data)
createCanvas(0, 3, 1, stream_0_chip_1_data)
createCanvas(0, 4, 2, stream_0_chip_2_data)
createCanvas(0, 5, 3, stream_0_chip_3_data)
createCanvas(0, 6, 4, stream_0_chip_4_data)
createCanvas(0, 7, 5, stream_0_chip_5_data)
createCanvas(0, 8, 6, stream_0_chip_6_data)
createCanvas(0, 9, 7, stream_0_chip_7_data)
createCanvas(0, 10, 8, stream_0_chip_8_data)
createCanvas(0, 11, 9, stream_0_chip_9_data)


channel = 0                          #variable to keep track of which channel is being plotted, and for naming purposes

#f.write("Stream 1 Dead Channels:\n")
#f1.write("Stream 1 Dipped Channels:\n")
###############################
##########STREAM 2#############

canvas12 = TCanvas('canvas12', 'individual channel plot', 200, 10, 700, 500)

for  entryNumX  in  range(0,channels):         #loops through each channel
   
   h12 = TH1F('h12', 'Stream 1 channel ' + str(entryNumX) +  sys.argv [1] + ' histogram', 64, 0, 63)
   h12.GetXaxis().SetNdivisions(32)
   leading_start_found = False            #Sets variable = false again for each channel
   leading_start = 0
   trailing_end_found = False
   trailing_end = -1111
   trailing_start = -1111
   max_value = -1111
   value = -1111
   data_array = []

   for i in range(63):            #loops through each bin/time interval
      h12.SetBinContent(i, 0)         #sets all bin contents back to 0 before adding the data for next channel
   
   for  entryNumY  in  range(0,nEntries2Y):   #loops through each time interval 
      prev_value = value
      value = hist2.GetBinContent(entryNumX,entryNumY)   #sets value equal to the output value of that channel at that time interval
      data_array.append(value)
      
      
      #print(value, entryNumY, channel)         #prints the time interval and output value for debugging
      
                        #STEEPENESS FITTING COMMENTS
                        
                        #First fitting task is arbitrary steepness fit
                        #find first and last maxima of plateau
                        #calculate average difference between the bin contents between the 0 and first max, and last max and next 0
                        #add to legend
      
      if prev_value < value and value >= max_value:         #checks to see if the next value is greater than the previous
         #print(str(value))
         max_value = value         #If true, sets the max value equal to the current value
         leading_end = entryNumY         #sets the max_bin variable equal to the bin number where the new maximum occured
                        #This should work to find the first maximum and where it occurs
                        #Need to find the first non-zero bin
      if value == max_value:
          #print(str(entryNumY))
          trailing_start = entryNumY    
          
      if (leading_start_found == False):
         if value != 0:
            leading_start = entryNumY
            leading_start_found = True
            #print("leading start:" + str(leading_start))

      if (value > 0):
         trailing_end = entryNumY
         #print('trailing end:' + str(trailing_end))
         
                        #Need to do something similar for finding the final maximum, but need to account for dips in the plateau
                        #So can't just reverse the < sign and define new variables
      
                        #ERROR FUNCTION COMMENTS
                        
                        #Somewhere in here need to find a mid point in the plateau
                        #Then stop the addition of data and fit the leading edge
                        #Add the data for the trailing edge seperately
                        #Fit trailing edge
                        #Put the two together with fits
      
      if(entryNumY == trailing_start + 5 and value != 0):
         anomaly = True
         stream_1_anomalies.append(channel)
         stream_1_trailing_anomalies += 1

      if value != 0:
         h12.SetBinContent(entryNumY, value)
      
   if np.sum(data_array) == 0:
      leading_start = 0
      leading_end = 0
      trailing_start = 0
      trailing_end = 0
      dead_channel = str(channel)
      stream_1_channels_dead.append(channel)
      #f.write("Channel: " + dead_channel + "\n")        #Checks to see if all the data for a channel is equal to 0, if so, write the channel number to the dead channels text file
      dead = True
      stream_1_dead_channels += 1
      
   for i in data_array[leading_end:trailing_start]:
      if i < max_value:          #Checks to see if there are any points between the end of the leading and start of the trailing edges that fall below the maximum value, if so, add to text file
         #f1.write("Channel: " + str(channel) + "\n")       
         stream_1_dipped_channels += 1
         stream_1_channels_dipped.append(channel)
   #print('Trailing edge start:' + str(trailing_end))
   
   #for x in range(leading_start, leading_end):
   leading_edge_values = np.diff(data_array[leading_start:leading_end+1])
   leading_edge_steepness = np.average(leading_edge_values)
   trailing_edge_values = np.diff(data_array[trailing_start:trailing_end+1])   
   #print(trailing_edge_values)
   trailing_edge_steepness = np.average(trailing_edge_values)
   width = trailing_start - leading_end
   if np.average(data_array) == 0:
      sd = 0
   else:
      sd = leading_end + (0.6*width)
      sd = round(sd,0)
   legend = TLegend(0.98,0.75,0.78,0.62)
   legend.AddEntry(h12, "width: " + str(width))
   legend.AddEntry(h12, "Leading edge steepness: " + str(leading_edge_steepness))
   legend.AddEntry(h12, "Traling edge steepness: " + str(trailing_edge_steepness))
   legend.AddEntry(h12, "Strobe Delay Value SD: " + str(sd))
   all_data_stream_1.append(data_array)
   all_sd_stream_1.append(sd)
   leading_edge_stream_1.append([leading_start, leading_end])
   trailing_edge_stream_1.append([trailing_start, trailing_end])
   h12.Draw()
   legend.Draw()
   canvas12.Update()                                             #updates the canvas
   #canvas12.SaveAs('./FinalPlots/November2020SS03/ChannelPlots/stream_1_'+ str(channel) + str(sys.argv [1]) + '_hist.pdf')     #saves the canvas for the current channel once all the data has been added
   del h12
   channel += 1                          #updates channel variable ready for next channel

f.write('Number Dead Channels: ' + str(stream_1_dead_channels) + "\n")
f.write('Number Dipped Channels: ' + str(stream_1_dipped_channels) + "\n")
f.write("Number Stream 1 Anomalies: " + str(stream_1_trailing_anomalies) + "\r\n")

canvas13 = TCanvas('Canvas 13', 'stream 1 2D all data histogram')            #Stream 1 2D histogram code
h13=TH2F('h13', sys.argv [1] + " stream 1 histogram", 1280, 0, 1279, 64, 0, 63)
h13.SetContour(1000)
h13.GetXaxis().SetTitle("Channels")
h13.GetYaxis().SetTitle("time")
h13.GetZaxis().SetTitle("Output Value")

channel = 0

for entryNumX in range(0,channels):                         #loop through each channel and each time interval, retrieve value and set relavent bin content in 2D hist equal to value
   value = -1111
   for entryNumY in range(0,nEntries1Y):
      value = hist2.GetBinContent(entryNumX, entryNumY)
      if value != 0:
         h13.SetBinContent(channel, entryNumY, value)
   channel += 1
   print(channel)
   
h13.Draw('colz')
canvas13.Update()
canvas13.SaveAs('./Final Plots/November2020SS03/' + str(sys.argv [1]) + '_Stream_1_2D_hist.pdf')

stream_1_chip_0_data = averageTime(np.array(all_data_stream_1[0:127]))
stream_1_chip_1_data = averageTime(np.array(all_data_stream_1[128:255]))
stream_1_chip_2_data = averageTime(np.array(all_data_stream_1[256:383]))
stream_1_chip_3_data = averageTime(np.array(all_data_stream_1[384:511]))
stream_1_chip_4_data = averageTime(np.array(all_data_stream_1[512:639]))
stream_1_chip_5_data = averageTime(np.array(all_data_stream_1[640:767]))
stream_1_chip_6_data = averageTime(np.array(all_data_stream_1[768:895]))
stream_1_chip_7_data = averageTime(np.array(all_data_stream_1[896:1023]))
stream_1_chip_8_data = averageTime(np.array(all_data_stream_1[1024:1151]))
stream_1_chip_9_data = averageTime(np.array(all_data_stream_1[1152:1279]))

sd_stream_1_chip_0 = round(np.array(all_sd_stream_1[0:127]).sum()/128,0)
sd_stream_1_chip_1 = round(np.array(all_sd_stream_1[128:255]).sum()/128,0)
sd_stream_1_chip_2 = round(np.array(all_sd_stream_1[256:383]).sum()/128,0)
sd_stream_1_chip_3 = round(np.array(all_sd_stream_1[384:511]).sum()/128,0)
sd_stream_1_chip_4 = round(np.array(all_sd_stream_1[512:639]).sum()/128,0)
sd_stream_1_chip_5 = round(np.array(all_sd_stream_1[640:767]).sum()/128,0)
sd_stream_1_chip_6 = round(np.array(all_sd_stream_1[768:895]).sum()/128,0)
#print(sd_stream_1_chip_6, file=sys.stderr)
#print(all_sd_stream_1[768:895], file=sys.stderr)
sd_stream_1_chip_7 = round(np.array(all_sd_stream_1[896:1023]).sum()/128,0)
sd_stream_1_chip_8 = round(np.array(all_sd_stream_1[1024:1151]).sum()/128,0)
sd_stream_1_chip_9 = round(np.array(all_sd_stream_1[1152:1279]).sum()/128,0)

stream_1_chip_0_leading = leading_edge_stream_1[0:127]
stream_1_chip_1_leading = leading_edge_stream_1[128:255]
stream_1_chip_2_leading = leading_edge_stream_1[256:383]
stream_1_chip_3_leading = leading_edge_stream_1[384:511]
stream_1_chip_4_leading = leading_edge_stream_1[512:639]
stream_1_chip_5_leading = leading_edge_stream_1[640:767]
stream_1_chip_6_leading = leading_edge_stream_1[768:895]
stream_1_chip_7_leading = leading_edge_stream_1[896:1023]
stream_1_chip_8_leading = leading_edge_stream_1[1024:1151]
stream_1_chip_9_leading = leading_edge_stream_1[1152:1279]

stream_1_chip_0_trailing = trailing_edge_stream_1[0:127]
stream_1_chip_1_trailing = trailing_edge_stream_1[128:255]
stream_1_chip_2_trailing = trailing_edge_stream_1[256:383]
stream_1_chip_3_trailing = trailing_edge_stream_1[384:511]
stream_1_chip_4_trailing = trailing_edge_stream_1[512:639]
stream_1_chip_5_trailing = trailing_edge_stream_1[640:767]
stream_1_chip_6_trailing = trailing_edge_stream_1[768:895]
stream_1_chip_7_trailing = trailing_edge_stream_1[896:1023]
stream_1_chip_8_trailing = trailing_edge_stream_1[1024:1151]
stream_1_chip_9_trailing = trailing_edge_stream_1[1152:1279]

stream_1_chip_0_leading_midpoint_final = findEdgeMidpoint(0,stream_1_chip_0_leading)
stream_1_chip_1_leading_midpoint_final = findEdgeMidpoint(1,stream_1_chip_1_leading)
stream_1_chip_2_leading_midpoint_final = findEdgeMidpoint(2,stream_1_chip_2_leading)
stream_1_chip_3_leading_midpoint_final = findEdgeMidpoint(3,stream_1_chip_3_leading)
stream_1_chip_4_leading_midpoint_final = findEdgeMidpoint(4,stream_1_chip_4_leading)
stream_1_chip_5_leading_midpoint_final = findEdgeMidpoint(5,stream_1_chip_5_leading)
stream_1_chip_6_leading_midpoint_final = findEdgeMidpoint(6,stream_1_chip_6_leading)
stream_1_chip_7_leading_midpoint_final = findEdgeMidpoint(7,stream_1_chip_7_leading)
stream_1_chip_8_leading_midpoint_final = findEdgeMidpoint(8,stream_1_chip_8_leading)
stream_1_chip_9_leading_midpoint_final = findEdgeMidpoint(9,stream_1_chip_9_leading)
stream_1_chip_0_trailing_midpoint_final = findEdgeMidpoint(0,stream_1_chip_0_trailing)
stream_1_chip_1_trailing_midpoint_final = findEdgeMidpoint(1,stream_1_chip_1_trailing)
stream_1_chip_2_trailing_midpoint_final = findEdgeMidpoint(2,stream_1_chip_2_trailing)
stream_1_chip_3_trailing_midpoint_final = findEdgeMidpoint(3,stream_1_chip_3_trailing)
stream_1_chip_4_trailing_midpoint_final = findEdgeMidpoint(4,stream_1_chip_4_trailing)
stream_1_chip_5_trailing_midpoint_final = findEdgeMidpoint(5,stream_1_chip_5_trailing)
stream_1_chip_6_trailing_midpoint_final = findEdgeMidpoint(6,stream_1_chip_6_trailing)
stream_1_chip_7_trailing_midpoint_final = findEdgeMidpoint(7,stream_1_chip_7_trailing)
stream_1_chip_8_trailing_midpoint_final = findEdgeMidpoint(8,stream_1_chip_8_trailing)
stream_1_chip_9_trailing_midpoint_final = findEdgeMidpoint(9,stream_1_chip_9_trailing)

#WRITE IMPORTANT VALUES TO TEXT FILE
f.write(str(sys.argv [1]) + 'Chip SD and Average Leading and Trailing Edge Midpoints\n')
f.write('#################\n')
f.write('Stream 1 Chip 0:\n')
f.write('SD: ' + str(sd_stream_1_chip_0) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_0_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_0_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 1:\n')
f.write('SD: ' + str(sd_stream_1_chip_1) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_1_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_1_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 2:\n')
f.write('SD: ' + str(sd_stream_1_chip_2) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_2_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_2_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 3:\n')
f.write('SD: ' + str(sd_stream_1_chip_3) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_3_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_3_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 4:\n')
f.write('SD: ' + str(sd_stream_1_chip_4) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_4_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_4_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 5:\n')
f.write('SD: ' + str(sd_stream_1_chip_5) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_5_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_5_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 6:\n')
f.write('SD: ' + str(sd_stream_1_chip_6) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_6_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_6_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 7:\n')
f.write('SD: ' + str(sd_stream_1_chip_7) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_7_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_7_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 8:\n')
f.write('SD: ' + str(sd_stream_1_chip_8) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_8_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_8_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('Stream 1 Chip 9:\n')
f.write('SD: ' + str(sd_stream_1_chip_9) + '\n')
f.write('Leading Midpoint: ' + str(stream_1_chip_9_leading_midpoint_final) + '\n')
f.write('Trailing Midpoint: ' + str(stream_1_chip_9_trailing_midpoint_final) + '\n')
f.write('#################\n')
f.write('\n')
f.write('Stream 0 Channel Info:\n')
f.write('Dead Channels:\n')
for i in stream_0_channels_dead:
   f.write(str(i) + '\n')
f.write('Dipped Channels:\n')
for i in stream_0_channels_dipped:
   f.write(str(i) + '\n')
f.write('Anomalous Channels:\n')
for i in stream_0_anomalies:
   f.write(str(i) + '\n')
f.write('\n')
f.write('Stream 1 Channel Info:\n')
f.write('Dead Channels:\n')
for i in stream_1_channels_dead:
   f.write(str(i) + '\n')
f.write('Dipped Channels:\n')
for i in stream_1_channels_dipped:
   f.write(str(i) + '\n')
f.write('Anomalous Channels:\n')
for i in stream_1_anomalies:
   f.write(str(i) + '\n')

createCanvas(1, 14, 0, stream_1_chip_0_data)
createCanvas(1, 15, 1, stream_1_chip_1_data)
createCanvas(1, 16, 2, stream_1_chip_2_data)
createCanvas(1, 17, 3, stream_1_chip_3_data)
createCanvas(1, 18, 4, stream_1_chip_4_data)
createCanvas(1, 19, 5, stream_1_chip_5_data)
createCanvas(1, 20, 6, stream_1_chip_6_data)
createCanvas(1, 21, 7, stream_1_chip_7_data)
createCanvas(1, 22, 8, stream_1_chip_8_data)
createCanvas(1, 23, 9, stream_1_chip_9_data)

f.close()
#h.Draw()
#canvas.Update()
