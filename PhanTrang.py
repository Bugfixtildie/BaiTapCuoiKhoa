from tkinter import*
import tkinter as tk
from tkinter import ttk
import json
#from PIL import Image, ImageTk
#import cv2
#import numpy as np
from tkinter.filedialog import askopenfilename
from tkVideoPlayer import TkinterVideo
import datetime

test = tk.Tk()
test.attributes("-fullscreen", True)
frame = Frame(test)
frame.pack(side='right')

PhanTrangFrame = Frame(frame)
PhanTrangFrame.grid(row=1, column=1)

videoplayer = TkinterVideo(master=test,bg='green')
videoplayer.pack(expand=True, fill="both")

videocontrolframe = Frame(test)
videocontrolframe.pack(side='bottom')

main = ttk.Treeview(frame)
main.grid(row=0,column=0,columnspan=3)

main['columns'] = ('stt', 'id', 'name')

main.column("#0", width = 0, stretch=NO)
main.column('stt', anchor=CENTER, width=80)
main.column('id', anchor=CENTER, width=80)
main.column('name', anchor=CENTER, width=80)

main.heading("#0", text="", anchor=CENTER)
main.heading('stt', text='ORDER', anchor=CENTER)
main.heading('id', text='ID', anchor=CENTER)
main.heading('name', text='NAME', anchor=CENTER)

with open('data.json') as f:
    file = json.load(f)

inputID = StringVar()
inputNAME = StringVar()
inputTIM = StringVar()

if len(file) < 3:
    SoPhanTuTrenTrang=0
    for i in range(len(file)):
        main.insert(parent="", index="end", iid=SoPhanTuTrenTrang, text='',
                    values=(SoPhanTuTrenTrang+1, file[i].get('id'), file[i].get('name')))
        SoPhanTuTrenTrang += 1
else:
    SoPhanTuTrenTrang=0
    for i in range(3):
        main.insert(parent="", index="end", iid=SoPhanTuTrenTrang, text='',
                    values=(SoPhanTuTrenTrang+1, file[i].get('id'), file[i].get('name')))
        SoPhanTuTrenTrang += 1

#DEFINING VARIABLES
TrangHienTai = 1
SearchResultIndexList = []
temp = 0
SrcHinh = ''


#DEFINING SECTION
def them():
    global TrangHienTai
    global SrcHinh

    if SrcHinh == "":
         SrcHinh = "NoImage.png"

    file.append(
        {
            "id": inputID.get(),
            "name": inputNAME.get(),
            "src": SrcHinh
        }
    )
    
    inputID.set("")
    inputNAME.set("")

    with open('data.json', "w", encoding='utf8') as f:
        json.dump(file, f, ensure_ascii=False, indent=2)
    
    for i in main.get_children():
        main.delete(i)

    count = 0
    for i in range(TrangHienTai*3-3 ,TrangHienTai*3):
            main.insert(parent='', index='end', iid=count, text='',
                        values=(i+1, file[i].get('id'), file[i].get('name')))
            if (count + 1 == len(file) - (TrangHienTai - 1)*3):
                     break
            count+=1         
    SrcHinh = ""

def themmenu():
    childwin = Toplevel()
    childwin.title('Save file')

    etrID = tk.Entry(childwin, textvariable=inputID)
    etrNAME = tk.Entry(childwin, textvariable=inputNAME)

    btnTHEM = tk.Button(childwin, text="Add", command=them)

    etrID.pack()
    etrNAME.pack()

    btnTHEM.pack()     

def xoa():
    global TrangHienTai
    global SearchResultIndexList
    global temp
        
    imtem = main.selection()[0]
    
    if TrangHienTai == 0:
         del file[SearchResultIndexList[int(imtem)]]
         TrangHienTai = temp
         inputTIM.set("")
    else:
        del file[(TrangHienTai - 1)*3 + int(imtem)]
        count = 0
        for i in main.get_children():
            count += 1
        if (count <= 1 ):
             TrangHienTai -= 1


    with open('data.json', "w", encoding='utf8') as f:
        json.dump(file, f, ensure_ascii=False, indent=2)
    
    for i in main.get_children():
         main.delete(i)

    count = 0
    for i in range(TrangHienTai*3-3 ,TrangHienTai*3):
            main.insert(parent='', index='end', iid=count, text='',
                        values=(i+1, file[i].get('id'), file[i].get('name')))
            if (count + 1 == len(file) - (TrangHienTai - 1)*3):
                     break
            count+=1 
    lblSoTrang.configure(text=TrangHienTai)

def tien():
    global TrangHienTai

    if len(file)/3 > 1:
         a = len(file)//3 + 1
    elif len(file) <= 1:
         a = 1
    
    if (TrangHienTai < a):
        TrangHienTai+=1

        for i in main.get_children():
            main.delete(i)

        lblSoTrang.configure(text=TrangHienTai)

        count = 0
        for i in range(TrangHienTai*3-3 ,TrangHienTai*3):
                main.insert(parent='', index='end', iid=count, text='',
                            values=(i+1, file[i].get('id'), file[i].get('name')))
                if (count + 1 == len(file) - (TrangHienTai - 1)*3):
                     break
                count+=1
        
def Lui():
    global TrangHienTai
    if (TrangHienTai > 1):
        TrangHienTai-=1

        for i in main.get_children():
            main.delete(i)

        count = 0
        for i in range(TrangHienTai*3-3 ,TrangHienTai*3):
                main.insert(parent='', index='end', iid=count, text='',
                            values=(i+1, file[i].get('id'), file[i].get('name')))
                count+=1
        
        lblSoTrang.configure(text=TrangHienTai)

def suamenu():
    childwin = Toplevel()
    childwin.title('Edit file')

    etrID = tk.Entry(childwin, textvariable=inputID)
    etrNAME = tk.Entry(childwin, textvariable=inputNAME)

    btnSUA = tk.Button(childwin, text="Edit", command=sua)

    etrID.pack()
    etrNAME.pack()

    btnSUA.pack()

def sua():
    global TrangHienTai
    global SearchResultIndexList
    global temp
    global SrcHinh

    imtem = main.selection()[0]

    if TrangHienTai == 0:
        file[SearchResultIndexList[int(imtem)]].update(
            {
                "id": inputID.get(),
                "name": inputNAME.get(),
                "src": file[SearchResultIndexList[int(imtem)]].get('src')
            }
        )
        TrangHienTai = temp
        inputTIM.set("")
    else:
        file[(TrangHienTai - 1)*3 + int(imtem)].update(
            {
                "id": inputID.get(),
                "name": inputNAME.get(),
                "src": file[(TrangHienTai - 1)*3 + int(imtem)].get('src')
            }
        )
         
    inputID.set("")
    inputNAME.set("")
    
    with open('data.json', "w", encoding='utf8') as f:
        json.dump(file, f, ensure_ascii=False, indent=2)
    
    for i in main.get_children():
         main.delete(i)

    count = 0
    for i in range(TrangHienTai*3-3 ,TrangHienTai*3):
            main.insert(parent='', index='end', iid=count, text='',
                        values=(i+1, file[i].get('id'), file[i].get('name')))
            if (count + 1 == len(file) - (TrangHienTai - 1)*3):
                     break
            count+=1
    SrcHinh = ""

def tim(*args):
    global TrangHienTai
    global SearchResultIndexList
    global temp

    SearchResultList = []
    if TrangHienTai != 0:
        temp = TrangHienTai
    
    for i in file:
         if (inputTIM.get() in i.get('name')):
            SearchResultIndexList.append(file.index(i))
            SearchResultList.append(i)

    for i in main.get_children():
        main.delete(i)
    
    if inputTIM.get() == "":
        count = 0
        TrangHienTai = temp
        for i in range(TrangHienTai*3-3 ,TrangHienTai*3):
            main.insert(parent='', index='end', iid=count, text='',
                        values=(i+1, file[i].get('id'), file[i].get('name')))
            if (count + 1 == len(file) - (TrangHienTai - 1)*3):
                    break
            count+=1
    else:   
        count = 0
        for i in range(len(SearchResultList)):
            main.insert(parent='', index='end', text='', iid=count,
                        values=(count+1, SearchResultList[i].get('id'), SearchResultList[i].get('name')))
            count+=1
        TrangHienTai = 0
inputTIM.trace("w",tim)              

def itemselected(event):
    global TrangHienTai
    global SearchResultIndexList
    global temp
    global  videoplayer

    videoplayer.stop()

    btnPLAY.configure(state='active')
    btnSTOP.configure(state='active')

    if len(main.selection()) != 0:
        item = main.selection()[0]

        if TrangHienTai == 0:
            videoplayer.load(file[SearchResultIndexList[int(item)]].get('src'))
            TrangHienTai = temp
        else:
            videoplayer.load(file[(TrangHienTai - 1)*3 + int(item)].get('src'))

    videoplayer.play()
    
def showimg(a):
    global videoplayer

    videoplayer.load(a)
    videoplayer.play()

main.bind("<<TreeviewSelect>>", itemselected)

def themanh():
    global TrangHienTai
    global temp
    global SearchResultIndexList
    global SrcHinh

    tk.Tk().withdraw()
    fn = askopenfilename()
    showimg(fn)
    SrcHinh = fn

def play():
    global videoplayer
    videoplayer.play()

def pause():
    global videoplayer
    videoplayer.pause()

def stop():
    global  videoplayer
    videoplayer.stop()

def play_pause():
    if videoplayer.is_paused():
        videoplayer.play()
    else:
        videoplayer.pause()

def update_duration(event):
    duration = videoplayer.video_info()["duration"]
    end_time.configure(text = str(datetime.timedelta(seconds=duration)))
    progress_slider["to"] = duration

def update_scale(event):
    progress_value.set(videoplayer.current_duration())
    current_time.configure(text=str(datetime.timedelta(seconds=int(progress_value.get()) + 1)))

def seek(value):
    videoplayer.seek(int(value) + 2)

def skip(value):
    videoplayer.seek(int(progress_slider.get()) + value)
    progress_value.set(progress_slider.get() + value)

def video_ended(event):
    progress_slider.set(progress_slider["to"])
    progress_slider.set(0)
    current_time.configure(text=0)

#LABEL SECTION
lblSoTrang = tk.Label(PhanTrangFrame, text=TrangHienTai, width=5)
lblSTARTTIME = tk.Label(videocontrolframe, text=str(datetime.timedelta(seconds=0)))
end_time = tk.Label(videocontrolframe, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side='right')

current_time = tk.Label(videocontrolframe, text=str(datetime.timedelta(seconds=0)))
current_time.pack(side='left')

#SCALE SECTION
progress_value = tk.IntVar(test)
progress_slider = tk.Scale(test, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.pack(side="bottom", expand=False, fill='x')

#ENTRY SECTION
# etrID = tk.Entry(childwin, textvariable=inputID)
# etrNAME = tk.Entry(childwin, textvariable=inputNAME)
etrTIM = tk.Entry(PhanTrangFrame, textvariable=inputTIM, bg='#C0C0C0')

#BUTTON SECTION
#btnTHEMHINH = tk.Button(test, text="Add image", command=themanh)
# btnTHEM = tk.Button(childwin, text="Add", command=them)
btnXOA = tk.Button(test, text="Delete", command=xoa)
btnTien = tk.Button(PhanTrangFrame, text=">>", command=tien)
btnLui = tk.Button(PhanTrangFrame, text="<<", command=Lui)
btnSUA = tk.Button(test, text="edit", command=sua)
btnPLAY = tk.Button(videocontrolframe, text=">||", command=play_pause, width=5, state='disable')
btnSTOP = tk.Button(videocontrolframe, text="O", command=stop, width=5, state='disable')

btnSKIP5SEC = tk.Button(videocontrolframe, text='+5', command=lambda: skip(5))
btnSKIP5SEC.pack(side="right")
btnSKIP_5SEC = tk.Button(videocontrolframe, text='-5', command=lambda: skip(-5))
btnSKIP_5SEC.pack(side="left")

#LABEL PACKING SECTION
btnTien.grid(row=0, column=2)
lblSoTrang.grid(row=0, column=1)
btnLui.grid(row=0, column=0)
#lblSHOWFRAME.grid(row=0,column=0,columnspan=3)

#BUTTON PACKING SECTION
# btnTHEM.pack()
# btnXOA.pack()
# btnSUA.pack()
#btnTHEMHINH.pack()
btnPLAY.pack(side="left")
btnSTOP.pack(side="right")

#ENTRY PACKING SECTION
# etrID.pack()
# etrNAME.pack()
etrTIM.grid(row=1,column=1)

videoplayer.bind("<<Duration>>", update_duration)
videoplayer.bind("<<SecondChanged>>", update_scale)
videoplayer.bind("<<Ended>>", video_ended)

#MENU
def donothing():
     pass

menubar = Menu(test)
# frame = Frame(test)
# frame.place(x=20, y=20, width=500,height=500, )

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=themanh)
filemenu.add_command(label="Save", command=themmenu)
filemenu.add_command(label="Delete", command=xoa)
filemenu.add_command(label="Edit", command=suamenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=test.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Play", command=play)
editmenu.add_command(label="Pause", command=pause)
editmenu.add_command(label="Stop", command=stop)
menubar.add_cascade(label="Playback", menu=editmenu)

test.config(menu=menubar)
test.mainloop()