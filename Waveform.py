import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import keyboard


PORT = 'COM8'         
BAUD = 115200
WINDOW_SIZE = 1000   

 

#setting parameters
voltages = np.zeros(WINDOW_SIZE)
time_stamps = np.zeros(WINDOW_SIZE)
MID_Point = 2.7
plt.style.use('bmh')
fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot(time_stamps, voltages, color='tab:red', linewidth=2)
datalog = []

ax.set_title("Line Voltage Monitoring")
ax.set_xlabel("Time (Seconds)")
ax.set_ylabel("Voltage (V)")


ax.set_ylim(0,300) 
ax.grid(True)

start_time = time.time() # used to start the timer

try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print(f"Connected. Streaming...")
except Exception as e:
    print(f"Error: {e}")
    exit()

while True:
    if ser.in_waiting > 0:
        try:
            
            raw = ser.readline().decode('utf-8').strip() 
            print(raw)
            new_val = float(raw) #typecasting to float
            print(new_val)
            new_val1 = (150/3450)*new_val
            print(new_val1)
            # --- NUMPY ROLLING LOGIC ---
            voltages = np.roll(voltages, -1)
            time_stamps = np.roll(time_stamps, -1)
            
            voltages[-1] = new_val1
            time_stamps[-1] = time.time() - start_time
            voltages1 = (150/3450)*voltages 
            
            
            # Update plot data
            line.set_xdata(time_stamps)
            line.set_ydata(voltages)
            
            # Auto-scroll X-axis. Just adding new value overwriting past values
            ax.set_xlim(time_stamps[0], time_stamps[-1])
            
            # Update Title with live values
            
            current_time = time.strftime("%H-%M-%S")
            new_row = {
                "Voltages" : new_val1,
                "Time" : current_time
            }
            datalog.append(new_row)
            
            if keyboard.is_pressed("q"):
                df = pd.DataFrame(datalog)
                df.to_excel("ZMPT.xlsx")
                exit()
                ser.close()
                
                
                break
            else:
                plt.draw()
                plt.pause(0.001) # Faster pause for smoother wave
                
            
        
        except ValueError:
            pass
        except KeyboardInterrupt:
            break

ser.close() 