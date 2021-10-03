#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 07:55:02 2021

@author: timur
"""

import os
import sys
import glob
import serial
import time


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

all_ports=[]

devices=[]

class Device:
    def ___init__(self):
        self.port=''
        
    def connect(self):
        self.ser = serial.Serial(port=self.port, baudrate=9600)
        self.ser.close()
        
    def write(self, val):
        self.ser = serial.Serial(port=self.port, baudrate=9600)
        self.ser.close()
        self.ser.open()
        self.ser.write(val.encode())
        time.sleep(5)

        
    


       

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    return ports  

ports=serial_ports()
print(ports)
mover=serial.Serial(port=input('com:'), baudrate=9600)



import requests
import datetime
import pandas as pd
import urllib.request
import telebot
import os
import shutil
from threading import Timer
from distutils.dir_util import copy_tree
import subprocess
from recognizer import recognize



os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class abs_bot():
    
    def __init__(self,token):
        self.api_url = "https://api.telegram.org/bot"+token+"/"
        self.token=token
        
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    
    def forward_message(self, chat_id, from_id, mess_id):
        params = {'chat_id': chat_id, 'from_chat_id': from_id, 'message_id': mess_id }
        method = 'forward_message'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
            return last_update
       

       



token="your_token_here"
bot = abs_bot(token)
bot2=telebot.TeleBot(token)
now = datetime.datetime.now()
path=str(os.path.dirname(os.path.realpath(__file__)))+'/'






def main():  
    new_offset = None
    
    while True:
        try:
            bot.get_updates(new_offset)
        except Exception:
            #print('Connection error')
            continue
       
        last_update = bot.get_last_update()
        if(type(last_update) == type({}) and ('message' in last_update or 'callback_query' in last_update)):
            last_update_id = last_update['update_id']
            
            if('callback_query' in last_update):
                callback_query = last_update['callback_query']
            
                username=last_update['callback_query']['from']['username']
                
                #print(callback_query)
              
                mess=callback_query['data']
                print(mess)
                if mess == 'fire':
                    mover.write(b'a')
                
                
            
            
            else:
                last_chat_id = last_update['message']['chat']['id']
                #print(last_update['message'])
                if('text' in last_update['message']):
                    last_chat_text = last_update['message']['text']
               
                    mess=last_chat_text.lower()
                    
                    if mess == '/fire' or mess == 'ок':
                        mover.write(b'a')
                    
                    
                   
                            
                    elif(mess == '/start' or mess == '/help'):
                        
                            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
                          
                            button = telebot.types.InlineKeyboardButton(text='Fire', 
                                                                        callback_data='fire')
                            
                            markup.add(button)
                           
                            
                            
                            bot2.send_message(chat_id=last_chat_id, 
                                            text='Select the command',reply_markup=markup)
                    else:
                        
                        mover.write(bytes(mess, 'utf-8'))
                            
                            
                 
                         
                    
                elif ('voice' in last_update['message']):
                    if 'username' in last_update['message']['chat']:
                        username=last_update['message']['chat']['username']
                        file_id=last_update['message']['voice']['file_id']
                        #print(file_id)               
                        link='https://api.telegram.org/bot'+token+'/getFile?file_id='+file_id
                        file_info=pd.read_json(link) 
                        link2='https://api.telegram.org/file/bot'+token+'/'+file_info['result']['file_path']
                        #print(link2)
                        f_name=file_info['result']['file_path']
                        
                        try:
                           
                            format_f=f_name.split('.')[-1]
                            directory_us='tf_files/'+username+'/voice'
                            
                            if not os.path.exists(directory_us):
                                os.makedirs(directory_us)                                         
                                        
                            file_loc=directory_us+'/'+'command'+'.oga'
                            
                            urllib.request.urlretrieve(link2, file_loc)
                            wav_file=directory_us+'/'+'command'+'.wav'
                            try:
                                os.remove(wav_file)
                            except:
                                pass
                            subprocess.run(['ffmpeg', '-i', file_loc, wav_file])
                            mess=str(recognize(wav_file))
                            print(mess)
                            
                               
                        
                           
                                
                        except Exception as error:
                                bot.send_message(last_chat_id, str(error))
                        
                    else:
                        
                        bot.send_message(last_chat_id, 'Missing username')
                        
                
                    
            new_offset = last_update_id + 1
        
        

if __name__ == '__main__':  
    try:
        while True:
            try:
                main()
            except Exception as error:
                print(error)
                time.sleep(15)
    except KeyboardInterrupt:
        exit()