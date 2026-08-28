# Multiview-Split
## What is it?
This tool generates batches of videos from multiple long videos at marker defined intervals and generates per-view trials at each point of interest.
It uses shotcut to define the multi-view timeline, and the markers included to define the points of interest.
## Prerequisites
[Python](https://www.python.org/) (add to path during installation)

[Shotcut](https://www.shotcut.org/download/)
## Setup - Windows
The tool uses `melt.exe` (packaged within shotcut) and a shotcut project file `.mlt`.
Firstly add shotcut's directory to path:

1.) win+R and search `SystemPropertiesAdvanced.exe`

2.) Select Environment Variables...

3.) Under "user variables for USER", select path and edit

4.) Select new and paste the folder location of Shotcut (default is `C:\Program Files\Shotcut`)
<img width="519" height="490" alt="image" src="https://github.com/user-attachments/assets/95bbf99d-5135-430e-bb53-517faa3b21c9" />

5.) Clone this repo and add to path (using instructions above) or use as is!
### Setup - Linux
1.) Install Shotcut using your desired method

2.) Clone this repo and add to path (using instructions above) or use as is!




## Usage
### Preparation
To begin splitting videos you need to generate a `.mlt` file, which will contain the target video clips that will get split.
Once you've added videos, you can add markers and select the start, end and name that you would like for the trial within the marker.
Once you've placed all of the markers you'd like to extract as trials, save the project file.
<img width="1913" height="558" alt="image" src="https://github.com/user-attachments/assets/e0da3450-c33b-48fd-85bf-8fc8741ffc6a" />
### Using Multiview-split
Open up a terminal and run the command
```cmd
multiviewsplit --mlt_path "PATH/TO/YOUR/SHOTCUT/MLT/FILE"
```
When processing, you will be asked to specify the video clip name, where you set the videos desired name.
After running it will begin generating divided up clips into a file called `output`, within will be the folders of each marker with each clip from the respective video
<img width="705" height="448" alt="image" src="https://github.com/user-attachments/assets/9104f2c3-056b-4bfd-b175-77bcf26b0fec" />
