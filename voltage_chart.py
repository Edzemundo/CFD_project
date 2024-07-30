import pathlib
import serial
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.animation as animation



# Initialize plot
def livePlot():
    global xs, ys, ax, fig
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    


def connect(serialPort, baudRate):
    # Initialize serial connection
    global ser
    ser = serial.Serial(serialPort, baudRate)
    if not ser.isOpen():
        try:
            ser.open()
            window["statustext"].update("Connected")
            window["connect"].update(disabled=True)
            window["disconnect"].update(disabled=False)
            window["chart"].update(disabled=False)

        except serial.SerialException:
            sg.Popup("Error connecting to Arduino. Please check your serial port settings.")
        except FileNotFoundError:
            sg.Popup("Error connecting to Arduino. Please check your serial port settings.")
    else:
        window["statustext"].update("Connected")
        window["connect"].update(disabled=True)
        window["disconnect"].update(disabled=False)
        window["chart"].update(disabled=False)

    
        
def createCSV(filename):
    global file
    with open(filename, 'w') as file:
        file.write("Time,Voltage\n")
        for i, y in zip(xs, ys):
            file.write(f"{i},{y}\n")

def update(i):
    try:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        voltage = float(line)  # Convert the line to a float
        xs.append(i)
        ys.append(voltage)
        ax.clear()
        ax.plot(xs, ys)
    except ValueError:
        pass
    except serial.serialutil.PortNotOpenError:
        sg.popup("Port closed")
        plt.close()
        window.close()


#------------------------------------------------------------------------------------------------------------------------

layout = [[sg.Text("Enter filepath for CSV: "), sg.Input(key="filepath", default_text=str(pathlib.Path.home())+f"\\Downloads\\"), sg.FileBrowse(key="filebrowse")],
          [sg.Text("Enter device location:  ", key="devicepathtext"), sg.Input(key="devicepathinput", default_text="COM3")],
          [sg.Text("Enter baud rate:          ", key="baudratetext"), sg.Input(key="baudrateinput", default_text="9600")],
          [sg.Push(), sg.Text("", key="statustext"), sg.Push()],
          [sg.Checkbox("Create CSV file", key="createCSV", default=True)],
          [sg.Button("Connect", key="connect"), sg.Button("Disconnect", key="disconnect", disabled=True), sg.Button("Chart", key="chart", disabled=True)]]

window  = sg.Window("CFD Project (github.com/Edzemundo)", layout=layout, size=(555,190))

while True:
    event, values = window.read()
    
    if event == "connect":
        connect(values["devicepathinput"], int(values["baudrateinput"]))
        print(values["devicepathinput"], values["baudrateinput"])
        livePlot()
        if values["createCSV"]:
            createCSV(values["filepath"])
    
            
    if event == "disconnect":
        ser.close()
        window["statustext"].update("Disconnected")
        window["connect"].update(disabled=False)
        window["disconnect"].update(disabled=True)
        
        
    if event == "chart":
        ani = animation.FuncAnimation(fig, update, interval=100)
        fig.show()
    
    if event == sg.WIN_CLOSED:
        break