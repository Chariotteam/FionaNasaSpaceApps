import math
import time
import os
import time
import subprocess
from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
import os
import sys
import glob
import serial
import time


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 






bind_host = "192.168.0.104"	#listening ip
bind_port = 5000	#listening port

target_host = "127.0.0.1"	
target_port = 4545	

last_sec = 0
count = 0
client = udp_client.SimpleUDPClient(target_host, target_port)



def eeg_handler(address, eeg, tp9, af7, af8, tp10, fpz):
    print(tp10)
    now=datetime.now()
    seconds = now.second
    global count
    global last_sec
   
    if abs(seconds - last_sec) > 2:
        command = " "
        if count == 1:
            print('command1')
            
            command = 'command1'

            
        elif count >= 2:
            print('command2')
            command = 'command2'
        count = 0  
        if command != " ":
            files = os.listdir(command)
            for file in files:
                if('.sh' in file):
                    try:
                        subprocess.run(['chmod', '+x', './{}/{}'.format(command,file)])
                    except:
                        pass
                    os.system('./{}/{}'.format(command,file))
                    
                elif '.py' in file:
                    process_name = open("process.sh","w")
                    process_name.write('cd {}/'.format(command))
                    process_name.write('\n')
                    process_name.write('python {}'.format(file))
                    process_name.close()
                    os.system('./process.sh')
                    
                elif '.cpp' in file:
                    process_name = open("process.sh","w")
                    process_name.write('cd {}/'.format(command))
                    process_name.write('\n')
                    process_name.write('g++ '+file+' -o '+ 'out/'+file.split('.')[0]+'.out')
                    process_name.write('\n')
                    process_name.write('./'+'out/'+file.split('.')[0]+'.out')
                    process_name.write('\ncd')
                    process_name.close()
                    os.system('./process.sh')
        
    
    if(float(tp10) > 1300):
        print('command')
       
        
        
        if abs(seconds - last_sec) > 0.001:
            last_sec = seconds
            count+=1
      
           
    """
	client.send_message("/muse/eeg/tp9", tp9)
	client.send_message("/muse/eeg/af7", af7)
	client.send_message("/muse/eeg/af8", af8)
	client.send_message("/muse/eeg/tp10", tp10)
	client.send_message("/muse/eeg/fpz", fpz)
    """

"""
def alpha_handler(address,alpha,val):
	client.send_message("/muse/elements/alpha_absolute", val)

def beta_handler(address,beta,val):
	client.send_message("/muse/elements/beta_absolute", val)
	
def delta_handler(address,delta,val):
	client.send_message("/muse/elements/delta_absolute", val)

def theta_handler(address,theta,val):
	client.send_message("/muse/elements/theta_absolute", val)

def gamma_handler(address,gamma,val):
	client.send_message("/muse/elements/gamma_absolute", val)
"""

if __name__ == "__main__":

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/eeg", eeg_handler, "EEG")
    """
    dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, "ALPHA")
    dispatcher.map("/muse/elements/beta_absolute", beta_handler, "BETA")
    dispatcher.map("/muse/elements/delta_absolute", delta_handler, "DELTA")
    dispatcher.map("/muse/elements/theta_absolute", theta_handler, "THETA")
    dispatcher.map("/muse/elements/gamma_absolute", gamma_handler, "GAMMA")
    """
    server = osc_server.ThreadingOSCUDPServer( (bind_host, bind_port), dispatcher)
    print("Listening on {}".format(server.server_address))
    server.serve_forever()