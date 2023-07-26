import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess as sp
import math

class PopupWindow:
    def __init__(self, mainframe):
        self.mainframe = mainframe
        self.popup = None
        self.user_input = ""
    
    def popup_input(self,title,detail):
        self.popup = tk.Toplevel(self.mainframe)
        self.popup.geometry("800x100")
        self.popup.title(title)
        self.popup.resizable(True,True)
        self.user_input = ""
        label = tk.Label(self.popup,text=detail)
        label.pack()
        
        entry = tk.Entry(self.popup)
        entry.pack()
        
        def get_input():
            self.user_input = entry.get()
            self.popup_destroy()
        
        button = tk.Button(self.popup,text="OK",command=get_input)
        button.pack()
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
        self.text = tk.Text(mainframe)
        self.text.pack()
    
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
        
class OperationMenu(tk.Menu):
    def __init__(self, parent,text_module,popup_window,file_paths,outdir_path):
        super().__init__(parent,tearoff=False)
        self.text_module = text_module
        self.popup_window = popup_window
        self.file_paths = file_paths
        self.outdir_path = outdir_path
        self.add_command(label = "Adapter trimming", command = self.adapter_trimming)
        self.add_command(label = "Mapping", command = self.mapping)
        self.add_command(label = "Remove unwanted reads", command = self.remove_unwanted_reads)
        self.add_command(label = "Convert sam to bam", command = self.convert_sam_to_bam)
        self.add_command(label = "Remove PCR duplicates", command = self.remove_pcr_duplicates)
        self.add_command(label = "Convert to bedgraph and bigwig", command = self.convert_to_bedgraph_and_bigwig)
        
        self.processes = []
        
        self.space = " "
        self.file_name = []
        self.file_extension = []
        self.file_directory = []

    def directory_making(self,name):
        try:
            command = 'mkdir ' + name
            output = sp.Popen(command,shell=True,universal_newlines=True,stdout=sp.PIPE, stderr=sp.PIPE)
            (stdout,stderr) = output.communicate()
            
            if stderr != "":
                self.popup_window.popup_input("Directory checking",name+" already exists. If you want to save results in that directory, input ok")
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
            self.popup_window.popup_input("Overwrite warning",f"{files_paths} already exists. If you want to overwrite, input ok")
            self.text_module.update_info_to_display("command terminated")
            overwrite_check = self.popup_window.user_input
            if overwrite_check != "ok":
                self.init()
                return False
        else:
            return True
        
    def name_proccessing(self):
        self.init()
        for i in range(len(self.file_paths)):
            self.file_name.append(self.file_paths[i].split("/"))
            self.file_name[i] = self.file_name[i][len(self.file_name[i])-1]
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

    def adapter_trimming(self): 
        
        self.text_module.clear_info_to_display()
        self.name_proccessing()
        self.file_directory = self.directory_processing(self.file_directory)
        print(self.file_directory)
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
          
        
        
        #command processing
        command = (
            "cutadapt " + "-a " + adapter1 +  self.space +  "-A " + adapter2 + self.space + 
            "-m 5" + self.space + "--nextseq-trim=20" + self.space + 
            "-o " + out_f1 + self.space + "-p " + out_f2 + self.space + 
            self.file_paths[0] + self.space + self.file_paths[1] + self.space +
            "> "+ outdir_adp + self.file_name[1][0] + ".trim.log"
        )
        
        rcommand = self.run_command(command)
        if rcommand != None:
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
        self.name_proccessing()
        
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
        
        mthreads = sp.run("nproc",shell=True,capture_output=True,text=True)
        rthreads = sp.run("top -bn1 | awk \'NR>7 { sum += $9 } END { print sum }\'",shell=True,capture_output=True,text=True)
        mthreads = float(mthreads.stdout)
        rthreads = float(rthreads.stdout)
        rthreads = math.ceil(rthreads / 100)
        athreads = mthreads - rthreads
        
        comment = "Input threads for running this task\nAvailable threads are %f\nUsing a lot of threads doesn't always speed up." % athreads
        
        # Threads
        while True:
            self.popup_window.popup_input("Threads for this task",comment)
            threads = self.popup_window.user_input
            a = int(threads)
            
            if a <= athreads:
                break
            
            else:
                self.text_module.update_info_to_display("The input value is more than the available number. Please enter it again")

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
        self.name_proccessing()
        
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
        self.name_proccessing()
        
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
            stderrfile = open(outdir_map+"Error_message.txt","w+")
            stderrfile.write(rcommand)
            stderrfile.close()
            self.text_module.update_info_to_display("Error message are saved in "+outdir_map+"Error_message.txt")
            self.init()
            return 1
        
        self.text_module.update_info_to_display(
            "Executed command are "+ command + "\nRemoving unwanted reads are done\nOutputs are saved in " + self.file_name[0][0] + ".processed_files/mapping directory\n"
        )
        
    def remove_pcr_duplicates(self):
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
        test2 = []
        dir = 0
        for i in range(len(self.file_paths)):
            test.append(self.file_paths[i].split("/"))
            test2.append(self.file_paths[i].split("/"))
            if (test[i][len(test[i])-2] == "mapping") and (test[i][len(test[i])-3] == (self.file_name[0][0] + ".processed_files")):
                del test[i][len(test[i])-1]
                del test2[i][len(test2[i])-1]
                test[i][len(test[i])-1] = 'map/'
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
            outdir_map = outdir + "map/"
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
            "INPUT=" + self.filepaths[0] + self.space +
            "OUTPUT=" + out_rmdup + self.space +
            "METRICS_FILE=" + outdir_qc + self.file_name[0][0] + ".Picard_Metrics_unfiltered_bam.txt" + self.space +
            "VALIDATION_STRINGENCY=LENIENT" + self.space + "ASSUME_SORTED=true" + self.space +
            "REMOVE_DUPLICATES=true" + self.space + 
            "1> " + outdir_qc + self.file_name[0][0] + ".Picard.log" + self.space +
            "2> " + outdir_qc + self.file_name[0][0] + ".Picard.err"
        )
        
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            return 1
        
        self.text_module.update_info_to_display(
            "Marking duplicates is done\nOutputs are saved in " + self.file_name[0][0] + ".processed_files/remove_pcr_duplicates directory\n" +
            "and" + self.file_name[0][0] + ".processed_files/QC directory\n"
        )
        
        command = ("samtools index " + out_rmdup)
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            self.text_module.update_info_to_display("Error occured during indexing")
            return 1
        command = ("samtools idxstats " + out_rmdup + self.space + ">" + outdir_qc + self.file_name[0][0] + "samtools.idxstats.txt")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            self.text_module.update_info_to_display("Error occured during making idxstats.txt")
            return 1
        command = ("samtools flagstat " + out_rmdup + self.space + ">" + outdir_qc + self.file_name[0][0] + "samtools.flagstat.txt")
        rcommand = self.run_command(command)
        if rcommand != None:
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
                continue
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
            outdir_map = self.directory_processing(self.file_directory)
            
        out_univ = outdir_map + self.file_name[0][0] + ".pe.q10.sort.rmdup."
    
        # Bam to Bed
        command = ("/seq/ATAC-seq/Code/bam2bed_shift.pl " + out_univ + "bam")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            return 1
        # Bed to bedGraph
        command = ("genomeCoverageBed -bg -split -i " + out_univ + "bed" + self.space + "-g /seq/ATAC-seq/Code/hg38.chrom.sizes" + self.space + 
                   ">" + outdir_map + self.file_name[0][0] + ".bedGraph")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            return 1
        # Normalizing bedGraph
        command = ("perl /seq/ATAC-seq/Code/norm_bedGraph.pl "+ outdir_map + self.file_name[0][0] + ".bedGraph" + self.space + 
                   outdir_map + self.file_name[0][0] + ".norm1.bedGraph >" + outdir_map + self.file_name[0][0] + ".norm.bedGraph.log")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            return 1
        # Sorting bedGraph
        command = ("LC_COLLATE=C sort -k1,1 -k2,2n " + outdir_map + self.name[0][0] + ".norm1.bedGraph >" + outdir_map + self.name[0][0] + ".norm.bedGraph")
        rcommand = self.run_command(command)
        if rcommand != None:
            self.init()
            return 1
        # BedGraph to BigWig
        command = (
            "bedGraphToBigWig " + outdir_map + self.file_name[0][0] + ".norm.bedGraph" + self.space + 
            "/seq/ATAC-seq/Code/hg38.chrom.sizes" + self.space +
            outdir_map + self.file_name[0][0] + ".norm.bw"
        )
        rcommand = self.run_command(command)
        if rcommand != None:
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
    
class MainMenu:
    def __init__(self, parent):
        
        parent.title("Sequencing preprocesser")
        parent.geometry("700x400")
        parent.resizable(True, True)
        
        self.text_module = TextModule(parent)
        self.popup_window = PopupWindow(parent)
        
        
        self.menu_bar = tk.Menu(parent)
        self.file_menu = FileMenu(self.menu_bar, self.text_module,self.popup_window)
        self.operation_menu = OperationMenu(self.menu_bar,self.text_module,self.popup_window,[],"")

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Operation", menu=self.operation_menu)
        
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
    mainframe.mainloop()

if __name__ == '__main__':
    main()
    
