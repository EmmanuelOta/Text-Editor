from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import font
from tkinter import messagebox

root = Tk()
root.title("Europad")
root.iconbitmap("Python/Text-Editor/Notepad.ico")
root.geometry("1200x680")

global selected
selected = False

global open_status_name
open_status_name = False

#File menu

def open_file():
    global text
    global root
    filepath = askopenfilename(filetype=[("Text Documents", ".txt"), ("All Files", "*.*")],
                               defaultextension=".txt", title="Choose a file:")

    splitted_filepath = filepath.split("/")
    doc_name = splitted_filepath[5]
    status_bar.config(text=f"{doc_name        }")

    if not filepath:
        return 

    if filepath:
        global open_status_name
        open_status_name = filepath

    with open(filepath, "r") as file:
        data = file.read()
        text.insert(END, data)
        file.close()
    root.title(f"Notepad-{doc_name}")


def save_as_file():
    global text
    global root
    filepath = asksaveasfilename(filetype=[("Text Documents", ".txt"), ("All Files", "*.*")],
                                 title="Save file:", defaultextension=".txt")

    slitted_filepath = filepath.split("/")
    doc_name = slitted_filepath[5]
    status_bar.config(text=f"Saved: {doc_name}")

    if not filepath:
        return
    
    with open(filepath, "w") as file:
        data = text.get(1.0, END)
        file.write(data)
        file.close()
    messagebox.showinfo("saved", "File Saved Successfully!")
    root.title(f"Notes-{doc_name}")


def new_file():
    global text
    global root
    text.delete(1.0, END)
    root.title("Notepad-Untitled.txt")
    status_bar.config(text="Untitled.txt        ")
    global open_status_name
    open_status_name = False


def save_file():
    global text
    global root
    global open_status_name

    if open_status_name:
        with open(open_status_name, "w") as file:
            data = text.get(1.0, END)
            file.write(data)
            file.close()
            status_bar.config(text=f"Saved: {open_status_name}        ")
            messagebox.showinfo("saved", "File Saved Successfully!")

    else:
        save_as_file()

    root.title(f"Notes-{open_status_name}")


#Edit menu

def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    else:
        if text.selection_get():
            selected = text.selection_get()
            text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if text.selection_get():
        selected = text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)

def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)


frame = Frame(root)
frame.pack(fill="both", expand=True, pady=5)

text_scroll = Scrollbar(frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(frame, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)


text = Text(frame, width=200, height=41, font=("Consolas", 10), selectbackground="light blue", 
            selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", 
            xscrollcommand=hor_scroll.set)
text.pack()

text_scroll.config(command=text.yview)
hor_scroll.config(command=text.xview)

menu = Menu(root)
file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=lambda: new_file())
file_menu.add_separator()
file_menu.add_command(label="Open", command=lambda: open_file())
file_menu.add_separator()
file_menu.add_command(label="Save", command=lambda: save_file())
file_menu.add_separator()
file_menu.add_command(label="Save as", command=lambda: save_as_file())
file_menu.add_separator()
file_menu.add_command(label="Exit", command=lambda: root.destroy())

edit_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_separator()
edit_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_separator()
edit_menu.add_command(label="Redo", command=text.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_separator()

status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15, )

root.config(menu=menu)

root.bind("<Control-Key-x>", cut_text)
root.bind("<Control-Key-c>", copy_text)
root.bind("<Control-Key-v>", paste_text)

root.mainloop()
