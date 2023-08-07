# Sequencing Preprocessor GUI

This GUI tool is designed to facilitate the preprocessing of sequencing data. It provides a user-friendly interface to perform various operations on sequencing files, such as adapter trimming, mapping, removing unwanted reads, converting SAM to BAM, removing PCR duplicates, and converting to bedGraph and bigWig formats.

## Naming rules
This program has a standard naming rule.
Cell line name-number_Read number.format or other informations

Ex) HCT116-1_R1.fastq.gz, HEK293T-1_R2.fastq.gz, HCT116-1.sam.

If the Cell line name contains '-', '_', '.', an error may occur, so pre-processing is required.

## Getting Started

### Prerequisites

Make sure you have the following software installed on your system:

- Python (>= 3.7)
- Tkinter (included with Python)
- Cutadapt
- Bowtie2
- Samtools 
- picard-tools;MarkDuplicates.jar (optional, for remove PCR duplicates)
- bam2bed_shift.pl (optional)
- norm_bedGraph.pl (optional)
- genomeCoverageBed (optional)
- GenomeCoverageBed (optional)
- CRISPResso2 (optional, for CRISPResso)

### Installation

1. Clone the repository from GitHub:
`git clone https://github.com/Operon1226/GUI_sequencing_preprocessor.git`
2. Navigate to the cloned directory:
`cd GUI_sequencing_preprocessor`
3. Run the GUI:
`python3 gui.py`

### Setting shebang

Please set the location of Python to use when you run this program in shebang.
Default is '#!/usr/bin/env python3'

## Troubleshooting & Errors

### The letters look broken or too small.

In Python, installed as Anaconda, we found that changing the font or size of the letters did not apply well.
Please set original interpreters; ex) #!/usr/bin/env python3 or #!/usr/bin/python3

### Error: "no display name and no $DISPLAY environment variable"

#### Detailed error messages
```Shell
Traceback (most recent call last):
  File "gui.py", line 108, in <module>
    main()
  File "gui.py", line 102, in main
    mainframe = tk.Tk()
  File "/home/intern/anaconda3/lib/python3.7/tkinter/__init__.py", line 2023, in __init__
    self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
_tkinter.TclError: no display name and no $DISPLAY environment variable
```

This error may occur if X11 forwarding is disabled during the SSH process. To resolve it:

#### If you are using MobaXterm

1. Right-click on the server icon.
2. Click "Edit Session."
3. Click "Advanced SSH settings."
4. Check "X11-forwarding."
5. Reconnect to the server.

#### If you are using shell

Add the '-X' option when connecting to the server using SSH:
`ssh -X -p port ID@IP``

### Error: "couldn't connect to display"

#### Detailed error messages
```Shell
connect /tmp/.X11-unix/X0: No such file or directory
connect /tmp/.X11-unix/X0: No such file or directory
Traceback (most recent call last):
  File "gui.py", line 782, in <module>
    main()
  File "gui.py", line 776, in main
    mainframe = tk.Tk()
  File "/home/intern/anaconda3/lib/python3.7/tkinter/__init__.py", line 2023, in __init__
    self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
_tkinter.TclError: couldn't connect to display "localhost:12.0"
```
If you run a program using a different tkinter on the same account, you may have problems.

## Usage

1. Open the GUI application.
2. Use the 'File' menu to import your sequencing files.
3. Select the preprocessing operation you want to perform from the 'Operation' menu.
4. Follow the prompts and provide any required input.
5. Click on the operation to execute it, and view the progress and results in the display.

## Functions

### adapter_trimming

This function uses the 'cutadapt' command for adapter trimming. The adapter sequence is set to 'CTGTCTCTTATACACATCT'.

### mapping

This function uses the 'bowtie2' command for mapping. 
mapping option is 'very sensitive'
This program also implemented to take the current CPU usage and show the number of threads available so that more than one thread can be used when mapping.

### remove unwanted reads

This function uses awk command and samtools.
Using awk, they filtered chrM and chrEBV.
And also, using samtools view, selects only reads with a mapping quality score greater than or equal to 10. output files are "name.pe.q10.sort.bam"  

### convert sam to bam 

This function uses samtools. They will convert sam files to bam files. 

### remove pcr duplicates

This function uses picard-tools;MarkDuplicates.jar, and samtools

### convert bam to bedGraph and bigwig

This function uses genomeCoverageBed, bam2bed_shift.pl, norm_bedGraph.pl, bedGraphToBigWig

### overwrite_warning

If a file already exists, there is a function to ask if you want to overwrite it.

### directory

If you already have a directory, this program has the ability to ask if you want to save outputs to that directory.
It also checks that the directory entered is valid.
And if the input files' directory is different, a warning popup will occur and they will request setting the output directory to users

### log file

When operations are executed, log files are created at same directory as output files. And if, error were occured during executing, error messages are also saved as "Error_message.txt". Since samtools and bowtie2 return values as stderr, It is not created when you run both tools.

### wrong input format warning

If input files are not proper to executing that operation, warning message will printed to GUI display.

## Classes

### PopupWindow

The 'PopupWindow' class is used to control popup windows. It has three methods:

#### `popup_input(title, detail)`

This function is designed to receive input from the user and returns the user's input. The 'title' parameter indicates the title of the popup window, and the 'detail' parameter provides a description displayed below the title.

#### `popup_wait(detail)`

This function creates a popup window with the title "Running command" to indicate that a command is executing. The 'detail' parameter works similarly to the 'popup_input' function.

#### `popup_destroy()`

This function is used to destroy popup windows.

### TextModule

The 'TextModule' class is used to control the text displayed in the GUI. It has three methods:

#### `update_file_paths_display(file_paths)`

This function is designed to indicate imported file paths on the display. It takes a list of file paths as a parameter.

#### `update_info_to_display(text)`

This function is used to print text on the display. The 'text' parameter must be a string.

#### `clear_info_to_display()`

This function is used to clear all information displayed on the GUI.

### FileMenu

The 'FileMenu' class is responsible for controlling the 'File' menu in the menubar. It has three functions:

#### `open_file_explorer()`

This function is designed to open the file explorer and save the selected file paths to another variable.

#### `exit_program()`

This function is used to exit the GUI program and terminate all subprocesses.

#### `outdir()`

This function is used to receive the output directory from the user and set it as the output directory. It also checks whether the entered directory is valid.

### OperationMenu

The 'OperationMenu' class is responsible for controlling various preprocessing operations. It includes methods for adapter trimming, mapping, removing unwanted reads, converting SAM to BAM, removing PCR duplicates, and converting to bedGraph and bigWig formats.

#### `adapter_trimming()`

This function performs adapter trimming on the imported ATAC-seq files. It uses the 'cutadapt' command with the default adapter sequence 'CTGTCTCTTATACACATCT'.

#### `mapping()`

This function maps the preprocessed reads to a reference genome using Bowtie2.

#### `remove_unwanted_reads()`

This function removes unwanted reads based on chromosome(chrM,chrEBV).
And also, using samtools view, selects only reads with a mapping quality score greater than or equal to 10.

#### `convert_to_bam()`

This function converts the mapped reads from SAM to BAM format using Samtools.

#### `remove_pcr_duplicates()`

This function removes PCR duplicates from the BAM files using picard-tools.

#### `convert_to_bedGraph_and_bigwig()`

This function converts the BAM files to bedGraph format and bigwig format.
This function converts BAM files to bed files using bam2bed_shift.pl
And using genomeCoverageBed, convert bed to bedGraph.
Using norm_bedGraph.pl, bedGraph were normalized.
Using bedGraphToBigWig, convert bedGraph to bigwig


## MainMenu

The 'MainMenu' class is the main entry point for the GUI application. It sets up the main window and composes the other classes to create the GUI elements.

## Contact

If you encounter any errors, have inquiries, or want to suggest improvements, please contact:

- Email: ansh1226@unist.ac.kr
- GitHub: [https://github.com/Operon1226/GUI_sequencing_preprocessor](https://github.com/Operon1226/GUI_sequencing_preprocessor)

Your feedback is appreciated, and it will help me enhance the tool further. Thank you for using the Sequencing Preprocessor GUI!
