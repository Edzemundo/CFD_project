import os
import serial
import pathlib
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize plot
def livePlot():
    """_summary_
    """
    global xs, ys, ax, fig, ani
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    ani = animation.FuncAnimation(fig, update, interval=100)
    fig.show()


def connect(serialPort, baudRate):
    """_summary_

    Args:
        serialPort (_type_): _description_
        baudRate (_type_): _description_
    """
    # Initialize serial connection
    global ser
    
    try:
        ser = serial.Serial(serialPort, baudRate)
        
        if not ser.isOpen():
            ser.open()
            window["statustext"].update("Connected")
            window["connect"].update(disabled=True)
            window["disconnect"].update(disabled=False)
            window["chart"].update(disabled=False)
        else:
            window["statustext"].update("Connected")
            window["connect"].update(disabled=True)
            window["disconnect"].update(disabled=False)
            window["chart"].update(disabled=False)

    except serial.SerialException:
        sg.Popup("Error connecting to Arduino. Please check your serial port settings.")
        exit()

        
def createCSV(filename):
    """_summary_

    Args:
        filename (_type_): _description_
    """
    global file
    with open(filename, 'w') as file:
        file.write("Time,Voltage\n")
        for i, y in zip(xs, ys):
            file.write(f"{i},{y}\n")
    

def update(i):
    """_summary_

    Args:
        i (_type_): _description_
    """
    try:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        voltage = float(line)  # Convert the line to a float
        xs.append(i)
        ys.append(voltage)
        ax.clear()
        ax.plot(xs, ys)
        if values["createCSV"]:
            createCSV(filelocation)
    except ValueError:
        pass
    except serial.serialutil.PortNotOpenError:
        sg.popup("Port closed")
        plt.close()
        window.close()


#*****GUI*****
#------------------------------------------------------------------------------------------------------------------------
sg.theme("DarkBlue5")

layout = [[sg.Text("Filename(without .csv):", key="filenametext"), sg.Input(key="filename")],
          [sg.Text("Enter filepath for CSV: "), sg.Input(key="filepath", default_text=os.path.join(str(pathlib.Path.home()), "Desktop")), sg.FolderBrowse(key="filebrowse")],
          [sg.Text("Enter device location:  ", key="devicepathtext"), sg.Input(key="devicepathinput", default_text="/dev/cu.usbmodem14101")],
          [sg.Text("Enter baud rate:          ", key="baudratetext"), sg.Input(key="baudrateinput", default_text="9600")],
          [sg.Push(), sg.Text("", key="statustext"), sg.Push()],
          [sg.Checkbox("Create CSV file", key="createCSV", default=True, enable_events=True)],
          [sg.Button("Connect", key="connect"), sg.Button("Disconnect", key="disconnect", disabled=True), sg.Push(), sg.Button("Chart", key="chart", disabled=True)]]

window  = sg.Window("CFD Project (github.com/Edzemundo)", layout=layout, size=(555,210))

while True:
    event, values = window.read()
    
    filelocation = os.path.join(values["filepath"], values["filename"] + ".csv")
    
    if event == "createCSV":
        if values["createCSV"]:
            window["filenametext"].update(visible=True)
            window["filename"].update(visible=True)
        else:
            window["filenametext"].update(visible=False)
            window["filename"].update(visible=False)           
    
    if event == "connect":
        print(filelocation)
        if values["createCSV"]:
            try:
                open(filelocation, "w")
                connect(values["devicepathinput"], int(values["baudrateinput"]))
                print(values["devicepathinput"], values["baudrateinput"])
                livePlot()
            except (FileNotFoundError, IsADirectoryError, OSError):
                window["statustext"].update("Filename not/improperly entered or path not/improperly entered")

        elif not values["createCSV"]:
            connect(values["devicepathinput"], int(values["baudrateinput"]))
            print(values["devicepathinput"], values["baudrateinput"])
            livePlot()
        
            
    if event == "disconnect":
        window["statustext"].update("Disconnected")
        window["connect"].update(disabled=False)
        window["disconnect"].update(disabled=True)
        plt.close()
        ser.close()
        
    if event == "chart":
        fig.show()
              
        
    if event == sg.WIN_CLOSED:
        break