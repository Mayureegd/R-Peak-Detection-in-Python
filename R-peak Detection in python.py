import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps
import tkinter as tk
from tkinter import *
from tkinter import filedialog , Text
from tkinter import messagebox
from tkinter import ttk
import os

#*********************************************************************************************************************

def tab6():
  def terminate():
    root.destroy()
  def arrythamia_detection():
    if(60<bpm<100):
        response = messagebox.showinfo("Arrythamia Dtetection" , "no arrythamia detected")
    else:
      response = messagebox.showinfo("Arrythamia Dtetection" , "Arrythamia detected! Please see a cardiologist!")
    terminate()
  btn5.destroy()
  btn6 = Button(frame , text="Next" , command=lambda:[(step()) , (arrythamia_detection())], bg='#263d42' , fg='white' )
  btn6.pack()
  btn6.place(x=150 , y=400)

def Rwave_peaks(ecg, d_ecg, Rwave_peaks_d_ecg, time):
    global bpm   
    Rwave = np.empty([len(Rwave_peaks_d_ecg)-1]) 
    for i in range(0, len(Rwave)): # for all peaks
        ecgrange = ecg[Rwave_peaks_d_ecg[i]:Rwave_peaks_d_ecg[i+1]] # create array that contains of the ecg within the d_ecg_peaks
        percentage = np.round(len(ecgrange)*0.2)
        maxvalue = np.array(list(np.where(ecgrange == np.max(ecgrange[0:int(percentage)])))) # find the index of the max value of ecg
        Rwave[i] = Rwave_peaks_d_ecg[i] + maxvalue[0,0]  # save this index         
    
    Rwave = Rwave.astype(np.int64)
    Rwave_t = time[Rwave]
    Rwave_t = Rwave_t.reset_index(drop = True)
    Rwave_t = Rwave_t.drop(columns = ['index'])
    RR_interval = np.diff(Rwave_t)
    bpm = (60/(np.mean(RR_interval)))*360
    print("Beats per minute is ",bpm)
    tab6()


def r_peaks(heightper , distanceper):
  #filter out all peaks that are under the height threshold and not over a minimum distance from each other
  #height threshold percentage in decimal, distance threshold in decimal
  meanpeaks_d_ecg = np.mean(d_ecg[peaks_d_ecg]) # find the mean of the peaks
  max_d_ecg = np.max(d_ecg) #find max of the ecg signal
  threshold = np.mean([meanpeaks_d_ecg,max_d_ecg])*heightper #height fraction should usually be 0.4
  newpeaks_d_ecg,_ = sps.find_peaks(d_ecg, height = threshold) # find the new peaks
  newpeaks_d_ecg_t = ecg.samples[newpeaks_d_ecg]
  newpeaks_d_ecg_t = newpeaks_d_ecg_t.reset_index(drop = True)
  meandistance = np.mean(np.diff(newpeaks_d_ecg))
  Rwave_peaks_d_ecg,_ = sps.find_peaks(d_ecg,height = threshold, distance = meandistance*0.5) #distance fraction should usually be 0.5
  Rwave_peaks(ecg, d_ecg, Rwave_peaks_d_ecg, ecg.samples)
  

def tab5():
    global btn5
    btn4.destroy()
    btn5 = Button(frame , text="Next" , command=lambda:[r_peaks(0.4 , 0.5) ,(step())], bg='#263d42' , fg='white' )
    btn5.pack()
    btn5.place(x=150 , y=400)


def peaks_in_ecg(d_ecg):
  global peaks_d_ecg
  peaks_d_ecg,_ = sps.find_peaks(d_ecg)
  tab5()

def tab4():
    global btn4 
    btn3.destroy()
    btn4 = Button(frame , text="Next" , command=lambda:[peaks_in_ecg(d_ecg) ,(step())], bg='#263d42' , fg='white' )
    btn4.pack()
    btn4.place(x=150 , y=400)

def decg(ecg, time):
    """Step 1: Find the peaks of the derivative of the ECG signal"""
    global d_ecg
    d_ecg = np.diff(ecg) #find derivative of ecg signal
    # plot step 1
    time = time[0:len(time)-1]
    tab4()

def step():
  my_progress['value'] +=20
  
def tab3():
    global btn3 
    text.delete(1.0,"end")
    text.insert(END , "Further in order to extract very\ndistinctive peaks, first order\nderivative of filtered signal is\ntaken,then peaks are")
    text.insert(END, " obtained,then filterd out by taking suitable\nthreshold to get R peaks in ECG\nusing scipy python library.")
    text.insert(END ,"\nHeart rate variability is \ncalculated using RR-interval\n(A normal resting heart rate for\nadults ranges from 60 to 100 bpm.)")
    text.insert(END ,"\n\nPlease Click on the next Button to proceed.")
    btn2.destroy()
    btn3 = Button(frame , text="Next" , command=lambda:[(decg(ecg.MLII , ecg.samples)) , (step())], bg='#263d42' , fg='white' )
    btn3.pack()
    btn3.place(x=150 , y=400)
  
def filter_ecg(ecg):
  Wn = 0.167
  b , a = sps.butter(4 , Wn , 'low' , analog=False)
  fecg = sps.filtfilt(b , a , ecg.MLII)
  ecg=fecg
  tab3()


def tab2():
    global btn2 , my_progress
    text.delete(1.0,"end")
    text.insert(END , "Electrocardiogram (ECG) is an\nimportant clinical tool for\ninvestigating the activities\nof heart. ECG signals may be\ncorrupted by various kinds of noise")
    text.insert(END , "\nLike  Power line interference ,\nElectrode contact noise,\nInstrumentation noise ,Muscle\ncontraction etc.")
    text.insert(END , "For the meaningful and accurate detection, steps have\nto be taken to filter out or\ndiscard all these noise sources.")
    text.insert(END , "\n\nPlease click on the next button")
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("Horizontal.TProgressbar", background='#263d42')
    my_progress = ttk.Progressbar(frame , orient=HORIZONTAL , length=300 , mode='determinate' ,style="Horizontal.TProgressbar")
    my_progress.pack()
    my_progress.place(x=10 ,y=330)
    btn1.destroy()
    btn2 = Button(frame , text="Next" , command=lambda:[(filter_ecg(ecg)) , (step())], bg='#263d42' , fg='white' )
    btn2.pack()
    btn2.place(x=150 , y=400)


def ecg_signal(filepath):
  column_names = ['samples' , 'MLII' , 'V5']
  global ecg
  ecg = pd.read_csv(filepath ,skiprows=1 , skipfooter=100000 , names = column_names , engine='python')
  ecg.drop('V5',axis=1)
  plt.figure(figsize=(10,5))
  plt.plot(ecg.samples[0:1000] , ecg.MLII[0:1000])
  plt.title("Your ECG File.Please Click on the next Button")
  plt.show()
  tab2()

def openfile():
    global filepath
    text.delete(1.0,"end")
    text.insert(END , "Electrocardiography is the process of producing an electrocardiogram.") 
    text.insert(END , "\nIt is an electrogram of the heart\nwhich is a graph of voltage versus\ntime of the electrical activity\nof the heart using\nelectrodes placed on the skin.")
    text.insert(END , "\n\nYour ECG file is Displayed")
    filepath = filedialog.askopenfilename(initialdir='C:/ECG Datasets' , title='Select a csv file', filetypes=(("csvfiles" , "*.csv"),))
    ecg_signal(filepath)

#*******************************************************************************************************************

root = tk.Tk()
root.title("Arrythamia Detector")

canvas = tk.Canvas(root , height=600, width=400 , bg="#263d42")
canvas.pack()

frame = tk.Frame(root , bg="#3e646c")
frame.place(relwidth=0.8 , relheight=0.8 , rely=0.1 , relx=0.1)



btn1 = Button(frame , text="Browse the ecg file" , command=openfile, bg='#263d42' , fg='white' , padx=5 , pady=10)
btn1.pack()
btn1.place(x=100 , y=350)

text = Text(frame , width = 35, height = 15 , bg="#263d42" , fg="white" )
text.pack()
text.place(x=15 , y= 60)
text.insert(END ," This GUI Application will detect\npresence or absence of arrythmia\nusing the ecg file(.csv). ")
text.insert(END , "\nArrythamia is a condition in which\nthe heart beats with an\nirregular or abnormal rhythm.")
text.insert(END , "\nWhich is caused due to Blocked\narteries,hyperthyroidism,\nhypothyroidism,Diabetes,High blood pressure etc")
text.insert(END , "\n\nPlease Choose a ECG recording savedon your system")
root.mainloop()







