import requests 
import StringIO
import re
import os
from time import sleep
import datetime

# 0    1.   2.     3.     4.    5.  6.   7.        8.    9.    10
#Time;Type;Volume;Symbol;Price;S/L;T/P;Price;Commission;Swap;Profit

signalId=410865

botId="bot783031725:AAGYhejw98sY7g9umOw982kVxfm5y5oqmEg"
chatId="-326021916"

url = "https://www.mql5.com/en/signals/" + str(signalId) + "/export/trading"
cookies = dict(uniq='322AB655-6E70-S-181210',
			   auth='97981A168949C44B1922365C656AF0E9E281E413694D80EC57924DAF52AC6723DD65EB13CEAA0D7D317511C564075C046252B840BB3900BED1672D46B2E0239CD9BA725FB52A8CE889BACF4F874068F840DA23F5'
	)

def send_telegram(text):
    url="https://api.telegram.org/" + botId + "/sendMessage?chat_id=" + chatId + "&text=" + text
    response = requests.get(url)
    return response

while True:
	timeNow = datetime.datetime.now()
	print timeNow
	
	response = requests.get(url, cookies=cookies)
	responseString = StringIO.StringIO(response.text)
	orders_dates=[]

	if response.text:
		for line in responseString:
			order=line.split(";")
			if order[0] != 'Time':
				#print order
				file_name = order[0].replace(" ", '_' ).replace('.', '_').replace(':', '_')
				file_path = "orders/" + file_name
				orders_dates.append(file_name)
				#print file_path
				if not os.path.exists(file_path):
					#print "new order writing to file"
					textToSend=str("NEW "+ order[0] + " " + order[1]+ " " +order[2]+ " " + order[3]+ " " + order[4])
					print textToSend
					send_telegram(textToSend)
				   	f = open( file_path, 'w+')
				   	f.write(str(order))
				   	f.close()
				else:
					pass

	#clean closed orders
	order_files=os.listdir("orders/")

	files_diff=list(set(order_files).symmetric_difference(set(orders_dates)))
	if len(files_diff) > 0:
		for file in files_diff:
			#print "deleting order in " + file
			f = open("orders/" + file, 'r')
			content=f.read()
			textToSend="CLOSED " + str(content[0] + " " + content[1]+ " " + content[2]+ " " + content[3] + " " + content[4] )
			send_telegram(textToSend)
			print textToSend
			f.close()
			os.remove("orders/" + file) 
	sleep(60)
