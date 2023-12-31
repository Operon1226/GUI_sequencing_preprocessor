#!/usr/bin/python3 

import tkinter as tk
from tkinter import messagebox, filedialog, font
import subprocess as sp
import math

class PopupWindow:
    def __init__(self, mainframe):
        self.mainframe = mainframe
        self.popup = None
        self.user_input = ""
        self.selected_values = []
    
    def popup_input(self,title,detail):
        self.popup = tk.Toplevel(self.mainframe)
        self.popup.protocol("WM_DELETE_WINDOW", self.popup_destroy)
        self.popup.geometry("800x150")
        self.popup.title(title)
        self.popup.resizable(True,True)
        self.user_input = ""
        label = tk.Label(self.popup,text=detail,font=("Helvetica",15))
        label.pack()
        
        entry = tk.Entry(self.popup)
        entry.pack()
        
        def get_input():
            self.user_input = entry.get()
            self.popup_destroy()
        
        button = tk.Button(self.popup,text="OK",command=get_input)
        button.pack()
        self.mainframe.wait_window(self.popup)
    
    def popup_checkbox_without_additional_input(self,title,detail,values):
        self.values = values
        self.popup = tk.Toplevel(self.mainframe)
        height_popup = math.ceil(len(values)/2) * 60 + 130
        enters = 0
        width_popup = 0
        for i in range(len(values)):
            enters += values[i][1].count("\n")
            if len(values[i][1]) > width_popup:
                width_popup = len(values[i][1])
        width_popup = width_popup * 6 + 100
        if width_popup > 1300:
            width_popup = 1300
        if enters > 0:
            height_popup += (enters -1) * 33
        
        geometry_popup = str(width_popup) + "x" + str(height_popup)
        self.popup.geometry(geometry_popup)
        self.popup.title(title)
        self.popup.resizable(True,True)
        self.selected_values = []
        
        label = tk.Label(self.popup,text=detail,font=("Helvetica",15))
        label.pack()
        
        checkbox_vars = []
        def update_selected():
            self.selected_values.clear()
        
            for idx,value in enumerate(self.values):
                if checkbox_vars[idx].get():
                    self.selected_values.append([idx,value])
                else:
                    self.selected_values.append([idx,False])
        
        for value in self.values:
            var = tk.BooleanVar()
            checkbox_vars.append(var)
            checkbox = tk.Checkbutton(self.popup, text=value[0], variable=var, command=update_selected,font=("Helvetica",14),pady=2)
            checkbox.pack(anchor="w")
            description_label = tk.Label(self.popup, text=value[1], font=("Helvetica", 12),justify="left",padx=20)
            description_label.pack(anchor="w")
            
        button = tk.Button(self.popup,text="OK",command=self.popup_destroy,height=1,width=1)
        button.pack()
        self.mainframe.wait_window(self.popup)
       
    def popup_checkbox(self,title,detail,values):
        self.values = values
        self.popup = tk.Toplevel(self.mainframe)
        self.popup.protocol("WM_DELETE_WINDOW", self.popup_destroy)
        
        # window size settings
        height_popup = math.ceil(len(values)/2) * 60 + 130
        enters = 0
        width_popup = 0
        for i in range(len(values)):
            enters += values[i][1].count("\n")
            if len(values[i][1]) > width_popup:
                width_popup = len(values[i][1])
        width_popup = width_popup * 6 + 100
        if enters > 0:
            height_popup += (enters -1) * 33
        if ((width_popup > 1200) and (height_popup > 700)):
            width_popup = self.popup.winfo_screenwidth() - 100
            height_popup = self.popup.winfo_screenheight() - 100 
        elif width_popup > 1200:
            width_popup = 1200
        elif height_popup > 700:
            height_popup = 700
            
        x_coordinate = (self.popup.winfo_screenwidth()-width_popup) // 2
        y_coordinate = 0    
            
        geometry_popup = f"{width_popup}x{height_popup}+{x_coordinate}+{y_coordinate}"
        self.popup.geometry(geometry_popup)
        
        self.popup.title(title)
        self.popup.resizable(True,True)
        self.selected_values = []
        
        label = tk.Label(self.popup,text=detail,font=("Helvetica",15))
        label.pack()
    
        checkbox_vars = []
        entry_vars = []
        entry_widgets = []
        
        def update_selected():
            self.selected_values.clear()
            for idx,value in enumerate(self.values):
                if checkbox_vars[idx].get():
                    print(value)
                    print(entry_vars[idx].get())
                    selected_value = ([value[0],entry_vars[idx].get()])
                    self.selected_values.append(selected_value)
                toggle_entry(idx)  
                
        def toggle_entry(idx):
            if checkbox_vars[idx].get():
                entry_widgets[idx].pack(anchor="w",padx=25)
            else:
                entry_widgets[idx].pack_forget()
        
        # Scrollbar set
        scrollbar = tk.Scrollbar(self.popup)
        scrollbar.pack(side="right",fill="y")
        
        content_frame = tk.Frame(self.popup)
        content_frame.pack(fill="both",expand=True)
        
        # Since scrollbar can't bind to frame directly, canvas is used as a middleman
        canvas = tk.Canvas(content_frame,yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.config(command=canvas.yview)
        
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0,0),window=inner_frame,anchor="nw")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")  
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        for value in self.values:
            value_frame = tk.Frame(inner_frame)
            value_frame.pack(anchor="w",padx=5)
        
            var = tk.BooleanVar()
            checkbox_vars.append(var)
            checkbox = tk.Checkbutton(value_frame, text=value[0], variable=var, command=update_selected,font=("Helvetica",14),pady=2)
            checkbox.pack(side="top",anchor="w")
            
            description_label = tk.Label(value_frame, text=value[1], font=("Helvetica", 12),justify="left",padx=20)
            description_label.pack(anchor="w")
          
            entry_var = tk.StringVar()
            entry_vars.append(entry_var)
            entry = tk.Entry(value_frame,textvariable=entry_var,font=("Helvetica",12))
            entry_widgets.append(entry)
            
        inner_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        def update_destroy():
            update_selected()
            self.popup.destroy()
            self.popup = None
        
        button = tk.Button(self.popup,text="OK",command=update_destroy,height=1,width=4)
        button.pack(anchor='s')
            
        self.mainframe.wait_window(self.popup)
        
        
    def popup_wait(self,name):
        self.popup = tk.Toplevel(self.mainframe)
        self.popup.geometry("800x100")
        self.popup.title(name)
        label = tk.Label(self.popup,text="Running command")
        label.pack()
        self.popup.update()
        
    def popup_destroy(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None

class TextModule:
    def __init__(self, mainframe):
        self.text = tk.Text(mainframe,width=1000,height=600)
        self.text.pack()
    
    def set_font(self,font_name,font_size):
        new_font = font.Font(family=font_name, size=font_size)
        self.text.configure(font=new_font)
    
    # added file_paths to parameter
    def update_file_paths_display(self,file_paths):
        if len(file_paths) != 0:
            self.text.insert(tk.END, "Imported files\n")
        for file_path in file_paths:
            self.text.insert(tk.END, file_path + "\n") # Append each file path
            
    def update_info_to_display(self,text):
        self.text.insert(tk.END, text + "\n")
        
    def clear_info_to_display(self):
        self.text.delete(1.0, tk.END)

class FileMenu(tk.Menu):
    def __init__(self, parent,text_module,popup_window):
        super().__init__(parent,tearoff=False)
        self.text_module = text_module
        self.popup_window = popup_window
        self.add_command(label="Open", command=self.open_file_explorer)
        self.add_command(label="Set output directory", command=self.outdir)
        self.add_separator()
        self.add_command(label="Exit", command=self.exit_program)
        self.file_paths = []
        self.processes = []
        self.outdir_path = ""
        
    def open_file_explorer(self):
        self.file_paths = []
        paths = filedialog.askopenfilenames()
        self.file_paths.extend(paths)
        self.text_module.clear_info_to_display()
        self.text_module.update_file_paths_display(self.file_paths)
        self.operation_menu.file_paths = self.file_paths
        self.crispresso_menu.file_paths = self.file_paths
    
    def exit_program(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.master.destroy()
            self.master.quit() 
            for process in self.processes:
                process.terminate()

    def outdir(self):
        self.outdir_path = ""
        self.popup_window.popup_input("Set output directory","Input output directory path.")
        self.outdir_path = self.popup_window.user_input
        
        try:
            sp.run(["ls",self.outdir_path],check=True,stdout=sp.PIPE,stderr=sp.PIPE)
        except sp.CalledProcessError:
            print(f"The directory '{self.outdir}' doesn't exist.")
            print("Please input the correct directory path.")
            self.outdir()
        
        self.operation_menu.outdir_path = self.outdir_path
        self.cripresso_menu.outdir_path = self.outdir_path
        
class OperationMenu(tk.Menu):
    def __init__(self, parent,text_module,popup_window,file_paths,outdir_path):
        self.inherited(parent,text_module,popup_window,file_paths,outdir_path)
        self.add_command(label = "Adapter trimming", command = self.adapter_trimming)
        self.add_command(label = "Mapping", command = self.mapping)
        self.add_command(label = "Remove unwanted reads", command = self.remove_unwanted_reads)
        self.add_command(label = "Convert sam to bam", command = self.convert_sam_to_bam)
        self.add_command(label = "Remove PCR duplicates", command = self.remove_pcr_duplicates)
        self.add_command(label = "Convert to bedgraph and bigwig", command = self.convert_to_bedgraph_and_bigwig)

    def inherited(self,parent,text_module,popup_window,file_paths,outdir_path):
        super().__init__(parent,tearoff=False)
        self.text_module = text_module
        self.popup_window = popup_window
        self.file_paths = file_paths
        self.outdir_path = outdir_path
        self.file_name = []
        self.file_extension = []
        self.file_directory = []
        self.processes = []
        self.space = " "
        self.file_full_name = []

    def directory_making(self,name):
        try:
            command = 'mkdir ' + name
            output = sp.Popen(command,shell=True,universal_newlines=True,stdout=sp.PIPE, stderr=sp.PIPE)
            (stdout,stderr) = output.communicate()
            
            if stderr != "":
                self.popup_window.popup_input("Directory checking",name+" already exists. \nIf you want to save results in that directory, input ok")
                dircheck = self.popup_window.user_input
                if dircheck != "ok":
                    self.text_module.update_info_to_display("Error occured, please check the error message below")
                    self.text_module.update_info_to_display(stderr)
                    self.init()
                    return (stderr, dircheck)
                else:
                    return (stderr, dircheck)
            else:
                return (stderr, "ok")
            
        except sp.CallledProcessError as e:
            print(f"Command execution failed with return code {e.returncode}")
            print(f"Error message: {e.output}")
            self.text_module.update_info_to_display(f"Command execution failed with return code {e.returncode}")
            self.text_module.update_info_to_display(f"Error message: {e.output}")
    
    def init(self):
        self.file_name = []
        self.file_extension = []
        self.file_directory = []
    
    def overwrite_warn(self,files_paths):
        command = f"ls {files_paths}"
        result = sp.run(command,shell=True,capture_output=True,text=True)
        if result.returncode == 0:
            self.text_module.update_info_to_display(f"Warning: {files_paths} already exists.")
            self.popup_window.popup_input("Overwrite warning",f"{files_paths} already exists. \nIf you want to overwrite, input ok")
            overwrite_check = self.popup_window.user_input
            if overwrite_check != "ok":
                self.text_module.update_info_to_display("command terminated")
                self.init()
                return False
        else:
            return True
        
    def name_proccessing(self):
        self.init()
        if self.file_paths == []:
            self.text_module.update_info_to_display("Please select files before running the processes")
            return False
        for i in range(len(self.file_paths)):
            self.file_name.append(self.file_paths[i].split("/"))
            self.file_name[i] = self.file_name[i][len(self.file_name[i])-1]
            self.file_full_name.append(self.file_name[i])
            self.file_name[i] = self.file_name[i].split(".")
            self.file_extension.append(self.file_name[i])
            self.file_name[i] = self.file_name[i][0]
            self.file_name[i] = self.file_name[i].split("_")
            if self.file_extension[i][len(self.file_extension[i])-1] == "gz":
                self.file_extension[i] = self.file_extension[i][len(self.file_extension[i])-2] + "." + self.file_extension[i][len(self.file_extension[i])-1]
            else:
                self.file_extension[i] = self.file_extension[i][len(self.file_extension[i])-1]
            self.file_directory.append(self.file_paths[i].split("/"))
            self.file_directory[i] = self.file_directory[i][0:len(self.file_directory[i])-1]
            self.file_directory[i] = '/'.join(self.file_directory[i])
             
    def directory_processing(self,directory):
        self.directory = directory
        
        # Directory checking
        value = True
        for i in range(1,len(self.directory)):
            if self.directory[0] != self.directory[i]:
                value = False
                break
        
        if self.outdir_path != "":
            self.directory = self.outdir_path
        else:
            # When all files aren't in the same directory, input the saving directory
            if value == False:
                self.popup_window.popup_input("Output directory","Input output directory as absolute path")
                self.directory = self.popup_window.user_input
            else:
                self.directory = self.directory[0]  
        
        return self.directory

    def run_command(self,command):
        try:
            self.popup_window.popup_wait("Running")
        
            output = sp.Popen(command, shell=True, universal_newlines=True,stdout=sp.PIPE, stderr=sp.PIPE)    
            self.processes.append(output)
            # HERE
            self.file_menu.processes = self.processes
            (stdout,stderr) = output.communicate()
            
            output.wait()           
            self.popup_window.popup_destroy()
            self.processes.remove(output)
            
            if stderr != "":
                return stderr
            
        except sp.CalledProcessError as e:
            print(f"Command execution failed with return code {e.returncode}")
            print(f"Error message: {e.output}")
            self.text_module.update_info_to_display(f"Command execution failed with return code {e.returncode}")
            self.text_module.update_info_to_display(f"Error message: {e.output}")

    def check_threads(self):
        mthreads = sp.run("nproc",shell=True,capture_output=True,text=True)
        rthreads = sp.run("top -bn1 | awk \'NR>7 { sum += $9 } END { print sum }\'",shell=True,capture_output=True,text=True)
        mthreads = float(mthreads.stdout)
        rthreads = float(rthreads.stdout)
        rthreads = math.ceil(rthreads / 100)
        athreads = mthreads - rthreads
        comment = "Input threads for running this task\nAvailable threads are %f\nUsing a lot of threads doesn't always speed up." % athreads
        # Threads
        self.popup_window.popup_input("Threads for this task",comment)
        threads = self.popup_window.user_input
        a = int(threads)
        if a <= athreads:
            return threads
        else:
            self.text_module.update_info_to_display("The input value is more than the available number. Please enter it again")
            self.check_threads()

    def adapter_trimming(self): 
        
        self.text_module.clear_info_to_display()
        
        name_processing_check = self.name_proccessing()
        if name_processing_check == False:
            return 1
        
        self.file_directory = self.directory_processing(self.file_directory)
        
        #Error processing
        if (len(self.file_name) > 2):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if (self.file_name[0][0] != self.file_name[0][0]):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Files are not paired")
            return 1
        if not(((self.file_extension[0] and self.file_extension[1]) == "fastq") or ((self.file_extension[0] and self.file_extension[1]) == "fastq.gz")):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
          
        #directory processing    
        outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
        (dcommand_a,dircheck_a) = self.directory_making(outdir)
        if dcommand_a != None:
            if dircheck_a != "ok":
                return 1
        outdir_adp = outdir+"adapter_trimming/"
        (dcommand_b,dircheck_b) = self.directory_making(outdir_adp)
        if dcommand_b != None:
            if dircheck_b != "ok":
                return 1
            
        out_f1 = outdir_adp + self.file_name[0][0] + "_" + self.file_name[0][1] + ".trim" + ".fastq"
        out_f2 = outdir_adp + self.file_name[1][0] + "_" + self.file_name[1][1] + ".trim" + ".fastq"
        
        ov_out_f1 = self.overwrite_warn(out_f1)
        ov_out_f2 = self.overwrite_warn(out_f2)
        
        if ov_out_f1 == False or ov_out_f2 == False:
            self.init()
            return 1
        
        # 3' R1 adapter sequence
        self.popup_window.popup_input("Adapter sequence R1","3\' adapter to be removed from R1\nIf you want to use \"CTGTCTCTTATACACATCT\", enter ok")
        adapter1 = self.popup_window.user_input
        if adapter1 == "ok":
            adapter1 = "CTGTCTCTTATACACATCT"
        # 3' R2 adapter sequence
        self.popup_window.popup_input("Adapter sequence R2","3\' adapter to be removed from R2\nIf you want to use \"CTGTCTCTTATACACATCT\", enter ok")
        adapter2 = self.popup_window.user_input
        if adapter2 == "ok":
            adapter2 = "CTGTCTCTTATACACATCT"
        
        threads = self.check_threads()
        
        #command processing
        command = (
            "cutadapt " + "-a " + adapter1 +  self.space +  "-A " + adapter2 + self.space + 
            "-m 5" + self.space + "--nextseq-trim=20" + self.space + "-j " + threads + self.space +
            "-o " + out_f1 + self.space + "-p " + out_f2 + self.space + 
            self.file_paths[0] + self.space + self.file_paths[1] + self.space +
            "> "+ outdir_adp + self.file_name[1][0] + ".trim.log"
        )
        
        rcommand = self.run_command(command)
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.text_module.update_info_to_display("Error occured, please check the error message below")
            self.text_module.update_info_to_display(rcommand)
            stderrfile = open(outdir_adp+"Error_message.txt","w+")
            stderrfile.write(rcommand)
            stderrfile.close()
            self.text_module.update_info_to_display("Error message are saved in "+outdir_adp+"Error_message.txt")
            self.init()
            return 1
        
        self.text_module.update_info_to_display(
            "Executed command are "+ command + "\nAdapter trimming is done\nOutputs and log are saved in " + self.file_name[1][0] + ".processed_files/adapter_trimming directory\n"
            "log file name is " + self.file_name[1][0] + ".trim.log"
        )
        
    def mapping(self):
        
        self.text_module.clear_info_to_display()
        
        name_processing_check = self.name_proccessing()
        if name_processing_check == False:
            return 1
        
        # error processing
        if (len(self.file_name) > 2):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if (self.file_name[0][0] != self.file_name[1][0]):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Files are not paired")
            return 1
        if not((self.file_extension[0] and self.file_extension[1]) == "fastq"):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
        
        test = []
        dir = 0
        for i in range(len(self.file_paths)):
            test.append(self.file_paths[i].split("/"))
            if (test[i][len(test[i])-2] == "adapter_trimming") and (test[i][len(test[i])-3] == (self.file_name[0][0] + ".processed_files")):
                del test[i][len(test[i])-1]
                test[i][len(test[i])-1] = 'mapping/'
                test[i] = "/".join(test[i])
            else:
                dir += 1
        if dir != 0:
            self.file_directory = self.directory_processing(self.file_directory)
            outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
            (dcommand_a,dircheck_a) = self.directory_making(outdir)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1
            outdir_map = outdir + "mapping/"
            (dcommand_b,dircheck_b) = self.directory_making(outdir_map)
            if dcommand_b != None:
                if dircheck_b != "ok":
                    return 1
        else:
            outdir_map = self.directory_processing(test)
            (dcommand_a,dircheck_a) = self.directory_making(outdir_map)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1

        #Reference genome setting
        self.popup_window.popup_input("Reference genome","Input reference genome path as absolute path\nIf you want to use \"/seq/Ref/Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome\", enter ok")
        refpath = self.popup_window.user_input
        if refpath == "ok":
            refpath = "/seq/Ref/Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome"
          
        # Overwrite checking
        out_sam = outdir_map + self.file_name[1][0] + ".sam"
        ov_out_sam = self.overwrite_warn(out_sam)
        if ov_out_sam == False:
            self.init()
            return 1
        
        threads = self.check_threads()
        
        # Command processing
        command = (
            "bowtie2 " + "--very-sensitive" +self.space + "-p " + threads + self.space +
            "-x " + "/seq/Ref/Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome" + self.space + 
            "-1 " + self.file_paths[0] + self.space +
            "-2 " + self.file_paths[1] + self.space +
            "-S " + out_sam + self.space + 
            "--rg-id " + self.file_name[0][0] + self.space +
            "> "+ outdir_map + self.file_name[0][0] + ".mapping.log"
            
        )
        
        # samtools & bowtie2 return result as stderr
        rcommand = self.run_command(command)
        stderrfile = open(outdir_map+self.file_name[0][0]+".mapping.log","w+")
        stderrfile.write(rcommand)
        stderrfile.close()
        self.text_module.update_info_to_display(
            "Executed command are "+ command + "\nMapping is done\nOutputs are saved in " + self.file_name[1][0] + ".processed_files/mapping directory\n"
            "log file name is " + self.file_name[0][0] + ".mapping.log"
        )
        
    def remove_unwanted_reads(self):
        
        self.text_module.clear_info_to_display()
        
        name_processing_check = self.name_proccessing()
        if name_processing_check == False:
            return 1
        
        # error processing
        if (len(self.file_name) > 1):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if not((self.file_extension[0]) == "sam"):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
        
        test = []
        dir = 0
        for i in range(len(self.file_paths)):
            test.append(self.file_paths[i].split("/"))
            if (test[i][len(test[i])-2] == "mapping") and (test[i][len(test[i])-3] == (self.file_name[0][0] + ".processed_files")):
                del test[i][len(test[i])-1]
                test[i][len(test[i])-1] = 'mapping/'
                test[i] = "/".join(test[i])
            else: 
                dir += 1
        if dir != 0:
            print("dir != 0")
            self.file_directory = self.directory_processing(self.file_directory)
            outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
            (dcommand_a,dircheck_a) = self.directory_making(outdir)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1
            outdir_map = outdir + "mapping/"
            (dcommand_b,dircheck_b) = self.directory_making(outdir_map)
            if dcommand_b != None:
                if dircheck_b != "ok":
                    return 1
        else:
            outdir_map = self.directory_processing(test)
        
        out_map = outdir_map + self.file_name[0][0] + ".sam"
          
        # Command processing
        command = (
            "awk " + "\'$3!=\"chrM\" && $3!=\"chrEBV\"\'" + self.space +
            out_map + self.space + "| samtools view -S -b -f 0x2 -q 10 -" + self.space +
            "| samtools sort - -o" + self.space + outdir_map + self.file_name[0][0] + ".pe.q10.sort.bam"  
        )
        
        # samtools & bowtie2 return result as stderr
        rcommand = self.run_command(command)
        stderrfile = open(outdir_map+self.file_name[0][0]+".remove_unwanted_reads.log","w+")
        stderrfile.write(rcommand)
        stderrfile.close()
            
        self.text_module.update_info_to_display(
            "Executed command are "+ command + "\nRemoving unwanted reads are done\nOutputs are saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n"
            "log file name is " + self.file_name[0][0] + ".remove_unwanted_reads.log"
        )
        
    def convert_sam_to_bam(self):
        
        self.text_module.clear_info_to_display()
        
        name_processing_check = self.name_proccessing()
        if name_processing_check == False:
            return 1
        
        # error processing
        if (len(self.file_name) > 1):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if not((self.file_extension[0]) == "sam"):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
        
        test = []
        dir = 0
        for i in range(len(self.file_paths)):
            test.append(self.file_paths[i].split("/"))
            if (test[i][len(test[i])-2] == "mapping") and (test[i][len(test[i])-3] == (self.file_name[0][0] + ".processed_files")):
                del test[i][len(test[i])-1]
                test[i][len(test[i])-1] = 'mapping/'
                test[i] = "/".join(test[i])
            else:
                dir += 1
        if dir != 0:
            self.file_directory = self.directory_processing(self.file_directory)
            outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
            (dcommand_a,dircheck_a) = self.directory_making(outdir)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1
            outdir_map = outdir + "mapping/"
            (dcommand_b,dircheck_b) = self.directory_making(outdir_map)
            if dcommand_b != None:
                if dircheck_b != "ok":
                    return 1
        else:
            outdir_map = self.directory_processing(test)
        
        out_map = outdir_map + self.file_name[0][0] + ".sam"
          
        # Command processing
        command = (
            "samtools view -Sb " + out_map + self.space +
            "> "+ outdir_map + self.file_name[0][0] + ".bam" 
        )
        
        rcommand = self.run_command(command)
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            stderrfile = open(outdir_map+"Error_message.txt","w+")
            stderrfile.write(rcommand)
            stderrfile.close()
            self.text_module.update_info_to_display("Error message are saved in "+outdir_map+"Error_message.txt")
            self.init()
            return 1
        
        self.text_module.update_info_to_display(
            "Executed command are "+ command + "\nConverting were done!\nOutputs are saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n"
        )
        
    def remove_pcr_duplicates(self):
        self.text_module.clear_info_to_display()
        
        name_processing_check = self.name_proccessing()
        if name_processing_check == False:
            return 1
        
        # error processing
        if (len(self.file_name) > 1):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if not((self.file_extension[0]) == "bam"):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
        
        test = []
        test2 = []
        dir = 0
        for i in range(len(self.file_paths)):
            test.append(self.file_paths[i].split("/"))
            test2.append(self.file_paths[i].split("/"))
            if (test[i][len(test[i])-2] == "mapping") and (test[i][len(test[i])-3] == (self.file_name[0][0] + ".processed_files")):
                del test[i][len(test[i])-1]
                del test2[i][len(test2[i])-1]
                test[i][len(test[i])-1] = 'mapping/'
                test2[i][len(test2[i])-1] = 'QC/'
                test[i] = "/".join(test[i])
                test2[i] = "/".join(test2[i])
            else:
                dir += 1
        if dir != 0:
            self.file_directory = self.directory_processing(self.file_directory)
            outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
            (dcommand_a,dircheck_a) = self.directory_making(outdir)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1
            outdir_map = outdir + "mapping/"
            (dcommand_b,dircheck_b) = self.directory_making(outdir_map)
            if dcommand_b != None:
                if dircheck_b != "ok":
                    return 1
            outdir_qc = outdir + "QC/"
            (dcommand_c,dircheck_c) = self.directory_making(outdir_qc)
            if dcommand_c != None:
                if dircheck_c != "ok":
                    return 1
        else:
            outdir_map = self.directory_processing(test)
            outdir_qc = self.directory_processing(test2)
            (dcommand_a,dircheck_a) = self.directory_making(outdir_map)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1
            (dcommand_b,dircheck_b) = self.directory_making(outdir_qc)
            if dcommand_b != None:
                if dircheck_b != "ok":
                    return 1
          
        # Overwrite checking
        out_rmdup = outdir_map + self.file_name[0][0] + ".pe.q10.sort.rmdup.bam"
        ov_out_rmdup = self.overwrite_warn(out_rmdup)
        if ov_out_rmdup == False:
            self.init()
            return 1
          
        # Making duplicates
        command = (
            "java -Xmx4G -jar /seq/picard-tools-1.79/MarkDuplicates.jar" + self.space + 
            "INPUT=" + self.file_paths[0] + self.space +
            "OUTPUT=" + out_rmdup + self.space +
            "METRICS_FILE=" + outdir_qc + self.file_name[0][0] + ".Picard_Metrics_unfiltered_bam.txt" + self.space +
            "VALIDATION_STRINGENCY=LENIENT" + self.space + "ASSUME_SORTED=true" + self.space +
            "REMOVE_DUPLICATES=true" + self.space + 
            "1> " + outdir_qc + self.file_name[0][0] + ".Picard.log" + self.space +
            "2> " + outdir_qc + self.file_name[0][0] + ".Picard.err"
        )
        
        rcommand = self.run_command(command)
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.init()
            return 1
        
        self.text_module.update_info_to_display(
            "Executed command are "+ command +"Marking duplicates is done\nOutputs are saved in " + self.file_name[0][0] + ".processed_files/remove_pcr_duplicates directory\n" +
            "and" + self.file_name[0][0] + ".processed_files/QC directory\n"
        )
        
        command = ("samtools index " + out_rmdup)
        rcommand = self.run_command(command)
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.init()
            self.text_module.update_info_to_display("Error occured during indexing")
            return 1
        command = ("samtools idxstats " + out_rmdup + self.space + ">" + outdir_qc + self.file_name[0][0] + ".samtools.idxstats.txt")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.init()
            self.text_module.update_info_to_display("Error occured during making idxstats.txt")
            return 1
        command = ("samtools flagstat " + out_rmdup + self.space + ">" + outdir_qc + self.file_name[0][0] + ".samtools.flagstat.txt")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.init()
            self.text_module.update_info_to_display("Error occured during making flagstat.txt")
            return 1
        self.text_module.update_info_to_display("Indexing is done\nOutput files are saved in " + 
                                                outdir_qc + "samtools.idxstats.txt and samtools.flagstat.txt\n")
        
    def convert_to_bedgraph_and_bigwig(self):
        self.text_module.clear_info_to_display()
        self.name_proccessing()
        
        # error processing
        if (len(self.file_name) > 1):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if not((self.file_extension[0]) == "bam"):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
        
        test = []
        dir = 0
        for i in range(len(self.file_paths)):
            test.append(self.file_paths[i].split("/"))
            if (test[i][len(test[i])-2] == "mapping") and (test[i][len(test[i])-3] == (self.file_name[0][0] + ".processed_files")):
                del test[i][len(test[i])-1]
                test[i][len(test[i])-1] = 'mapping/'
                test[i] = "/".join(test[i])
            else:
                dir += 1
        if dir != 0:
            self.file_directory = self.directory_processing(self.file_directory)
            outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
            (dcommand_a,dircheck_a) = self.directory_making(outdir)
            if dcommand_a != None:
                if dircheck_a != "ok":
                    return 1
            outdir_map = outdir + "mapping/"
            (dcommand_b,dircheck_b) = self.directory_making(outdir_map)
            if dcommand_b != None:
                if dircheck_b != "ok":
                    return 1
        else:
            outdir_map = self.directory_processing(test)
            
        out_univ = outdir_map + self.file_name[0][0] + ".pe.q10.sort.rmdup."
    
        # Bam to Bed
        command = ("/seq/ATAC-seq/Code/bam2bed_shift.pl " + out_univ + "bam")
        rcommand = self.run_command(command)
        self.text_module.update_info_to_display("Bam to bed is done\nOutput file is saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n")
        # Bed to bedGraph
        command = ("genomeCoverageBed -bg -split -i " + out_univ + "bed" + self.space + "-g /seq/ATAC-seq/Data/hg38.chrom.sizes" + self.space + 
                   ">" + outdir_map + self.file_name[0][0] + ".bedGraph")
        rcommand = self.run_command(command)
        self.text_module.update_info_to_display("Bed to bedGraph is done\nOutput file is saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n")
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.text_module.update_info_to_display("Error occured during bed to bedGraph")
            self.text_module.update_info_to_display(rcommand)
            self.init()
            return 1
        # Normalizing bedGraph
        command = ("perl /seq/ATAC-seq/Code/norm_bedGraph.pl "+ outdir_map + self.file_name[0][0] + ".bedGraph" + self.space + 
                   outdir_map + self.file_name[0][0] + ".norm1.bedGraph >" + outdir_map + self.file_name[0][0] + ".norm.bedGraph.log")
        rcommand = self.run_command(command)
        self.text_module.update_info_to_display("Normalizing Bedgraph is done\nOutput file is saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n")
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.text_module.update_info_to_display("Error occured during normalizing bedGraph")
            self.init()
            return 1
        # Sorting bedGraph
        command = ("LC_COLLATE=C sort -k1,1 -k2,2n " + outdir_map + self.name[0][0] + ".norm1.bedGraph >" + outdir_map + self.file_name[0][0] + ".norm.bedGraph")
        rcommand = self.run_command(command)
        self.text_module.update_info_to_display("Sorting Bedgraph is done\nOutput file is saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n")
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.text_module.update_info_to_display("Error occured during sorting bedGraph")
            self.init()
            return 1
        # BedGraph to BigWig
        command = (
            "bedGraphToBigWig " + outdir_map + self.file_name[0][0] + ".norm.bedGraph" + self.space + 
            "/seq/ATAC-seq/Code/hg38.chrom.sizes" + self.space +
            outdir_map + self.file_name[0][0] + ".norm.bw"
        )
        rcommand = self.run_command(command)
        self.text_module.update_info_to_display("bedGraph to bigwig is done\nOutput file is saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n")
        if rcommand != None:
            self.text_module.update_info_to_display("Error occured, executed command is below\n" + command)
            self.text_module.update_info_to_display("Error occured during bedGraph to BigWig")
            self.init()
            return 1
        
        self.text_module.update_info_to_display(
            "Converting is done\nOutputs are saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n"
            "log file name is " + outdir_map + self.file_name[0][0] + ".norm.bedGraph.log"
        )
        
        path_bQC = 0
        try:
            sp.run(['ls',outdir_map + self.file_name[0][0] + ".bam"],check=True,stdout=sp.PIPE,stderr=sp.PIPE)
        except sp.CalledProcessError:
            self.popup_window.popup_input("File cannot find","File " + outdir_map + self.file_name[0][0] + ".bam" + " cannot find\n"
                                          "If you want to count of total reads before QC filter, enter file path\n" +
                                          "If not, enter 1")
            path_bQC = self.popup_window.user_input
                        
        treadaQC = ("bedtools bemtobed -i " + outdir_map + self.file_name[0][0] + ".pe.q10.sort.rmdup.bam" + self.space + "| wc -l")
        freads = ("wc -l " + outdir_map + self.file_name[0][0] + ".pe.q10.sort.rmdup.bam")
        
        rtreadaQC = sp.run(treadaQC,shell=True,capture_output=True,text=True)
        rfreads = sp.run(freads,shell=True,capture_output=True,text=True)
        self.text_module.update_info_to_display(
            "final mapped reads: " + rfreads.stdout + "\n" +
            "count of total reads after QC filter: " + rtreadaQC.stdout + "\n")
        if path_bQC != 1:
            if path_bQC == 0:
                treadbQC = ("bedtools bemtobed -i " + outdir_map + self.file_name[0][0] + ".bam" + self.space + "| wc -l")
            else:
                treadbQC = path_bQC
            rtreadbQC = sp.run(treadbQC,shell=True,capture_output=True,text=True)
            self.text_module.update_info_to_display("count of total reads before QC filter: " + rtreadbQC.stdout + "\n")

class CRISPResso(OperationMenu):
    def __init__(self, parent,text_module, popup_window, file_paths, outdir_path):
        super().inherited(parent, text_module, popup_window, file_paths, outdir_path)
        self.add_command(label="CRISPResso", command=self.crispresso)
        self.add_command(label="CRISPRessoBatch", command=self.crispresso_batch)
        self.add_command(label="CRISPRessoPooled", command=self.crispresso_pooled)
        self.add_separator()
        self.add_command(label="CRISPRessoHELP", command=self.crispresso_help)
        self.docker1 = 'docker run -v '
        self.docker2 = ':/DATA -w /DATA -i pinellolab/crispresso2 '

    def command_processor(self,command):
        modified_command = command.replace(' ', '_')
        modified_command = "--" + modified_command
        return modified_command

    def option_processor(self,title,detail,option_list):
        self.popup_window.popup_checkbox(title,detail,option_list)
        
        selected_option = []
        selected_option = self.popup_window.selected_values
        
        if selected_option == []:
            self.popup_window.popup_input("No option is selected","No option is selected\nIf you want to operate without additional options, enter 1\nIf not, enter")
            selected_option = self.popup_window.user_input
            if selected_option == "1":
                selected_option = []
                return (selected_option)
            else:
                self.text_module.update_info_to_display("No option is selected\n")
                self.option_processor(title,detail,option_list)
        
        else:
            for j in range(len(selected_option)):
                selected_option[j][0] = self.command_processor(selected_option[j][0])
            return (selected_option)

    def crispresso(self):
        self.text_module.clear_info_to_display()
        
        name_processing_check = self.name_proccessing()
        if name_processing_check == False:
            return 1
        
        self.file_directory = self.directory_processing(self.file_directory)
        
        #Error processing
        if (len(self.file_name) > 2):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Too many files selected")
            return 1
        if (self.file_name[0][0] != self.file_name[0][0]):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Files are not paired")
            return 1
        if not(((self.file_extension[0] and self.file_extension[1]) == "fastq") or ((self.file_extension[0] and self.file_extension[1]) == "fastq.gz")):
            self.init()
            self.text_module.clear_info_to_display()
            self.text_module.update_info_to_display("Selected files are wrong format")
            return 1
        
        #directory processing    
        outdir = self.file_directory + "/" + self.file_name[0][0] + ".processed_files/"
        (dcommand_a,dircheck_a) = self.directory_making(outdir)
        if dcommand_a != None:
            if dircheck_a != "ok":
                return 1
        
        for i in range(len(self.file_name)):
            sp.run("mv " + self.file_paths[i] + self.space + outdir, shell = True)
        
        command_F = self.docker1 + outdir + self.docker2 + "CRISPResso "
            
        command_F += "--fastq_r1 " + self.file_full_name[0] + self.space
        
        if len(self.file_full_name) == 2:
            command_F += "--fastq_r2 " + self.file_full_name[1] + self.space
        
        self.popup_window.popup_input("Enter amplicon sequence","Enter amplicon sequence")
        ampliseq = self.popup_window.user_input
        command_F += "--amplicon_seq " + ampliseq + self.space
        
        # name
        self.popup_window.popup_input("Enter name","Enter output name of the report")
        input_name = self.popup_window.user_input
        while True:
            if input_name == "":
                self.popup_window.popup_input("Enter name","Enter output name of the report")
                input_name = self.popup_window.user_input
            else:
                break
            
        command_F += '--name ' + input_name + self.space
        
        command_F += "--output_folder /DATA" + self.space
    
    
        basic_options = [["amplicon name","A name for the reference amplicon can be given. If multiple amplicons are given, multiple names can be specified here.\namplicon names are truncated to 21bp unless the parameter --suppress_amplicon_name_truncation is set.\nDefault : Reference"],
                    #sgRNA options
                    ["guide seq","sgRNA sequence, if more than one, please separate by commas.\nsgRNA needs to be input as the guide RNA sequence immediately adjacent to but not including the PAM sequence (5' of NGG for SpCas9)."],
                    ["guide name","sgRNA names, if more than one, please separate by commas\ndefalut: sgRNA"],
                    ["discard guide positions overhanging amplicon edge","If set, for guides that align to multiple positions, guide positions will be discarded if plotting around those regions would included bp that extend beyond the end of the amplicon.\ndefault: False"],
                    ["expected hdr amplicon seq","Amplicon sequence expected after HDR.\nNote that the entire amplicon sequence must be provided, not just the donor template."],
                    ["coding seq","Subsequence/s of the amplicon sequence covering one or more coding sequences for frameshift analysis.\nIf more than one (for example, split by intron/s), please separate by commas.\nUsers should provide the subsequences of the reference amplicon sequence that correspond to coding sequences (not the whole exon sequence(s)!)."],
                    ["minimum average read quality","Minimum average quality score (phred33) to keep a read\ndefault: 0"],
                    ["minimum single bp quality","Minimum single bp score (phred33) to keep a read\ndefault: 0"],
                    ["plot histogram outliers","If set, all values will be shown on histograms. By default (if unset), histogram ranges are limited to plotting data within the 99 percentile.\ndefault: False"],
                    #quantification options
                    ["quantification window size","This option also called \'window_around_sgRNA\'\nDefines the size (in bp) of the quantification window extending from the position \nspecified by the \"--quantification_window_center\" parameter in relation to the provided guide RNA sequence(s)\ndefault: 1"],
                    ["quantification window center","This option also called \'cleavage_offset\'\nCenter of quantification window to use within respect to the 3' end of the provided sgRNA sequence.\nRemember that the sgRNA sequence must be entered without the PAM.If using the Cpf1 system, enter the sequence immediately 3' of the PAM sequence and explicitly set the '--cleavage_offset' parameter to 1\ndefault: -3"],
                    # output options
                    ["file prefix","File prefix for output plots and tables"],
                    ["fastq output","If set, a fastq file with annotations for each read will be produced\ndefault: False"],
                    ["keep intermediate","Keep all the intermediate files\ndefault: False"],
                    ["zip output","If true, the output folder will be zipped upon completion.\ndefault: False"],
                    ["suppress amplicon name truncation","If set, amplicon names will not be truncated when creating output filename prefixes. If not set, amplicon names longer than 21 characters will be truncated when creating filename prefixes.\ndefault: False"],
                    ["ETC","Use if you want to set options that is not listed\nIf you select this option, you will enter the option yourself. There is no additional validation in the program for the option entered."]]
        
        basic_options = self.option_processor("CRISPResso options","Which of the optional options would you like to use",basic_options)
        
        if basic_options != []:
            for i in range(len(basic_options)):
                command_F += basic_options[i][0] + self.space + basic_options[i][1] + self.space

        rcommand = self.run_command(command_F)
        # print(command_F)
        print(rcommand)


        for i in range(len(self.file_name)):
            sp.run("mv " + outdir + self.file_full_name[i] + self.space + self.file_paths[i], shell = True)
        
        
        
    def crispresso_batch(self):
        print("CRISPRessoBatch")
    
    def crispresso_pooled(self):
        print("CRISPRessoPooled")
    
    def crispresso_help(self):
        self.text_module.clear_info_to_display()
        self.text_module.update_info_to_display("CRISPRessoHELP")
        self.text_module.update_info_to_display("CRISPResso is a software pipeline for the analysis of CRISPR-Cas9 genome editing outcomes from deep sequencing data.\n"
                                                "It is designed to enable rapid and intuitive interpretation of results produced by amplicon sequencing.\n"
                                                "They will do the following\n"
                                                "aligns sequencing reads to a reference sequence\n"
                                                "quantifies insertions, mutations and deletions to determine whether a read is modified or unmodified by genome editing\n"
                                                "summarizes editing results in intuitive plots and datasets\n"
                                                "If you want to trim adapter, you have to use \'trimming\' function in \'Operation\' menu.\n"
)
   
class MainMenu:
    def __init__(self, parent):
        
        parent.title("Sequencing preprocesser")
        parent.geometry("1200x700")
        parent.resizable(True, True)
        
        self.text_module = TextModule(parent)
        self.text_module.set_font("Helvetica",12)
        self.popup_window = PopupWindow(parent)
        
        
        self.menu_bar = tk.Menu(parent)
        self.file_menu = FileMenu(self.menu_bar, self.text_module,self.popup_window)
        self.operation_menu = OperationMenu(self.menu_bar,self.text_module,self.popup_window,[],"")
        self.crispresso_menu = CRISPResso(self.menu_bar,self.text_module,self.popup_window,[],"")

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Operation", menu=self.operation_menu)
        self.menu_bar.add_cascade(label="CRISPResso", menu=self.crispresso_menu)
        
        # Comments for users
        self.text_module.update_info_to_display(
            "This processer is based on tkinter, python\n"
            "Before using, please read \"README.md\"\n"
            "This processer uses cutadapt, bowtie2, samtools\n"
            "If you doesn't setting output_directory, output files are saved in the same directory as the input file.\n"
            "If you have any errors, inquiries, or improvements, Please contact me at the following information.\n"
            "ansh1226@unist.ac.kr\n"
            "https://github.com/Operon1226/GUI_sequencing_preprocessor"
        )
        
        parent.config(menu=self.menu_bar)

def main():
    mainframe = tk.Tk()
    main_menu = MainMenu(mainframe)
    main_menu.file_menu.operation_menu = main_menu.operation_menu
    main_menu.file_menu.crispresso_menu = main_menu.crispresso_menu
    main_menu.operation_menu.file_menu = main_menu.file_menu
    main_menu.crispresso_menu.file_menu = main_menu.file_menu
    mainframe.mainloop()

if __name__ == '__main__':
    main()
    
