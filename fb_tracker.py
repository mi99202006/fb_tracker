import requests
import time
import traceback
import sys
import json
init=True
try:
	with open('FBTrackerOption.txt', encoding = 'utf8') as OptionFile:
		FBTrackerOption = json.load(OptionFile)
except FileNotFoundError:
	print('IDTrackerOption.txt is not found')
	sys.exit()

ID=FBTrackerOption['IDList']
try:
	with open('cookies.txt') as cookiefile:
		cookie=cookiefile.read().rstrip('\n')
	#set cookies
	
except FileNotFoundError:
	print('cookies.txt is not found')
	sys.exit()

while True:
	try:
		s=requests.Session()
		s.headers.update({'cookie':cookie})
		res=s.get('https://www.facebook.com')
		text=res.text
		last_act_time_data=eval(text[text.find('lastActiveTimes')+16:text.find('}',text.find('lastActiveTimes')+1)+1])
		#load first time data
		if init:
				init=False
				old_data=last_act_time_data
				for key in ID:
						#print time,id,last active time,how long to last login 
						print(time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+key+'\t'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(old_data[key]))+'\t'+time.strftime('%H:%M:%S',time.gmtime(time.time()-last_act_time_data[key])))
						with open('log.txt','a') as log:
							log.write(time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+key+'\t'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(old_data[key]))+'\t'+time.strftime('%H:%M:%S',time.gmtime(time.time()-last_act_time_data[key]))+'\n')
		#keep tracking
		for key in ID:
			if old_data[key]!=last_act_time_data[key]:
				print(time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+key+'\t'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(old_data[key]))+'\t'+time.strftime('%H:%M:%S',time.gmtime(time.time()-last_act_time_data[key])))
				with open('log.txt','a') as log:
					log.write(time.strftime('%Y-%m-%d %H:%M:%S')+'\t'+key+'\t'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(old_data[key]))+'\t'+time.strftime('%H:%M:%S',time.gmtime(time.time()-last_act_time_data[key]))+'\n')
					old_data[key]=last_act_time_data[key]
	except KeyboardInterrupt:
		print('end')
		sys.exit()