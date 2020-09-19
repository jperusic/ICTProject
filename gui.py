## import tkinter libraries to use 
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import data as d
import plot as p
##import data

file1 = ''

##from data.py import process

## test script to test function of buttons
def testScript():
        messagebox.showinfo("Hello", "Wazzup")

def importFunction():
    file1 = d.importData()

def normaliseFunction():
    d.process(importFunction)

def importReadyDataFunction():
    p.importReadyData()

def plotFunction():
    p.plot(importReadyDataFunction)

## new tkinter window - labelled window
## title and size of window set
window = tk.Tk()
window.geometry("1080x720")
window.title("Raman Plotter")

## tabs will use notebook format
tabControl = ttk.Notebook(window)

## create layout for Raw Data tab - 2 panes flows vertically
## top row to hold buttons - 2 buttons flows horizontally
## bottom row to hold file list and preview of selected file - 2 panes flows horizonatally 
## footer to hold development details
raw = ttk.PanedWindow(tabControl, orient=VERTICAL)
rawTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
rawBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
rawFooter = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create layout for Ready Data tab - 2 panes flows vertically
## top row to hold buttons - 2 buttons flows horizontally
## bottom row to hold file list and preview of selected file - 2 panes flows horizonatally 
## footer to hold development details
ready = ttk.PanedWindow(tabControl, orient=VERTICAL)
readyTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
readyBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
readyFooter = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create layout for Plot tab - 1 Pane flows vertically
## footer to hold development details
plot = ttk.PanedWindow(tabControl, orient=VERTICAL)
plotFooter = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create 3 tabs with titles for each stage of the data flow: Raw, Ready, Plot
## display tabs on window
tabControl.add(raw, text="Raw")
tabControl.add(ready, text="Ready")
tabControl.add(plot, text="Plot")
tabControl.pack(expand=1, fill="both")

## label and entry box prompts user to enter waveshift offset - this offset will be used in normalisation process
## pack entry box to RH side with appropriate padding
inputLabel = Label(rawTop, text="Enter Waveshift Offset: ")
rawInput = Entry(rawTop, width=20)
rawInput.pack(side=RIGHT, padx=(10,20), pady=(10,0))
inputLabel.pack(side=RIGHT, padx=(0,5), pady=(10,0))

## raw labels to hold details of developers and their contact details for support/enquiries
## pack labels to footer with appropriate padding
rawDev = Label(rawFooter, height=1, text="Developed by J.Perusic & J.Winter (2020)")
rawContact = Label(rawFooter, height=1, text="Contact the Developers at: example@example.com")
rawContact.pack(side=BOTTOM, pady=(5,0))
rawDev.pack(side=BOTTOM, pady=(0,0))

## ready labels to hold details of developers and their contact details for support/enquiries
## pack labels to footer with appropriate padding
readyDev = Label(readyFooter, height=1, text="Developed by J.Perusic & J.Winter (2020)")
readyContact = Label(readyFooter, height=1, text="Contact the Developers at: example@example.com")
readyContact.pack(side=BOTTOM, pady=(5,0))
readyDev.pack(side=BOTTOM, pady=(0,0))

## plot labels to hold details of developers and their contact details for support/enquiries
## pack labels to footer with appropriate padding
plotDev = Label(plotFooter, height=1, text="Developed by J.Perusic & J.Winter (2020)")
plotContact = Label(plotFooter, height=1, text="Contact the Developers at: example@example.com")
plotContact.pack(side=BOTTOM, pady=(5,0))
plotDev.pack(side=BOTTOM, pady=(0,0))

## create button to import raw data files
## create button to normalise selected raw data files
## display buttons on raw tab (top row)
importRaw = Button(rawTop, text="Import Raw Data", width=20, height=2, command=importFunction, bg="blue", fg="black")
normaliseData = Button(rawTop, text="Normalise Data", width=20, height=2, command=normaliseFunction, bg="green", fg="black")
importRaw.pack(side=LEFT, padx=(20,10), pady=(10,0))
normaliseData.pack(side=LEFT, padx=(10,10), pady=(10,0))

## create button to import ready data files
## create button to plot selected ready data files
## display buttons on ready tab (top row)
importReady = Button(readyTop, text="Import Ready Data", width=20, height=2, command=importReadyDataFunction, bg="blue", fg="black")
plotData = Button(readyTop, text="Plot Data", width=20, height=2, command=plotFunction, bg="green", fg="black")
importReady.pack(side=LEFT, padx=(20,10), pady=(10,0))
plotData.pack(side=LEFT, padx=(10,10), pady=(10,0))

## create pane to hold the file list and a pane to display a preview of a file when selected
rawFiles = Listbox(rawBottom, width=55, height=32)
rawPreview = Listbox(rawBottom, width=55, height=32)

## create pane to hold the file list and a pane to display a preview of a file when selected
readyFiles = Listbox(readyBottom, width=55, height=32)
readyPreview = Listbox(readyBottom, width=55, height=32)

## create single pane to display graph generated by the plot button function
plotPreview = Frame(plot, height=600)

## demo data to populate file lists
for rawList in ["file1", "file2", "file3", "file4", "etc"]:
    rawFiles.insert(END, rawList)

for readyList in ["file1", "file2", "file3", "file4", "etc"]:
    readyFiles.insert(END, readyList)

## add the created panes which hold and preview raw data files to the raw data tab (bottom row)
rawBottom.add(rawFiles)
rawBottom.add(rawPreview)

## add the created panes which hold and preview ready data files to the ready data tab (bottom row)
readyBottom.add(readyFiles)
readyBottom.add(readyPreview)

## add the created panes which hold and the top and bottom rows of the raw tab
raw.add(rawTop)
raw.add(rawBottom)
raw.add(rawFooter)

## add the created panes which hold and the top and bottom rows of the ready tab
ready.add(readyTop)
ready.add(readyBottom)
ready.add(readyFooter)

## add the created panes which holds the generated graph to the plot tab
plot.add(plotPreview)
plot.add(plotFooter)
## display the window on run
window.mainloop()

##importRaw