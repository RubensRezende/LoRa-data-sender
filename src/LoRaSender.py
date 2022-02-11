import serial
import time
import logging
import threading
import json

#Log declaration
logging.basicConfig(filename="LoRaLog.log", format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO)

#Json file reading
with open('LoRaConfigurations.json') as j:
    json_data = json.load(j)
cont = 0 


# Serial portt configuration
#-------------------------------------------------------------------------------------------------------------------------------------
serialPort = json_data["system"][0]["port"]
baudratePort = json_data["system"][0]["baudrate"]

ser = serial.Serial(serialPort, baudratePort, timeout=0)
print("Comunication at", ser.name)    


#LoRa comunication parametres
#-------------------------------------------------------------------------------------------------------------------------------------
#Baseband
cmd= 'AT+DR='+str(json_data["lora"][0]["base_band"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["base_band"]) in x:  
                print("Base band settup complete")          
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Base band at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+DR='+str(json_data["lora"][0]["base_band"])+ '\r\n'
                        ser.write(cmd.encode()) 
                        cont=0               
                        time.sleep(1)   

#Baseband DR
cmd= 'AT+DR='+str(json_data["lora"][0]["base_band_DR"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["base_band_DR"]) in x:  
                print("Base band DataRate settup complete")          
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Base band DataRate at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+DR='+str(json_data["lora"][0]["base_band_DR"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1)          

#Subband 
for ch in range(0, 8):
        cmd = "AT+CH="+str(ch)+", 0\n"
        ser.write(cmd.encode())
        while True:
                x=ser.read(100).decode() 
                if str(ch) in x:  
                        print("Sucess disabling LoRa channel %s", ch)          
                        break
                else:
                        cont=cont+1
                        if cont >= 100000:
                                print("Failed disabling LoRa channel %s", ch)
                                cmd = "AT+CH="+str(ch)+", 0\n"
                                ser.write(cmd.encode())
                                cont=0

for ch in range(16, 65):
        cmd = "AT+CH="+str(ch)+", 0\n"
        ser.write(cmd.encode())
        while True:
                x=ser.read(100).decode() 
                if str(ch) in x:  
                        print("Sucess disabling LoRa channel %s", ch)          
                        break
                else:
                        cont=cont+1
                        if cont >= 100000:
                                print("Failed disabling LoRa channel %s", ch)
                                cmd = "AT+CH="+str(ch)+", 0\n"
                                ser.write(cmd.encode())
                                cont=0

for ch in range(66, 72):
        cmd = "AT+CH="+str(ch)+", 0\n"
        ser.write(cmd.encode())
        while True:
                x=ser.read(100).decode() 
                if str(ch) in x:  
                        print("Sucess disabling LoRa channel %s", ch)          
                        break
                else:
                        cont=cont+1
                        if cont >= 100000:
                                print("Failed disabling LoRa channel %s", ch)
                                cmd = "AT+CH="+str(ch)+", 0\n"
                                ser.write(cmd.encode())
                                cont=0

#Device class
cmd= 'AT+CLASS='+str(json_data["lora"][0]["class"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["class"]) in x: 
                print("Device class settup complete")           
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Device class at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+CLASS='+str(json_data["lora"][0]["class"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1)  

#Enable RX window 1
cmd= 'AT+RXWIN1=ON\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if "RXWIN1: ON" in x:
                print("RX window 1 settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("RX window 1 at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+DR='+str(json_data["lora"][0]["sub_band"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1) 


#Configure RX window 2
cmd= 'AT+RXWIN2='+str(json_data["lora"][0]["rxwin2_freq"])+','+str(json_data["lora"][0]["rxwin2_dr"])+'\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["rxwin2_dr"]) in x:
                print("RX window 2 settup complete")           
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("RX window 2 at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+RXWIN2='+str(json_data["lora"][0]["rxwin2_freq"])+','+str(json_data["lora"][0]["rxwin2_dr"])+'\r\n'
                        ser.write(cmd.encode())
                        time.sleep(1) 
                        cont=0


#Device operate mode
cmd= 'AT+MODE='+str(json_data["lora"][0]["auth_mode"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["auth_mode"]) in x:
                print("Device operate mode settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Device operate mode at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+DR='+str(json_data["lora"][0]["auth_mode"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1) 

#Device repeat message
cmd= 'AT+REPT='+str(json_data["lora"][0]["repeat"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["repeat"]) in x:
                print("Device repeat message settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Device repeat message at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+REPT='+str(json_data["lora"][0]["repeat"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1) 

#Device retry message
cmd= 'AT+RETRY='+str(json_data["lora"][0]["retry"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if str(json_data["lora"][0]["retry"]) in x:
                print("Device retry message settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Device retry message at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+RETRY='+str(json_data["lora"][0]["retry"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1) 

#TTN aplication configuration
#-------------------------------------------------------------------------------------------------------------------------------------
#Dev EUI
ttn_id=str(json_data["ttn"][0]["dev_eui"])
ttn_id=ttn_id[:2].lower()
cmd= 'AT+ID=DevEui,'+str(json_data["ttn"][0]["dev_eui"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if ttn_id in x:
                print("Device EUI settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Device EUI at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+ID=DevEui,'+str(json_data["ttn"][0]["dev_eui"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1)

#Dev Addr
ttn_id=str(json_data["ttn"][0]["dev_addr"])
ttn_id=ttn_id[:2].lower()
cmd= 'AT+ID=DevAddr,'+str(json_data["ttn"][0]["dev_addr"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if ttn_id in x:
                print("Device Addr settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Device Addr at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+ID=DevAddr,'+str(json_data["ttn"][0]["dev_addr"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1)

#Nwk S Key
ttn_id=str(json_data["ttn"][0]["nwks_key"])
ttn_id=ttn_id[:2]
cmd= 'AT+KEY=NwkSKey,'+str(json_data["ttn"][0]["nwks_key"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode() 
        if ttn_id in x:
                print("Network Session Key settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("Network Session Key at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+KEY=NwkSKey,'+str(json_data["ttn"][0]["nwks_key"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1)

#App S Key 
ttn_id=str(json_data["ttn"][0]["apps_key"])
cmd= 'AT+KEY=AppSKey,'+str(json_data["ttn"][0]["apps_key"])+ '\r\n'
ser.write(cmd.encode())
time.sleep(0.5)
while True:
        x=ser.read(100).decode()
        x= x.replace(" ", "") 
        if ttn_id[:2] in x:
                print("App Session Key settup complete")            
                break
        else:
                cont=cont+1
                if cont >= 100:
                        print("App Session Key at LoRa module are not correctly configured, trying again")
                        cmd= 'AT+KEY=AppSKey,'+str(json_data["ttn"][0]["apps_key"])+ '\r\n'
                        ser.write(cmd.encode())
                        cont=0
                        time.sleep(1)




#Test settup
#-------------------------------------------------------------------------------------------------------------------------------------
#Test
print("Starting test\n----------------------------------------")
numberMessages = json_data["system"][0]["number_of_messages"]
logging.info("Starting tests with "+ str(json_data["system"][0]["lora_module"]))
cmd= 'AT+MSG='+str(json_data["system"][0]["message"])+'\r\n'
cont=0


for i in range (numberMessages):
        ser.write(cmd.encode())
        time.sleep(0.1)

        while True:
                x=ser.read(100).decode('utf-8')
                time.sleep(0.5)
                if "Done" in x:            
                        break
                else:
                        cont=cont+1
                        #print(cont)
                        if cont >= 20:
                                cmd= 'AT+MSG='+str(json_data["system"][0]["message"])+'\r\n'
                                ser.write(cmd.encode())
                                cont = 0
        cont = 0

        print("message complete : %s" % str(i+1))

logging.info("Test with message : " + str(json_data["system"][0]["message"]))
logging.info("Test with : " + str(i+1)+ " messages")
logging.info("Finish tests with "+ str(json_data["system"][0]["lora_module"]))

