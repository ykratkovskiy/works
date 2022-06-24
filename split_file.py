import tkinter as tk
from tkinter import E,W, messagebox, VERTICAL
from tkinter import  StringVar, filedialog
from os import path
import time


window = tk.Tk()
window.resizable(width=True, height=True)
window.geometry('640x980+560+30')
window.title('Отчет по прямой маркировке (разбивка на роли)')
window.iconbitmap('/build/split_file/og_img.ico')


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = tk.Canvas(window,borderwidth=0)
canvas.pack(side='left',fill='both',expand=True)
frame =tk.Frame(canvas)
scrollbar = tk.Scrollbar(window,orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side='right',fill='y')
canvas.configure(yscrollcommand=scrollbar.set)

canvas.create_window((4,4),window=frame)
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))



source_label_msg = tk.Label(frame, text='Выберите исходный файл для разбивки',foreground='maroon',font=('Arial',14))
source_label_msg.grid(row=0, columnspan=4,pady=5)

def source_button():
    filename = filedialog.askopenfilename()
    source_path.set(filename)
source_buttn = tk.Button(frame,text='Выбрать', command=source_button,width=16,height=1,foreground='maroon')
source_buttn.grid(row=1, columnspan=4,padx=5,pady=5)

source_path = StringVar()
source_label = tk.Label(frame,textvariable=source_path,foreground='maroon',font=('Arial',14))
source_label.grid(row=2, columnspan=4)



target_label_msg = tk.Label(frame, text='Выберите директорию для готовых файлов',foreground='royalblue1',font=('Arial',14))
target_label_msg.grid(row=3, columnspan=4)

def target_button():
    pathdirectory = filedialog.askdirectory()
    target_path.set(pathdirectory)
target_buttn = tk.Button(frame,text='Выбрать', command=target_button,width=16,height=1,foreground='royalblue1')
target_buttn.grid(row=4, columnspan=4,padx=5,pady=5)

target_path = StringVar()
target_label = tk.Label(frame,textvariable=target_path,foreground='royalblue1',font=('Arial',14))
target_label.grid(row=5, columnspan=4)


label = tk.Label(frame, text='Введите номера первого и последнено роля в диапазоне',foreground='darkgreen',font=('Arial',14))
label.grid(row=6, columnspan=4,padx=10)

label_min = tk.Label(frame, text='Первый:',foreground='darkgreen',font=14)
label_min.grid(row=7, column=0,sticky=E)
rol_min = tk.Entry(frame, width=5)
rol_min.grid(row=7, column=1,sticky=W)

label_max = tk.Label(frame, text='Последний:',foreground='darkgreen',font=14)
label_max.grid(row=7, column=2,sticky=E)
rol_max = tk.Entry(frame, width=5)
rol_max.grid(row=7, column=3,sticky=W)


my_entries = []
helplist =[]
list_of_numbers = []


def enter_button():
    try:
        rol_minint = int(rol_min.get())
        rol_maxint = int(rol_max.get())
        for number_of_rol in range (rol_minint,rol_maxint+1):
            list_of_numbers.append(number_of_rol)
        if rol_maxint<0 or rol_minint<0:
            messagebox.showerror(title='Error!', message=f'Значения не могут быть отрицательными!',onclick=window.quit())
        if rol_maxint<=rol_minint:
            messagebox.showerror(title='Error!', message=f'Значение "первого" роля должно быть меньше значения "второго" роля!')
        for i in range (rol_minint-1,rol_maxint):
            label_rols = tk.Label(frame, text=f'Введите количество кодов в роле № {i+1}').grid(row=i+10, column=1,sticky=E)
            entry_mult = tk.Entry(frame,width=10)
            entry_mult.grid(row=i+10, column=2,sticky=W)
            helplist.append(entry_mult)
            button_apply_values = tk.Button(
            frame, text='Запустить программу', command=write_and_run).grid(row=((rol_maxint-rol_minint)+1000), columnspan=4,pady=15)  
    except ValueError:
        messagebox.showerror(title='Error!', message=f'Введенным значением должно быть целое положительное число!')
        
   
button_enter = tk.Button(
frame, text='Ввести',command=enter_button,width=8,height=1,foreground='darkgreen').grid(row=7, columnspan=4,padx=10,pady=15)



def write_and_run():
    try:
        start_time = time.time()
        global full_name
        global name
        c=0
        for entries in helplist:
            try:
                my_entries.append(int(entries.get()))
            except ValueError:
                messagebox.showerror(title='Error!', message=f'Значением кодов в роле должно быть целое положительное число!')
                break
            for value in my_entries:
                if value < 0:
                    messagebox.showerror(title='Error!', message=f'Значением кодов в роле должно быть целое положительное число!')
                    break
    
        src = source_path.get()
        trg = target_path.get()
    
        full_name = path.basename(f'{src}')
        name = path.splitext(full_name)[0]
        dir_path = path.dirname(src)

        list_of_quantity_of_entries = []
        count = 0
        for entry in my_entries:
            list_of_quantity_of_entries.append(count)
            count+=1
            
    
        original_file = open(f'{dir_path}/{full_name}','r')
        for entries_count,number_of_rols in zip(list_of_quantity_of_entries,list_of_numbers):
                new_file = open(f'{trg}/{name} rol {number_of_rols}.txt', 'w')
                c = my_entries[entries_count]
                for j in range (1,c+1):
                    new_file.write(original_file.readline())
        original_file.close()
        new_file.close()
        messagebox.showinfo(title='Выполнено', message=f'Успешно выполнено за {round (time.time()-start_time,2)} сек',onclick=window.quit())
    
    except PermissionError:
        messagebox.showerror(title='Ошибка!', message=f'Не выбран исходный файл или директория для готовых файлов')


window.mainloop()