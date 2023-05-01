from tkinter import *
from os.path import *
from os import *
import json, shutil, threading, time
from PIL import ImageTk,Image

flag = threading.Event()

main_path = realpath(dirname(__name__)) 
extensions = {
    'video': ['mp4', 'mov', 'avi', 'mkv', 'mpg', 'mpeg', 'm4v', ],
    'audio': ['mp3', 'wav'],
    'image': ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 'gif','tiff'],
    'documents': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'tex', 'wpd', 'odt'],
    'Source code': ['py','CPP', 'java']
    }

class Sorting():
    def timer(LabelVar):
        second = 0
        minut = 0
        time.sleep(1)
        while True:
            flag.wait()
            second += 1
            minut = second // 60
            time.sleep(1)
            LabelVar.set(f"time work: {minut}:{second}")

    def sort():
        while True:
            flag.wait()
            def create_folders_from_list(folder_path, folder_names):
                for folder in folder_names:
                    if not exists(f'{folder_path}/{folder}'):
                        mkdir(f'{folder_path}/{folder}')

            def get_subfolder_names(folder_path) -> list:
                subfolder_paths = get_subfolder_paths(folder_path)
                subfolder_names = [f.split('/')[-1] for f in subfolder_paths]
                return subfolder_names

            def get_file_paths(folder_path) -> list:
                file_paths = [f.path for f in scandir(folder_path) if not f.is_dir()]
                return file_paths

            def sort_files(folder_path):
                file_paths = get_file_paths(folder_path)
                ext_list = list(extensions.items())
                for file_path in file_paths:
                    extension = file_path.split('.')[-1]
                    file_name = file_path.split('/')[-1]        
                    for dict_key_int in range(len(ext_list)):
                        if extension in ext_list[dict_key_int][1]:
                            print(f'Moving {file_name} in {ext_list[dict_key_int][0]} folder\n')
                            rename(file_path, f'{main_path}/{ext_list[dict_key_int][0]}/{file_name}')

            create_folders_from_list(main_path, extensions)
            sort_files(main_path)
            time.sleep(60)  

class GUI():
    def __init__(self, master):
        self.master = master
        self.master.title("Sorting file")
        self.master.geometry("320x210")
        self.master.resizable(False,False)

        menubar = Menu(master)
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="info", command=self.open_infoWindow)
        menubar.add_cascade(label="File", menu=fileMenu)
        master.config(menu=menubar)

        ButtonStart = Button(self.master,text="Start", command=flag.set)
        ButtonStop = Button(self.master,text="Stop",command=flag.clear)
        phantomImage = ImageTk.PhotoImage(Image.new("RGB", (1,1), (0,0,1)))
        LabelLine = Label(self.master, image=phantomImage,bg="black", width=280, height=1)
        LabelVar = StringVar(value="time work: 00:00")
        LabelTimer = Label(self.master,textvariable=LabelVar)

        LabelTimer.pack()
        LabelLine.pack(side="top")
        ButtonStart.pack(side="right", padx=10, pady=10)
        ButtonStop.pack(side="left", padx=10, pady=10)

        threadTimer = threading.Thread(target=Sorting.timer,args=[LabelVar])
        threadTimer.start()
        threadSort = threading.Thread(target=Sorting.sort)
        threadSort.start()

        self.master.mainloop()

    def open_infoWindow(self,width=400,height=100):
        window = Toplevel(self.master)
        window.title("Info window")
        window.geometry('{}x{}'.format(width,height))
        window.resizable(False,False)

        LabelInfo = Label(window, text="Is programm writing is EternalSlow. If my program caused an error, \nthen write to this email: \nnikslastd@gmail.com")
        ButtonClose = Button(window,text="close window", command=window.destroy)
        LabelInfo.pack()
        ButtonClose.pack()

if __name__ == "__main__":
    root = Tk()
    print(root)
    app = GUI(root)

