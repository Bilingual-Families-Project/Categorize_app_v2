#!/usr/bin/env python3

'''
app to read in and classify chunks of audio
Meg Cychosz & Ronald Sprouse
UC Berkeley

adapted by: 
Jessica Kosie
Princeton University
For use in the Princeton/Concordia Bilingual Families Project

'''


try:
    import Tkinter as tk  # Python2
except ImportError:
    import tkinter as tk  # Python3
import tkinter.font as tkFont
import pandas as pd
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from functools import partial
import os
import subprocess
import datetime

from math import ceil, log10

#number of minute-audio-clips in folder; index of row in df
idx = 0
df = None
row = None
resp_df = None





# clear category selection   
def clear():
    beginoptionscat.set("Categorize clip")
 
    englishcat.set(0)
    frenchcat.set(0)
    mixedcat.set(0)
    unsurecat.set(0)
    mostlyenglishcat.set(0)
    mostlyfrenchcat.set(0)
    equalcat.set(0)
    unsure2cat.set(0)
    withinspeakercat.set(0)
    betweenspeakerscat.set(0)
    noswitchingcat.set(0)
    unsure3cat.set(0)
    adultmalecat.set(0)
    adultfemalecat.set(0)
    targetchildcat.set(0)
    otherchildcat.set(0)
    unsure4cat.set(0)
    targetchild2cat.set(0)
    otherchild2cat.set(0)
    adultcat.set(0)
    unsure5cat.set(0)


    comments.delete(0, 'end')






# need to give multiple commands to button below
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func



# get initial info about annotator
def annotatorinfo():
    global df
    global outdir
    global content
    global resp_df

    showinfo('Window', "Select a metadata file")

    fname = askopenfilename()
    outdir = os.path.split(fname)[0]

    df = pd.read_csv(fname).assign(outdir=outdir) # the master config file that won't change

    try:
        resp_df = pd.read_csv(os.path.join(outdir, "responses.csv")) # if available, open the response df in read mode 

    except: # if not, create one
        empty = pd.DataFrame().assign(id=None, age_YYMMDD=None, date_YYYYMMDD=None, gender=None, timestamp_HHMMSS=None, percents_voc=None, outdir=None, researcher_present=None) # add addtl columns, file_name=None, 
        empty.to_csv(os.path.join(outdir, "responses.csv"), index=False) 
        resp_df = pd.read_csv(os.path.join(outdir, "responses.csv")) 


    annotate = tk.Toplevel()
    annotate.title("Annotator information")
    annotateSize = 220
    
    def close_window(annotate):
        annotate.destroy()

    tk.Label(annotate, text="What is your name?").grid(row=0)
    name = tk.Entry(annotate)
    def return_name():
        global content
        content = name.get()
    name.grid(row=0, column=1)


    tk.Button(annotate, text="Enter", command=combine_funcs(return_name, partial(close_window, annotate))).grid(row=7,column=1,columnspan=2)







#index and play audio file aloud
def play_audio():

    global repeat_ct
    repeat_ct = 0 

    global row
    global audiofile
    row = df.sample(n=1).iloc[0] # just randomly sample from entire df
    if row['researcher_present']==1:
        print('Researcher present in recording. Press Next.')
    elif row['percents_voc']==0: # if no vocal activity, skip the clip
        print('No vocal activity in clip. Press Next.')
    elif row['sleeping']==1: # if child is sleeping
        print('Child is sleeping. Press Next.')
   
    else:
        audiofile = os.path.join(row.outdir, row.file_name)
        row_file_name = row.file_name
    
        print(idx, row.file_name) # keep us updated about progress in terminal 

        subprocess.call(["afplay", audiofile])



#go to the next audio file 
def next_audio():

    global repeat_ct

    beginoptions = beginoptionscat.get() # get the speaker classification
    
    english = englishcat.get() 
    french = frenchcat.get() 
    mixed = mixedcat.get()
    unsure = unsurecat.get() 
    mostlyenglish = mostlyenglishcat.get()
    mostlyfrench = mostlyfrenchcat.get()
    equal = equalcat.get()
    unsure2 = unsure2cat.get()
    withinspeaker = withinspeakercat.get()
    betweenspeakers = betweenspeakerscat.get()
    noswitching = noswitchingcat.get()
    unsure3 = unsure3cat.get()
    adultmale = adultmalecat.get()
    adultfemale = adultfemalecat.get()
    targetchild = targetchildcat.get()
    otherchild = otherchildcat.get()
    unsure4 = unsure4cat.get()
    targetchild2 = targetchild2cat.get() 
    otherchild2 = otherchild2cat.get()
    adult = adultcat.get()
    unsure5 = unsure5cat.get()

    clip_comments = comments.get()



    annotate_date_YYYYMMDD = datetime.datetime.now() # get current annotation time
    print(beginoptions, english, french, mixed, unsure, mostlyenglish, mostlyfrench, equal, unsure2, withinspeaker, betweenspeakers, noswitching, unsure3, adultmale, adultfemale, targetchild, otherchild, unsure4, targetchild2, otherchild2, adult, unsure5, annotate_date_YYYYMMDD, content, clip_comments) 

    global row
    global resp_df
    allcols = pd.DataFrame([row]).assign(beginoptions=beginoptions, Q1_English=english, Q1_French=french, Q1_Mixed=mixed, Q1_Unsure=unsure, Q2_MostlyEnglish=mostlyenglish, Q2_MostlyFrench=mostlyfrench, Q2_Equal=equal, Q2_Unsure=unsure2, Q3_Within=withinspeaker, Q3_Between=betweenspeakers, Q3_Unsure=unsure3, Q4_AdultMale = adultmale, Q4_AdultFemale = adultfemale, Q4_TargetChild=targetchild, Q4_OtherChild=otherchild, Q4_Unsure=unsure4, Q5_TargetChild = targetchild2, Q5_OtherChild = otherchild2, Q5_Adult = adult, Q5_Unsure = unsure5, comments=clip_comments, annotate_date_YYYYMMDD=annotate_date_YYYYMMDD, annotator=content, repeats=repeat_ct) 
    resp_df = pd.concat([resp_df, allcols], sort=True)
    resp_df.to_csv(os.path.join(outdir, "responses.csv"), index=False)  # yes, this overwrites responses.csv each time  

    global idx 
    idx += 1 # update the global idx

    repeat_ct = 0 

    play_audio()


    
def repeat():

    subprocess.call(["afplay", audiofile])

    global repeat_ct

    repeat_ct = repeat_ct + 1



def main():
    global beginoptionscat
    global englishcat
    global frenchcat
    global mixedcat
    global unsurecat
    global comments
    global mostlyenglishcat
    global mostlyfrenchcat
    global equalcat
    global unsure2cat
    global withinspeakercat
    global betweenspeakerscat
    global noswitchingcat
    global unsure3cat
    global adultmalecat
    global adultfemalecat
    global targetchildcat
    global otherchildcat
    global unsure4cat
    global targetchild2cat
    global otherchild2cat
    global adultcat
    global unsure5cat

    root = tk.Tk() # refers to annotation window 

    root.update()

    root.title("Categorize")

    frame = tk.Frame(root, bg="white")
    frame.grid(row=15, column=15)

    beginoptionscat = tk.StringVar()
 
    beginoptions_choices = {"No speech: Skip clip", "Categorize clip"}
    
    beginoptionscat.set("Categorize clip")

    popupMenu0 = tk.OptionMenu(frame, beginoptionscat, *beginoptions_choices)
    
    popupMenu0.grid(row=3, column=1)
    

    fontStyle = tkFont.Font(family="Lucida Grande", size=16, weight="bold")

    tk.Label(frame, font=fontStyle, text="Classify clip").grid(row=3, column=0)

# Classify language(s) used in clip: 

    tk.Label(frame, font=fontStyle, text="1. Languages Used").grid(row=4, column=0)

    tk.Label(frame, text="Classify the language(s) used in the clip:").grid(row=7, column=0)
    englishcat = tk.IntVar()
    tk.Checkbutton(frame, text='English', variable=englishcat).grid(row=7, column=1)


    frenchcat = tk.IntVar()
    tk.Checkbutton(frame, text='French', variable=frenchcat).grid(row=7, column=2)

    mixedcat = tk.IntVar()
    tk.Checkbutton(frame, text='Mixed', variable=mixedcat).grid(row=7, column=3)

    unsurecat = tk.IntVar()
    tk.Checkbutton(frame, text='Unsure', variable=unsurecat).grid(row=7, column=4)


# Classify approximate proportion of each langauge used in clip: 

    tk.Label(frame, font=fontStyle, text="2. Estimate of Primary Language").grid(row=8, column=0)

    tk.Label(frame, text="The language used in this clip is:").grid(row=11, column=0)
    
    mostlyenglishcat = tk.IntVar()
    tk.Checkbutton(frame, text='All/Mostly English', variable=mostlyenglishcat).grid(row=11, column=1)


    mostlyfrenchcat = tk.IntVar()
    tk.Checkbutton(frame, text='All/Mostly French', variable=mostlyfrenchcat).grid(row=11, column=2)


    equalcat = tk.IntVar()
    tk.Checkbutton(frame, text='Both Equally', variable=equalcat).grid(row=11, column=3)

    unsure2cat = tk.IntVar()
    tk.Checkbutton(frame, text='Unsure', variable=unsure2cat).grid(row=11, column=4)	

# Classify switching used in clip: 

    tk.Label(frame, font=fontStyle, text="3. Classify Switching").grid(row=12, column=0)

    tk.Label(frame, text="The switching types(s) used in this clip are:").grid(row=15, column=0)
    
    withinspeakercat = tk.IntVar()
    tk.Checkbutton(frame, text='Within Speaker Switching', variable=withinspeakercat).grid(row=15, column=1)


    betweenspeakerscat = tk.IntVar()
    tk.Checkbutton(frame, text='Between Speaker Switching', variable=betweenspeakerscat).grid(row=15, column=2)

    noswitchingcat = tk.IntVar()
    tk.Checkbutton(frame, text='No Switching', variable=noswitchingcat).grid(row=15, column=3)	

    unsure3cat = tk.IntVar()
    tk.Checkbutton(frame, text='Unsure', variable=unsure3cat).grid(row=15, column=4)


# Classify speaker(s) in clip: 

    tk.Label(frame, font=fontStyle, text="4. Classify Speaker(s)").grid(row=16, column=0)

    tk.Label(frame, text="The speech in this clip is spoken by:").grid(row=19, column=0)
    
    adultmalecat = tk.IntVar()
    tk.Checkbutton(frame, text='Adult Male', variable=adultmalecat).grid(row=19, column=1)


    adultfemalecat = tk.IntVar()
    tk.Checkbutton(frame, text='Adult Female', variable=adultfemalecat).grid(row=19, column=2)


    targetchildcat = tk.IntVar()
    tk.Checkbutton(frame, text='Target Child', variable=targetchildcat).grid(row=19, column=3)

    otherchildcat = tk.IntVar()
    tk.Checkbutton(frame, text='Other Child(ren)', variable=otherchildcat).grid(row=19, column=4)

    unsure4cat = tk.IntVar()
    tk.Checkbutton(frame, text='Unsure', variable=unsure4cat).grid(row=19, column=5)


# Classify addressee(s) used in clip: 

    tk.Label(frame, font=fontStyle, text="5. Classify Addressee(s)").grid(row=20, column=0)

    tk.Label(frame, text="The speech in this clip is addressed to:").grid(row=23, column=0)
    
    targetchild2cat = tk.IntVar()
    tk.Checkbutton(frame, text='Target Child', variable=targetchild2cat).grid(row=23, column=1)


    otherchild2cat = tk.IntVar()
    tk.Checkbutton(frame, text='Other Child(ren)', variable=otherchild2cat).grid(row=23, column=2)


    adultcat = tk.IntVar()
    tk.Checkbutton(frame, text='Adult(s)', variable=adultcat).grid(row=23, column=3)

    unsure5cat = tk.IntVar()
    tk.Checkbutton(frame, text='Unsure', variable=unsure5cat).grid(row=23, column=4)
    

    
    tk.Label(frame, font=fontStyle, text="Comments about clip?").grid(row=25, column=0)
    comments = tk.Entry(frame) 
    comments.grid(row=25, column=1, columnspan=2)




    tk.Button(frame, text="     Play     ", command=combine_funcs(play_audio, clear), bg="gray").grid(row=1, column=0) 

    tk.Button(frame, text="        Next       ", command=combine_funcs(next_audio, clear), bg="gray").grid(row=1, column=2) 

    tk.Button(frame, background="gray", text="   Repeat   ", command=repeat).grid(row=1, column=1)

    app = annotatorinfo()
    root.mainloop()  

if __name__ == "__main__":
    main()
