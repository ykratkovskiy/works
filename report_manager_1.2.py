import tkinter as tk
from tkinter import  StringVar, filedialog
import os
from tkinter import messagebox
import shutil
import re
import time


window = tk.Tk()
window.title('Report manager')
window.geometry('460x180+600+200')
window.resizable(width=True, height=True)


def source_button():
    filename = filedialog.askdirectory()
    source_path.set(filename)
    
source_path = StringVar()
source_label = tk.Label(textvariable=source_path)
source_label.grid(row=2, column=1)

source_buttn = tk.Button(text="Select source folder", command=source_button,width=16,height=1)
source_buttn.grid(row=2, column=0)


def target_button():
    filename = filedialog.askdirectory()
    target_path.set(filename)
    
target_path = StringVar()
target_label = tk.Label(textvariable=target_path)
target_label.grid(row=4, column=1)

target_buttn = tk.Button(text="Select target folder", command=target_button,width=16,height=1)
target_buttn.grid(row=4, column=0)


head_label = tk.Label(
                text='Report manager tool', 
                font=36,
                fg='turquoise3',
                
                )
head_label.grid(row=0, column=0)


def report_manager():
    start_time = time.time()
    try:
        path = source_path.get()
        list_of_files = sorted(os.listdir(path))
    

        global num_of_codes
        global num_of_noreads
        num_of_codes = []
        num_of_noreads = []
        lst_of_rols = []
    
        global src
        global trg
        src = source_path.get()
        trg = target_path.get()
        
        for file in list_of_files:
            if 'vse' in file:
                name = re.split(r'vse', file)[0]
                ext = re.split(r'vse', file)[1]
                global name_for_rep
                name_for_rep = re.split(r'%', name)[0]
                
                rol_number_help1 = re.findall(r'[\d\d]+_+', name)
                rol_number_help2 = ''.join(rol_number_help1)
                rol_number = re.split(r'_+',rol_number_help2)[0]
                
                noread_count=0
                count_of_codes = 0
                original_file = open(f'{src}/{file}','r')
                new_file = open(f'{trg}/{name}MOD{ext}', 'w')
                for line in original_file:
                    if not line.startswith('NOREAD'):
                        count_of_codes+=1
                        new_file.write(line)
                    else:
                        noread_count+=1
                new_file.close()
                num_of_codes.append(count_of_codes)
                num_of_noreads.append(noread_count)
                lst_of_rols.append(rol_number)
        stat_file = open (f'{trg}/{name_for_rep}%_STAT.txt', 'w')
        for rol_id,codes in zip (lst_of_rols,num_of_codes):
            rol_str = ''.join(rol_id)
            stat_file.writelines(f'Rol {rol_str} - {codes} codes\n')
        stat_file.write(f'Total codes used: {sum(num_of_codes)}\n')
        # stat_file.write(f'Total number of NOREAD\'s deleted: {sum(num_of_noreads)}')
        stat_file.close()
        original_file.close()
        messagebox.showinfo(title='Success!', message=f'Done in {round (time.time()-start_time,2)} sec')
        
    except FileNotFoundError:
        messagebox.showerror(title='Error!', message=f"Source folder hasn't been selected")
    except NameError:
        messagebox.showerror(title='Error!', message=f'No appropriate data found in source folder')
    except PermissionError:
        messagebox.showerror(title='Error!', message=f"Target folder hasn't been selected")
    

start_buttn = tk.Button(
                text = 'Start',
                font=20,
                width = 13,
                height = 1,
                bg = 'gray85',
                fg = 'gray10', 
                command=report_manager)
start_buttn.grid(row=6, column=1)


def archive_button():
    start_time=time.time()
    try:
        shutil.make_archive(f'{src}/{name_for_rep}%','zip', root_dir=None, base_dir=trg)
    except NameError:
        messagebox.showerror(title='Error!', message=f'No data to archivation found')
    else:
        messagebox.showerror(title=f'Success!', message=f'Done in {round (time.time()-start_time,2)} sec')
    

archive_buttn = tk.Button(text="Archive files", 
                    command=archive_button,
                    width=13,
                    height=1,
                    )
archive_buttn.grid(row=12, column=1)


window.mainloop()