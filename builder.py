from time import sleep
import datetime
import random
import time
import openpyxl
import glob
import requests
import random
import time
import shutil
import os, sys
import pickle
from os import system, name
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import PieChart, Reference, Series
from dataclasses import dataclass
from rich import print
from rich.layout import Layout
from rich import box
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.prompt import Confirm
from rich.prompt import Prompt
from rich.console import Console
from rich.align import Align

prnumber = 0
panelroom = 0
equipnumber = 0
elv = 0
el = 0
imglist = []

#lists
prlist = []
vlist = []
olist = []
prolist = []
crashsave=[]

#save last card info
sdtype=0
rlsave=0
olsave=0
elsave=0
essave=0
prsave=0
prnsave=["",""]
equipname="test"
equipnumber="000-000000"
hz=0
hz1=0

Iname1=""
Iname2=""
Iname3=""
Iname4=""
Iname5=""
Iname6=""

checkonce=True
loading = Text()
foundrecords = Text()

layout=Layout()
console = Console(height=63)

class eStops:
    def __init__(self):
        self.location = ""
    def gen_eStops(self):
        
        try:
            self.location = Prompt.ask("Location",default=str(self.location))
        except:
            return
class Rlockouts:
    def __init__(self):
        self.location = ""
    def gen_remoteLockouts(self):
        
        try:
            self.location = Prompt.ask("Location",default=str(self.location))  # Python 3
        except:
            return
class Olockouts:
    def __init__(self):
        self.Type = 0
        self.sType = 0
        self.cType = 0
        self.name = 0
        self.proced = 0
        self.sproced=0
    def gen_other(self):
        olheader=""
        loadold = Align.center(
            Text.from_markup(f"Select Other Lockout Types", justify="center"),
            vertical="middle",style="yellow"
        )
        layout["lower"].update(Panel(loadold))#Text("Would you Like to load your previous data?",style="bright_red",justify="center")))
        _ = system('cls')
        screen.update(layout)
        for oroom in olist:
            olheader+=str(olist.index(oroom)) + " : " + oroom+"\n"
        layout["lower"].update(Panel(olheader))
        _ = system('cls')
        screen.update(layout)
        Oltry = True
        while Oltry:
            try:
                self.Type = Prompt.ask("Enter 0-"+str(len(olist)-1),default=str(self.sType))
                self.sType=self.Type
                self.Type = int(self.Type)
            except:
                console.print("Use Only Numbers.", style="red",justify="center")
                continue
            if self.Type >= len(olist):
                console.print("Use Values Between 0 - "+len(olist)-1, style="red",justify="center")
                continue
            if self.Type < len(olist):
                self.Type = olist[self.Type]
                if self.Type == "Other":
                    self.Type = Prompt.ask("Enter Lockout Type",default=str(self.cType))
                    self.cType = self.Type
                Oltry = False
        self.name = Prompt.ask("\nLockout Name",default=str(self.name))
        console.print(Panel("Select Usage\n1 : 3A\n2 : 3B\n3 : 3C\n4 : 3D"))
        self.protry = True
        while self.protry:
            self.proced = Prompt.ask("Enter 1-4",default=str(self.sproced))
            self.sproced=self.proced
            self.proced=int(self.proced)
            if self.proced == 1 or self.proced == 2 or self.proced == 3 or self.proced == 4:
                if self.proced > 4:
                    continue
                if self.proced == 1:
                    self.protry = False
                    self.proced = "3A"
                if self.proced == 2:
                    self.protry = False
                    self.proced = "3B"
                if self.proced == 3:
                    self.protry = False
                    self.proced = "3C"
                if self.proced == 4:
                    self.protry = False
                    self.proced = "3D"
            else:
                console.print("Use Only Numbers 1-4.", style="red",justify="center")
                self.prrtry = True
class Elockouts:
    def __init__(self):
        self.volts = ""
        self.bucket = ""
        self.proced = 0
        #backup saves
        self.svolts=""
        self.sproced=""

    def gen_elect(self):
        loadold = Align.center(
            Text.from_markup(f"Select Lockout Voltage", justify="center"),
            vertical="middle",style="yellow"
        )
        layout["lower"].update(Panel(loadold))#Text("Would you Like to load your previous data?",style="bright_red",justify="center")))
        _ = system('cls')
        screen.update(layout)
        vheader=""
        for vroom in vlist:
            vheader+=str(vlist.index(vroom)) + " : " + vroom+"\n"
        layout["lower"].update(Panel(vheader))
        _ = system('cls')
        screen.update(layout)
        Eltry = True
        while Eltry:
            try:
                self.volts = Prompt.ask("Enter 0-"+str(len(vlist)-1),default=str(self.svolts))
                self.svolts=self.volts
                self.volts = int(self.volts)
            except:
                console.print("Use Only Numbers.", style="red",justify="center")
                self.vols=""
                continue
            if self.volts >= len(vlist):
                console.print("Use Numbers between 0 - "+str(len(vlist)-1), style="red",justify="center")
            if self.volts < len(vlist):
                    self.volts = vlist[self.volts]
                    Eltry = False
                    
                    if self.volts == "Other":
                        self.volts = Prompt.ask("Enter Lockout Type",default=str(self.volts))
        self.bucket = Prompt.ask("Bucket Number",default=str(self.bucket))
        console.print("Select Usage", style="cyan",justify="center")
        console.print(Panel("1 : 3A\n2 : 3B\n3 : 3C\n4 : 3D"))
        self.protry = True
        while self.protry:
            self.proced = Prompt.ask("Enter 1-4",default=str(self.sproced))
            self.sproced=self.proced
            self.proced=int(self.proced)
            if self.proced == 1 or self.proced == 2 or self.proced == 3 or self.proced == 4:
                if self.proced > 4:
                    continue
                if self.proced == 1:
                    self.protry = False
                    self.proced = "3A"
                if self.proced == 2:
                    self.protry = False
                    self.proced = "3B"
                if self.proced == 3:
                    self.protry = False
                    self.proced = "3C"
                if self.proced == 4:
                    self.protry = False
                    self.proced = "3D"
            else:
                console.print("Use Only Numbers 1-4.", style="red",justify="center")
                self.prrtry = True


def elecLockouts(elsave):
    eltry = True
    while eltry:
        try:
            electext = Align.center(
            Text.from_markup(f"How many Eletrical Lockouts (Enter 0-5)\n\n", justify="center"),
            vertical="middle",style="yellow"
            )
            layout["lower"].update(Panel(electext))
            _ = system('cls')
            screen.update(layout)
            el = Prompt.ask("(Enter 0-5)",default=str(elsave))
            electext = Align.center(
            Text.from_markup(f"How many Eletrical Lockouts (Enter 0-5)\n\n"+str(el), justify="center"),
            vertical="middle",style="yellow"
            )
            layout["lower"].update(Panel(electext))
            _ = system('cls')
            screen.update(layout)
            el = int(el)
        except:
            console.print("Use Only Numbers!", style="red",justify="center")
            continue
        if el > 5:
            console.print("Invalid Input Please Enter A Value 0-5", style="red",justify="center")
        if el <= 5:
            eltry = False
            return el
def otherLockouts(olsave):
    oltry = True
    while oltry:
        try:
            othertext = Align.center(
            Text.from_markup(f"How many Other Lockouts (Enter 0-5)", justify="center"),
            vertical="middle",style="yellow"
            )
            layout["lower"].update(Panel(othertext))
            _ = system('cls')
            screen.update(layout)
            ol = Prompt.ask("\nHow many Other Lockouts (Enter 0-5)",default=str(olsave))
            othertext = Align.center(
            Text.from_markup(f"How many Other Lockouts (Enter 0-5)\n\n"+str(ol), justify="center"),
            vertical="middle",style="yellow"
            )
            layout["lower"].update(Panel(othertext))
            _ = system('cls')
            screen.update(layout)
            ol = int(ol)
        except:
            console.print("Use Only Numbers! other lockouts", style="red",justify="center")
            continue
        if ol > 5:
            console.print("Invalid Input Please Enter A Value 0-5", style="red",justify="center")
        if ol < 6:
            oltry = False
            return ol
def select_PR(prnsave):
    pr = 0
    prheader= ""
    prsave=str(prnsave[1])
    prn2save=prnsave[0]
    prtext = Text(justify="left")
    prtext.append("Lockout Card Builder\n\n", style="bold cyan")
    _ = system('cls')
    screen.update(layout)
    for proom in prlist:
        prheader+=str(prlist.index(proom)) + " : " + proom+"\n"
    prtext.append(prheader)
    layout["lower"].update(Panel(prtext,title="Select Panel Rooms"))
    _ = system('cls')
    screen.update(layout)
    invalid_input = True
    while invalid_input:
        try:
            pr = Prompt.ask(" Enter 0-"+str(len(prlist)-1),default=str(prsave))
            prsave=pr
            pr = int(pr)
        except:
            console.print("Use Only Numbers.", style="red",justify="center")
            continue
        if pr >= len(prlist):
            console.print("Invalid Input Please try again.", style="red",justify="center")
        if pr < len(prlist):
            prn = " Panel Room"
            if pr == 0:
                
                panelroom = Prompt.ask("Enter Panel Room Name",default=str(prn2save))
                invalid_input = False
                return panelroom, prsave
            else:
                panelroom = prlist[pr] + prn
                invalid_input = False
                return panelroom, prsave
def eStop_count(essave):
    estry = True
    while estry:
        try:
            es = Prompt.ask("\nHow Many eStops (Enter 0-2)",default=str(essave))
            es = int(es)
            print("")
        except:
            console.print("Use Only Numbers!", style="red",justify="center")
            continue
        if es > 2:
            console.print("Invalid Input Please Enter A Value 0-2", style="red",justify="center")
        if es < 3:
            estry = False
            return es
def remoteLockouts(rlsave):
    rltry = True
    while rltry:
        try:
            rl = Prompt.ask("\nHow Many Remote Lockouts (Enter 0-7:) ",default=str(rlsave))
            rl = int(rl)
            print("")
        except:
            console.print("Use Only Numbers!", style="red",justify="center")
            continue
        if rl > 7:
            console.print("Invalid Input Please Enter A Value 0-7", style="red",justify="center")
        if rl < 8:
            return rl
def shutdownprocedure(sdtype):
    Type = 0
    spheader=""
    console.print("Select Shutdown Procedure", style="cyan",justify="center")
    for proroom in prolist:
        spheader+=str(prolist.index(proroom)) + " : " + proroom+"\n"
    console.print(Panel(spheader))
    sdtry = True
    while sdtry:
        try:
            sdtype = Prompt.ask("Enter 0-"+str(len(prolist)-1),default=str(sdtype))
            sdtype = int(Type)
        except:
            console.print("Use Only Numbers.", style="red",justify="center")
            continue
        if sdtype >= len(prolist):
            console.print("Use values between 0 - "+str(len(prolist)-1), style="red",justify="center")
        if sdtype < len(prolist):
            sdtype = prolist[Type]
            
            if sdtype == "Other":
                sdtype = Prompt.ask("Input Shutdown Procedure",str(sdtype))
            return sdtype
def hazard(hz):
    global hz1
    hz1 = Prompt.ask("\nIs there a Hazardous energy permit? yes/no",default=str(hz1))
    if hz1 == '' or not hz1[0].lower() in ['y','n']:
        print('Please answer with yes or no!') 
    if hz1[0].lower() == 'y': #Do something 
        hz = Prompt.ask("What is the SOP Number",default=(str(hz)))
        return hz
    if hz1[0].lower() == 'n': #Do something 
        hz = None
        return
def check_exists(dir):
    isdir = os.path.isdir(dir) 
    return isdir
def generate_resources():
    try:
        with open('resources.txt') as f:
            fr="Found Resources"
            return fr
    except IOError:
        resourcedefault = ['<panelrooms>','Custom','Harvest/Trolly Floor','Cut Floor','Converting','Old Rendering','New Rendering','Scald Tub','Nippon','Cellars','CO2','Flow-Thru','Jeep Shop','Plasma','Waste Water One','Waste Water Two','Waste Water Three','Waste Water Four','Powerhouse One','Powerhouse Two','MQ Chill','Telephone','TCCS','</panelrooms>','<volts>','480v','220v','110v','24v','Other','</volts>','<otherlockouts>','Hydraulic','Water','Air','Steam','Other','</otherlockouts>','<ssProcedure>','USE STOP/START SWITCH','USE STOP/START BUTTONS','SHUT OFF PANEL SWITCH','SHUT OFF VALVE AT MOTOR (PRESSURE)','USE STOP/START BUTTON ON MAGELIS','Custom','</ssProcedure>']
        with open('resources.txt', 'w') as f:
            for item in resourcedefault:
                f.write("%s\n" % item)
def displayTable():
    try:
        table = Table(title="Lockout Card")
        table.add_column("Equipment Number: "+equipnumber, justify="left", style="yellow", no_wrap=True)
        table.add_column("Equipment Name: "+equipname, style="white")
        table.add_column("Panel Room: "+str(panelroom[0]), justify="right", style="green")

        table.add_row("Electric Lockouts"                    , "Other Lockouts"                       , "eStops")
        table.add_row(el1.volts+"|"+el1.bucket+"|"+el1.proced, ol1.volts+"|"+ol1.bucket+"|"+ol1.proced, es1.location)
        table.add_row(el2.volts+"|"+el2.bucket+"|"+el2.proced, ol2.volts+"|"+ol2.bucket+"|"+ol2.proced, es2.location)
        table.add_row(el3.volts+"|"+el3.bucket+"|"+el3.proced, ol3.volts+"|"+ol3.bucket+"|"+ol3.proced, "Remote Lockouts")
        table.add_row(el4.volts+"|"+el4.bucket+"|"+el4.proced, ol4.volts+"|"+ol4.bucket+"|"+ol4.proced, rl1.location)
        table.add_row(el5.volts+"|"+el5.bucket+"|"+el5.proced, ol5.volts+"|"+ol5.bucket+"|"+ol5.proced, rl2.location)
        table.add_row(""                                     , ol6.volts+"|"+ol6.bucket+"|"+ol6.proced, rl3.location)
        table.add_row(""                                     , ""                                     , rl4.location)
        table.add_row(""                                     , ""                                     , rl5.location)
        table.add_row(""                                     , ""                                     , rl6.location)
        table.add_row(""                                     , ""                                     , rl7.location)
    except:
        pass
    return table
if __name__ == 'builder':
    try:
        el1 = Elockouts()
        el2 = Elockouts()
        el3 = Elockouts()
        el4 = Elockouts()
        el5 = Elockouts()
        ol1 = Olockouts()
        ol2 = Olockouts()
        ol3 = Olockouts()
        ol4 = Olockouts()
        ol5 = Olockouts()
        ol6 = Olockouts()
        es1 = eStops()
        es2 = eStops()
        rl1 = Rlockouts()
        rl2 = Rlockouts()
        rl3 = Rlockouts()
        rl4 = Rlockouts()
        rl5 = Rlockouts()
        rl6 = Rlockouts()
        rl7 = Rlockouts()
    except:
        pass
    template_file = "template.xlsx"
    wb = load_workbook(template_file)
    ws = wb['A']

    with console.screen(style="bold white on black") as screen:
        layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
        layout["upper"].size = 10
        #layout["lower"].size = 53
        layout["upper"].split_row(
        Layout(name="uleft"),
        Layout(name="uright"),
    )
        layout["uleft"].size=80
        layout["uright"].overflow="crop"
        #intro build
        intro = Text(justify="center")
        intro.append("Lockout Card Builder\n\n", style="bold cyan")
        intro.append(" Put any images for the cards in a subfolder layout show below\nAll images will need to be named properly for the program to utilize them\nAn example would be [Panel 2-3-5 2.jpg] the very last number in\nthe name will tell the program what spot to place the image.")
        layout["uleft"].update(Panel(intro))
        _ = system('cls')
        screen.update(layout)
        if checkonce:
            loading.append("Checking for required folders\n", style="yellow")
            #Check for folders and files.
            savepath = r"new/"
            imagepath = r"Photos/"
            dir = savepath
            if check_exists(dir):
                loading.append("Directory /new/ found!\n",style="green")
            else:
                loading.append("Directory /new/ is being created new cards will be in there\n",style="bright_white")
                os.mkdir(savepath)
                if check_exists(dir):
                    loading.append("Directory /new/ found!\n",style="green")
                else:
                    loading.append("RROR CANNOT CREATE DIRECTORY /new/ Check permissions and try again\n",style="red")
            if check_exists(imagepath):
                loading.append("Directory /Photos/ found!\n",style="green")
            else:
                loading.append("Directory /Photos/ being created.\n",style="bright_white")
                os.mkdir(imagepath)
                if check_exists(imagepath):
                    loading.append("Directory /Photos/ being created.\n")
                else:
                    loading.append("ERROR CANNOT CREATE DIRECTORY /Photos/ Check permissions and try again\n",style="red")
            loading.append("Loading resources...\n",style="yellow")
    
            try:
                with open('resources.txt') as f:
                    pass
            except IOError:
                generate_resources()
            with open('resources.txt') as f:
                prRecordingMode = False
                vRecordingMode = False
                oRecordingMode = False
                proRecordingMode = False
                for line in f:
                    if not prRecordingMode:
                        if line.startswith('<panelrooms>'):
                            prRecordingMode = True
                    elif line.startswith('</panelrooms>'):
                        prRecordingMode = False
                    else:
                        prlist.append(line)
                        prlist = [x.strip('\n') for x in prlist]
                        prlist = [x.strip('\t') for x in prlist]
                    if not vRecordingMode:
                        if line.startswith('<volts>'):
                            vRecordingMode = True
                    elif line.startswith('</volts>'):
                        vRecordingMode = False
                    else:
                        vlist.append(line)
                        vlist = [x.strip('\n') for x in vlist]
                        vlist = [x.strip('\t') for x in vlist]

                    if not oRecordingMode:
                        if line.startswith('<otherlockouts>'):
                            oRecordingMode = True
                    elif line.startswith('</otherlockouts>'):
                        oRecordingMode = False
                    else:
                        olist.append(line)
                        olist = [x.strip('\n') for x in olist]
                        olist = [x.strip('\t') for x in olist]
                    if not proRecordingMode:
                        if line.startswith('<ssProcedure>'):
                            proRecordingMode = True
                    elif line.startswith('</ssProcedure>'):
                        proRecordingMode = False
                    else:
                        prolist.append(line)
                        prolist = [x.strip('\n') for x in prolist]
                        prolist = [x.strip('\t') for x in prolist]

            loading.append("These records where found\n",style="cyan")
            loading.append("Panel Rooms: "+str(len(prlist))+"\n", style="cyan")
            loading.append("Voltages: "+str(len(vlist))+"\n", style="cyan")
            loading.append("Lockout Types: "+str(len(olist))+"\n", style="cyan")
            checkonce = False
        else:
            pass
        layout["uright"].update(Panel(loading, title="System Checks"))
        #ask to load crash file
        loadold = Align.center(
                Text.from_markup(f"Would you Like to load your previous data?", justify="center"),
                vertical="middle",style="bright_red"
            )
        layout["lower"].update(Panel(loadold))#Text("Would you Like to load your previous data?",style="bright_red",justify="center")))
        _ = system('cls')
        screen.update(layout)
        if Confirm.ask(""):
            with open('crash.bak', 'rb') as fp:
                crashsave = pickle.load(fp)
            prnsave=[]
            equipnumber=crashsave[0]
            equipname=crashsave[1]
            sdtype=crashsave[2]
            hz=crashsave[3]
            prnsave.append(crashsave[4])
            elsave=crashsave[5]
            el1.svolts=crashsave[6]
            el1.bucket=crashsave[7]
            el1.sproced=crashsave[8]
            el2.svolts=crashsave[9]
            el2.bucket=crashsave[10]
            el2.sproced=crashsave[11]
            el3.svolts=crashsave[12]
            el3.bucket=crashsave[13]
            el3.sproced=crashsave[14]
            el4.svolts=crashsave[15]
            el4.bucket=crashsave[16]
            el4.sproced=crashsave[17]
            el5.svolts=crashsave[18]
            el5.bucket=crashsave[19]
            el5.sproced=crashsave[20]
            olsave=crashsave[21]
            ol1.sType=crashsave[22]
            ol1.cType=crashsave[23]
            ol1.name=crashsave[24]
            ol1.proced=crashsave[25]
            ol1.sproced=crashsave[26]
            ol2.sType=crashsave[27]
            ol2.cType=crashsave[28]
            ol2.name=crashsave[29]
            ol2.proced=crashsave[30]
            ol2.sproced=crashsave[31]
            ol3.sType=crashsave[32]
            ol3.cType=crashsave[33]
            ol3.name=crashsave[34]
            ol3.proced=crashsave[35]
            ol3.sproced=crashsave[36]
            ol4.sType=crashsave[37]
            ol4.cType=crashsave[38]
            ol4.name=crashsave[39]
            ol4.proced=crashsave[40]
            ol4.sproced=crashsave[41]
            ol5.sType=crashsave[42]
            ol5.cType=crashsave[43]
            ol5.name=crashsave[44]
            ol5.proced=crashsave[45]
            ol5.sproced=crashsave[46]
            ol6.sType=crashsave[47]
            ol6.cType=crashsave[48]
            ol6.name=crashsave[49]
            ol6.proced=crashsave[50]
            ol6.sproced=crashsave[51]
            essave=crashsave[52]
            es1.location=crashsave[53]
            es2.location=crashsave[54]
            rlsave=crashsave[55]
            rl1.location=crashsave[56]
            rl2.location=crashsave[57]
            rl3.location=crashsave[58]
            rl4.location=crashsave[59]
            rl5.location=crashsave[60]
            rl6.location=crashsave[61]
            rl7.location=crashsave[62]
            prnsave.append(crashsave[63])
        enumask = Align.center(
                Text.from_markup(f"Enter Equipment number to begin. Example: 000-000000", justify="center"),
                vertical="middle",style="bright_red"
            )
        layout["lower"].update(Panel(enumask))
        _ = system('cls')
        screen.update(layout)
        equipnumber = Prompt.ask(" Equipment Number",default=equipnumber)
        checkphotostext = Text(justify="center")
        checkphotostext.append("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nChecking for Photos."+equipnumber+"\n", style="yellow")
        try:
            imgfolder = os.listdir(r'Photos/' + equipnumber + '/')
            checkphotostext.append("Checking Photo Dimensions\n", style="yellow")
            for file in imgfolder:
                corrected = imagepath+equipnumber+'/'+file
                resize_Image(corrected)
        except IOError as e:
            checkphotostext.append("No Photos Found.\nGet off you @$$ and take some!", style="red")
        #checkphotostext = Align.center(
                #Text.from_markup(checkphotostext, justify="center"),
                #vertical="middle",style="yellow"
            #)
        layout["lower"].update(Panel(checkphotostext))
        _ = system('cls')
        screen.update(layout)
        eqnametext = Align.center(
                Text.from_markup("Enter Equipment Name.", justify="center"),
                vertical="middle",style="cyan"
            )
        layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
        )
        layout["upper"].size = 20
        layout["lower"].update(Panel(eqnametext))
        table=displayTable()
        layout["upper"].update(Panel(table))
        _ = system('cls')
        screen.update(layout)
        equipname = Prompt.ask("Equipment Name",default=equipname)
        table=displayTable()
        layout["upper"].update(Panel(table))
        _ = system('cls')
        screen.update(layout)
        panelroom = select_PR(prnsave)

        table=displayTable()
        layout["upper"].update(Panel(table))
        _ = system('cls')
        screen.update(layout)

        prnsave=panelroom
        el = elecLockouts(elsave)
        elsave=el
        if el != 0:
            if el == 1:
                el1.gen_elect()
            if el == 2:
                el1.gen_elect()
                el2.gen_elect()
            if el == 3:
                el1.gen_elect()
                el2.gen_elect()
                el3.gen_elect()
            if el == 4:
                el1.gen_elect()
                el2.gen_elect()
                el3.gen_elect()
                el4.gen_elect()
            if el == 5:
                el1.gen_elect()
                el2.gen_elect()
                el3.gen_elect()
                el4.gen_elect()
                el5.gen_elect()
        ol = otherLockouts(olsave)
        olsave=ol
        if ol != 0:
            if ol == 1:
                ol1.gen_other()
            if ol == 2:
                ol1.gen_other()
                ol2.gen_other()
            if ol == 3:
                ol1.gen_other()
                ol2.gen_other()
                ol3.gen_other()
            if ol == 4:
                ol1.gen_other()
                ol2.gen_other()
                ol3.gen_other()
                ol4.gen_other()
            if ol == 5:
                ol1.gen_other()
                ol2.gen_other()
                ol3.gen_other()
                ol4.gen_other()
                ol5.gen_other()
            if ol == 6:
                ol1.gen_other()
                ol2.gen_other()
                ol3.gen_other()
                ol4.gen_other()
                ol5.gen_other()
                ol6.gen_other()
        es = eStop_count(essave)
        essave=es
        if es != 0:
            if es == 1:
                console.print("Where is the First eStop?",style="red")
                es1.gen_eStops()
            if es == 2:
                console.print("Where is the First eStop?",style="red")
                es1.gen_eStops()
                console.print("Where is the Second eStop?",style="red")
                es2.gen_eStops()
        rl = remoteLockouts(rlsave)
        rlsave=rl
        if rl != 0:
            if rl == 1:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
            if rl == 2:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
                console.print("Where is the 2nd Remote Lockout?",style="bright_white", justify="left")
                rl2.gen_remoteLockouts()
            if rl == 3:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
                console.print("Where is the 2nd Remote Lockout?",style="bright_white", justify="left")
                rl2.gen_remoteLockouts()
                console.print("Where is the 3rd Remote Lockout?",style="bright_white", justify="left")
                rl3.gen_remoteLockouts()
            if rl == 4:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
                console.print("Where is the 2nd Remote Lockout?",style="bright_white", justify="left")
                rl2.gen_remoteLockouts()
                console.print("Where is the 3rd Remote Lockout?",style="bright_white", justify="left")
                rl3.gen_remoteLockouts()
                console.print("Where is the 4th Remote Lockout?",style="bright_white", justify="left")
                rl4.gen_remoteLockouts()
            if rl == 5:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
                console.print("Where is the 2nd Remote Lockout?",style="bright_white", justify="left")
                rl2.gen_remoteLockouts()
                console.print("Where is the 3rd Remote Lockout?",style="bright_white", justify="left")
                rl3.gen_remoteLockouts()
                console.print("Where is the 4th Remote Lockout?",style="bright_white", justify="left")
                rl4.gen_remoteLockouts()
                console.print("Where is the 5th Remote Lockout?",style="bright_white", justify="left")
                rl5.gen_remoteLockouts()
            if rl == 6:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
                console.print("Where is the 2nd Remote Lockout?",style="bright_white", justify="left")
                rl2.gen_remoteLockouts()
                console.print("Where is the 3rd Remote Lockout?",style="bright_white", justify="left")
                rl3.gen_remoteLockouts()
                console.print("Where is the 4th Remote Lockout?",style="bright_white", justify="left")
                rl4.gen_remoteLockouts()
                console.print("Where is the 5th Remote Lockout?",style="bright_white", justify="left")
                rl5.gen_remoteLockouts()
                console.print("Where is the 6th Remote Lockout?",style="bright_white", justify="left")
                rl6.gen_remoteLockouts()
            if rl == 7:
                console.print("Where is the 1st Remote Lockout?",style="bright_white", justify="left")
                rl1.gen_remoteLockouts()
                console.print("Where is the 2nd Remote Lockout?",style="bright_white", justify="left")
                rl2.gen_remoteLockouts()
                console.print("Where is the 3rd Remote Lockout?",style="bright_white", justify="left")
                rl3.gen_remoteLockouts()
                console.print("Where is the 4th Remote Lockout?",style="bright_white", justify="left")
                rl4.gen_remoteLockouts()
                console.print("Where is the 5th Remote Lockout?",style="bright_white", justify="left")
                rl5.gen_remoteLockouts()
                console.print("Where is the 6th Remote Lockout?",style="bright_white", justify="left")
                rl6.gen_remoteLockouts()
                console.print("Where is the 7th Remote Lockout?",style="bright_white", justify="left")
                rl7.gen_remoteLockouts()
        sp = shutdownprocedure(sdtype)
        sdtype=sp
        hz = hazard(hz)

        sleep(1)