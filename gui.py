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
window.geometry("820x420")
window.minsize(820, 420)
window.title("Raman Plotter")

## tabs will use notebook format
tabControl = ttk.Notebook(window)

## create layout for Raw Data tab - 2 panes flows vertically
## top row to hold buttons - 2 buttons flows horizontally
## bottom row to hold file list and preview of selected file - 2 panes flows horizonatally
## create footer to hold dev info 
raw = ttk.PanedWindow(tabControl, orient=VERTICAL)
rawTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
rawBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
rawFooter = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create layout for Ready Data tab - 2 panes flows vertically
## top row to hold buttons - 2 buttons flows horizontally
## bottom row to hold file list and preview of selected file - 2 panes flows horizonatally 
## create footer to hold dev info 
ready = ttk.PanedWindow(tabControl, orient=VERTICAL)
readyTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
readyBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
readyFooter = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create layout for Plot tab - 1 Pane flows vertically
## create footer to hold dev info 
plot = ttk.PanedWindow(tabControl, orient=VERTICAL)
plotTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
plotBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
plotFooter = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create 3 tabs with titles for each stage of the data flow: Raw, Ready, Plot
## display tabs on window
tabControl.add(raw, text="Raw")
tabControl.add(ready, text="Ready")
tabControl.add(plot, text="Plot")
tabControl.pack(expand=1, fill="both")

## create buttons to import raw data files and normalise selected ready data files
## display buttons on raw tab (top row)
importRaw = Button(rawTop, text="Import Raw Data", width=20, height=2, bg="blue", fg="white", highlightbackground='#0000FF', command=importFunction,)
normaliseData = Button(rawTop, text="Normalise Data", width=20, height=2, bg="green", fg="white", highlightbackground='#008000', command=normaliseFunction, )
importRaw.pack(side=LEFT, padx=(20,10), pady=(15,10))
normaliseData.pack(side=LEFT, padx=(10,10), pady=(15,10))

## label and entry box prompts user to enter waveshift offset - this offset will be used in normalisation process
## pack entry box to RH side with appropriate padding
inputLabel = Label(rawTop, text="Enter Waveshift Offset: ")
rawInput = Entry(rawTop, width=15)
rawInput.pack(side=RIGHT, padx=(10,20), pady=(10,0))
inputLabel.pack(side=RIGHT, padx=(0,5), pady=(10,0))

## create pane to hold the file list and a pane to display a preview of a file when selected
rawFiles = Listbox(rawBottom, selectmode=MULTIPLE, yscrollcommand=TRUE)
rawPreview = Listbox(rawBottom, yscrollcommand=TRUE)

## scrollbar for file list on raw tab
rawScroll = Scrollbar(rawFiles)
rawScroll.pack(side=RIGHT, fill=Y)
rawFiles.config(yscrollcommand=rawScroll.set)
rawScroll.config(command=rawFiles.yview)

## scrollbar for preview list on raw tab
rawScroll2 = Scrollbar(rawPreview)
rawScroll2.pack(side=RIGHT, fill=Y)
rawPreview.config(yscrollcommand=rawScroll2.set)
rawScroll2.config(command=rawPreview.yview)

## demo data to populate file lists
for rawList in ["file1", "file2", "file3", "file4", "etc"]:
    rawFiles.insert(END, rawList)

## create buttons to import ready data files and plot selected ready data files
## display buttons on ready tab (top row)
importReady = Button(readyTop, text="Import Ready Data", width=20, height=2, bg="blue", fg="white", highlightbackground='#0000FF', command=importReadyDataFunction)
plotData = Button(readyTop, text="Plot Data", width=20, height=2, bg="green", fg="white", highlightbackground='#008000', command=plotFunction)
importReady.pack(side=LEFT, padx=(20,10), pady=(15,10))
plotData.pack(side=LEFT, padx=(10,10), pady=(15,10))

## create pane to hold the file list and a pane to display a preview of a file when selected
readyFiles = Listbox(readyBottom, selectmode=MULTIPLE, yscrollcommand=TRUE)
readyPreview = Listbox(readyBottom, yscrollcommand=TRUE)

## scrollbar for file list on ready tab
readyScroll = Scrollbar(readyFiles)
readyScroll.pack(side=RIGHT, fill=Y)
readyFiles.config(yscrollcommand=readyScroll.set)
readyScroll.config(command=readyFiles.yview)

## scrollbar for preview list on ready tab
readyScroll2 = Scrollbar(readyPreview)
readyScroll2.pack(side=RIGHT, fill=Y)
readyPreview.config(yscrollcommand=readyScroll2.set)
readyScroll2.config(command=readyPreview.yview)

## demo data to populate file lists
for readyList in ["file1", "file2", "file3", "file4", "etc"]:
    readyFiles.insert(END, readyList)

## create buttons to plot the current graph as scatter or line 
## display buttons on plot tab (top row)
showScatter = Button(plotTop, text="Plot as Scatter", width=20, height=2, bg="blue", fg="white", highlightbackground='#0000FF', command=testScript)
showLine = Button(plotTop, text="Plot as Line", width=20, height=2, bg="green", fg="white", highlightbackground='#008000', command=testScript)
showScatter.pack(side=LEFT, padx=(20,10), pady=(15,10))
showLine.pack(side=LEFT, padx=(10,10), pady=(15,10))

## create single pane to display graph generated by the plot button function
plotPreview = Frame(plotBottom, height=600, bd=2, relief=GROOVE)

## raw labels to hold details of developers and their contact details for support/enquiries
## pack labels to footer with appropriate padding
rawDev = Label(window, height=1, text="Developed by J.Perusic & J.Winter (2020)")
rawContact = Label(window, height=1, text="Contact the Developers at: example@example.com")
rawContact.pack(side=BOTTOM, pady=(0,5))
rawDev.pack(side=BOTTOM, pady=(5,2))

## add the created panes which hold and the top and bottom rows of the raw tab
## pack file list and preview panes to the raw tab
## allocate footer space to display dev info
raw.add(rawTop)
raw.add(rawBottom)
rawFiles.pack(side=LEFT, expand=1, fill="both", padx=(0,10))
rawPreview.pack(side=RIGHT, expand=1, fill="both")
rawFooter.pack(side=BOTTOM)

## pack file list and preview panes to the ready tab
## add the created panes which hold and the top and bottom rows of the ready tab
## allocate footer space to display dev info
ready.add(readyTop)
ready.add(readyBottom)
readyFiles.pack(side=LEFT, expand=2, fill="both", padx=(0,10))
readyPreview.pack(side=RIGHT, expand=2, fill="both")
readyFooter.pack(side=BOTTOM)

## add the created panes which holds the generated graph to the plot tab
## allocate footer space to display dev info
plot.add(plotTop)
plot.add(plotBottom)
plotBottom.add(plotPreview)
plotFooter.pack(side=BOTTOM)

## display the window on run
window.mainloop()