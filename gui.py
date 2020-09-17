## import tkinter libraries to use 
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

## test script to test function of buttons
def testScript():
        messagebox.showinfo("Hello", "Wazzup")

## new tkinter window - labelled window
## title and size of window set
window = tk.Tk()
window.geometry("400x400")
window.title("Raman Plotter")

## tabs will use notebook format
tabControl = ttk.Notebook(window)

## create layout for Raw Data tab - 2 panes flows vertically
## top row to hold buttons - 2 buttons flows horizontally
## bottom row to hold file list and preview of selected file - 2 panes flows horizonatally 
raw = ttk.PanedWindow(tabControl, orient=VERTICAL)
rawTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
rawBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create layout for Ready Data tab - 2 panes flows vertically
## top row to hold buttons - 2 buttons flows horizontally
## bottom row to hold file list and preview of selected file - 2 panes flows horizonatally 
ready = ttk.PanedWindow(tabControl, orient=VERTICAL)
readyTop = ttk.PanedWindow(tabControl, orient=HORIZONTAL)
readyBottom = ttk.PanedWindow(tabControl, orient=HORIZONTAL)

## create layout for Plot tab - 1 Pane flows vertically
plot = ttk.PanedWindow(tabControl, orient=VERTICAL)

## create 3 tabs with titles for each stage of the data flow: Raw, Ready, Plot
## display tabs on window
tabControl.add(raw, text="Raw")
tabControl.add(ready, text="Ready")
tabControl.add(plot, text="Plot")
tabControl.pack(expand=1, fill="both")

## create button to import raw data files
## create button to normalise selected raw data files
## display buttons on raw tab (top row)
importRaw = tk.Button(rawTop, text="Import Raw Data", command=testScript)
normaliseData = tk.Button(rawTop, text="Normalise Data", command=testScript)
importRaw.pack()
normaliseData.pack()

## create button to import ready data files
## create button to plot selected ready data files
## display buttons on ready tab (top row)
importReady = Button(readyTop, text="Import Ready Data", command=testScript)
plotData = Button(readyTop, text="Plot Data", command=testScript)
importReady.pack()
plotData.pack()

## create pane to hold the file list and a pane to display a preview of a file when selected
rawFiles = Listbox(rawBottom)
rawPreview = Frame(rawBottom)

## create pane to hold the file list and a pane to display a preview of a file when selected
readyFiles = Listbox(readyBottom)
readyPreview = Frame(readyBottom)

## create single pane to display graph generated by the plot button function
plotPreview = Frame(plot)

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

## add the created panes which hold and the top and bottom rows of the ready tab
ready.add(readyTop)
ready.add(readyBottom)

## add the created panes which holds the generated graph to the plot tab
plot.add(plotPreview)
## display the window on run
window.mainloop()