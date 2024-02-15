import serial
import re
import json
import sys

# Define the serial port settings
port = 'COM9'  # Change this to match your serial port
baud_rate = 115200  # Change this to match your baud rate

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 send_side.py COMX")
        return

    port = sys.argv[1]
    # Open the serial port
    ser = serial.Serial(port, baud_rate)

    # Open a file to save the data
    file_path = 'send_data.csv'
    n=1
    with open(file_path, 'w') as file:
        out = 'topic,temp,co2,ir,date,time,fire-score'
        print(' ', out)
        file.write(out + '\n')
        try:
            while True:
                # Read a line of data from the serial port
                line = ser.readline().decode().strip()
                #print(line)
                if not line.startswith('splavice'):
                    print(f'skip {line}')
                    continue
                    
                i=line.find('{')
                input= line[i:]
                topic=line[:i-1]
                #print(input)
                j = json.loads(input)
                #print(n, j)
                out = f'''{topic},{j['temp']},{j['co2']},{j['ir']},{j['time'].split(' ')[0]},{j['time'].split(' ')[1]},{j['fire-score']}'''
                # Write the data to the file
                file.write(out + '\n')
                file.flush()  # Flush the buffer to ensure data is written ij.ediately

                # Print the data to the console (optional)
                print(n, out)
                n+=1

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Closing the serial port.")
            ser.close()
        
if __name__ == "__main__":
    main()
