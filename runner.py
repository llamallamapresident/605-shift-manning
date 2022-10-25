import tkinter as tk
import tkinter.filedialog as filedialog
from main import main

master = tk.Tk()
input_namelist_path = None
input_dutylist_path = None

def input_namelist():
    global input_namelist_path 
    input_namelist_path  = filedialog.askopenfilename()
    input_namelist_entry.delete(1, tk.END)  # Remove current text in entry
    input_namelist_entry.insert(0, input_namelist_path)  # Insert the 'path'


def input_dutylist():
    global input_dutylist_path 
    input_dutylist_path = filedialog.askopenfilename()
    input_dutylist_entry.delete(1, tk.END)  # Remove current text in entry
    input_dutylist_entry.insert(0, input_dutylist_path)  # Insert the 'path'


def begin():
    output_namelist_name = output_namelist_entry.get()
    output_dutylist_name = output_dutylist_entry.get()
    main(input_namelist_path, input_dutylist_path, output_namelist_name, output_dutylist_name)


# tkinter things
top_frame = tk.Frame(master)
bottom_frame = tk.Frame(master)
line = tk.Frame(master, height=1, width=400, bg="grey80", relief='groove')

input_namelist_text = tk.Label(top_frame, text="Input namelist (.csv file only!):")
input_namelist_entry = tk.Entry(top_frame, text="", width=40)
browse1 = tk.Button(top_frame, text="Browse", command=input_namelist)

input_dutylist_text = tk.Label(top_frame, text="Input dutylist (.csv file only!):")
input_dutylist_entry = tk.Entry(top_frame, text="", width=40)
browse2 = tk.Button(top_frame, text="Browse", command=input_dutylist)

output_namelist_text = tk.Label(top_frame, text="Output namelist (filename.csv):")
output_namelist_entry = tk.Entry(top_frame, text="output_namelist", width=40)

output_dutylist_text = tk.Label(top_frame, text="Output dutylist (filename.csv):")
output_dutylist_entry = tk.Entry(top_frame, text="output_dutylist", width=40)

begin_button = tk.Button(bottom_frame, text='Begin!', command=begin)

# Style
top_frame.pack(side=tk.TOP)
line.pack(pady=10)
bottom_frame.pack(side=tk.BOTTOM)

input_namelist_text.pack(pady=5)
input_namelist_entry.pack(pady=5)
browse1.pack(pady=5)

input_dutylist_text.pack(pady=5)
input_dutylist_entry.pack(pady=5)
browse2.pack(pady=5)

output_namelist_text.pack(pady=5)
output_namelist_entry.pack(pady=5)

output_dutylist_text.pack(pady=5)
output_dutylist_entry.pack(pady=5)

begin_button.pack(pady=20, fill=tk.X)

master.mainloop()