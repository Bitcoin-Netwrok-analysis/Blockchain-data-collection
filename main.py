# to get http request's respond 
import requests
# time module to convert yyyy-mm-dd to millisec
from datetime import datetime
import delorean 
# for writing csv file
import csv

# function for converting time to millisec
def timestamp(dt):
    return delorean.Delorean(dt, timezone='UTC').epoch * 1000

# list that will contain millisec for which we want past 24 hr blocks
millisec_list = []

# taking inputs
n = int(input())
for i in range(n):
    year = int(input())
    month = int(input())
    date = int(input())
    millisec_list.append(int(timestamp(datetime(year,month,date))))
    
     
# Making a get request and geting hash of all the required blocks
block_hashes = []
for i in range(n):   
    response = requests.get(f'https://blockchain.info/blocks/{millisec_list[i]}?format=json').json()
    for j in response:
        block_hashes.append(j["hash"])
        

count = 0
total = 0
error = 0

# file names where we will store processed data
input_file = 'input.csv'
output_file = 'output.csv'

with open(input_file,mode = 'a',newline = '') as inp:
    with open(output_file,mode = 'a', newline = '') as out:
        csvwriter1 = csv.writer(inp)
        csvwriter2 = csv.writer(out)
        

        for i in block_hashes:
            response = requests.get(f'https://blockchain.info/rawblock/{i}').json()["tx"][1:] #transactions list
            for j in response: # particular transactions
                for k in j["inputs"]:
                    if "addr" in k["prev_out"]:
                        temp_input = [count]
                        temp_input.append(k["prev_out"]["addr"])
                        temp_input.append(k["prev_out"]["value"])
                        csvwriter1.writerow(temp_input)
                    else:
                        error +=1
                    total+=1
                for k in j["out"]:
                    if "addr" in k:
                        temp_out = [count]
                        temp_out.append(k["addr"])
                        temp_out.append(k["value"])
                        csvwriter2.writerow(temp_out)
                    else:
                        error+=1
                    total+=1
                count += 1
            print(error/total)
