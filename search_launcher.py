import splunklib.client as client
import splunklib.results as results
import pickle
from prettytable import PrettyTable
import os
from getpass import getpass
import datetime
import pandas as pd

__author__ = "Rafa de Vega"

def printLogo():
    print("""                         _       _                        _               
 ___  ___  __ _ _ __ ___| |__   | | __ _ _   _ _ __   ___| |__   ___ _ __ 
/ __|/ _ \/ _` | '__/ __| '_ \  | |/ _` | | | | '_ \ / __| '_ \ / _ \ '__|
\__ \  __/ (_| | | | (__| | | | | | (_| | |_| | | | | (__| | | |  __/ |   
|___/\___|\__,_|_|  \___|_| |_| |_|\__,_|\__,_|_| |_|\___|_| |_|\___|_|\n\n""")


######### CONFIGURATION ##########
host = 'mysplunk.org'
port = 8089
username = '' # if empty, script will request 
password = '' # if empty, script will request
db_name = 'launcher.db'
##################################


def printHelp():
    print ("\n cancel   -\tcancel search jobs and delete local data of search")
    print (" clear    -\tclear local database")
    print (" create   -\tcreate new search")
    print (" delete   -\tdelete search from local database")
    print (" download -\tdownload search results")
    print (" help     -\tprint help")
    print (" list     -\tlist searches")
    print (" login     -\tLogin splunk with new credentials")
    print (" load     -\tload search from sid")
    print (" status   -\tview search status")  
    print (" quit     -\texit\n")
    print (" Press Ctrl+C to cancel operation\n")


def login():
	try:
		global username
		global password
		username = input('splunk user: ')
		password = getpass('splunk pass: ')
		splunkConnection()
	except KeyboardInterrupt:
		print("\nOperation canceled")
	except Exception as e:
		print(e)
		login()


def splunkConnection():
    #Check credentials
    global username
    global password
    if username == '':
        username = input('splunk user: ')
    if password == '':
        password = getpass('splunk pass: ')
    # Create a Service instance and log in 
    service = client.connect(
        host=host,
        port=port,
        username=username,
        password=password)
    return service


def loadDB():
    try:
        if os.path.exists(db_name):
            with open(db_name, 'rb') as f:
                db = pickle.load(f)
                return db
        else:
            db = {};
            return db
    except Exception as e:
        print("\nError:\t" + str(e))

    exit()


def saveDB(data):
	if type(data) == dict:
		with open(db_name, 'wb') as f:
			pickle.dump(data, f)
	elif type(data) == list:
		db = loadDB()
		db[data[0]]= data[1]
		with open(db_name, 'wb') as f:
			pickle.dump(db, f)


def listDB():
	try:
		searchesList = loadDB()
		list_searches = PrettyTable()
		list_searches.field_names = ['Search', 'Sid']
		for search in searchesList:
		    list_searches.add_row([search,searchesList[search]])
		print(list_searches)
		print()
	except Exception as e:
	    print("\nError:\t" + str(e))


def delete(search_name):
	try:
		if not search_name:
			print("Warning. This option doesn't delete search from splunk.")
			search_name = input('Enter search name: ')
		db = loadDB()
		if not search_name in db.keys():
	            print("The search name doesn't exists\n")
	            return False
		del db[search_name]
		saveDB(db)
		print ("\nSearch deleted!")
	except KeyboardInterrupt:
		print("\nOperation canceled")
	except Exception as e:
		print("\nError:\t" + str(e))


def cancel():
	try:			
		search_name = input('Enter search name: ')
		db = loadDB()
		if not search_name in db.keys():
			print("The search name doesn't exists\n")
			return False
		sid = db[search_name]
		service = splunkConnection()
		job = service.job(sid)
		job.cancel()
		print ("Job canceled!\n")
		sure = input("Do you want delete search from local database? y/(n): ")
		if sure == "Y" or sure == "y":
			delete(search_name)
	except KeyboardInterrupt:
		print("\nOperation canceled")
	except Exception as e:
		print("\nError:\t" + str(e))


def loadSid():
	try:
		search_name = input('Enter search name: ')
		if search_name in loadDB().keys():
			print("The search name already exists\n")
			return False
		search_sid = input('Enter search sid: ')
		saveDB([search_name,search_sid])
		search = PrettyTable()
		search.field_names = ['Search', 'Sid']
		search.add_row([search_name,search_sid])
		print(search)
		print("\nSearch Loaded\n")
	except KeyboardInterrupt:
		print("\nOperation canceled")
	except Exception as e:
		print("\nError:\t" + str(e))


def clear():
	sure = input("This option deleted all local database, but not the splunk searches. Are you sure? y/(n): ")
	if sure == "Y" or sure == "y":
		print("\nBye Bye dabase...\n")
		os.remove(db_name)
	else:
		print("\nDon't touch my database!!\n")


def status():
    try:
        search_name = input('Enter search name: ')
        db = loadDB()
        sid = db[search_name]
        service = splunkConnection()
        status = PrettyTable()
        status.field_names = ['is Done','State', 'Progress', 'Scanned', 'Matched', 'Results', 'Duration', 'Sid']
        
        job = service.job(sid)
        status.add_row([bool(job['isDone']),job['dispatchState'], str(round(float(job['doneProgress'])*100,0))+"%", job['scanCount'], job['eventCount'], job['resultCount'], str(datetime.timedelta(seconds=round(float(job['runDuration']),0))), sid])
        print()
        print(status)
        print('\nMessages:\n')
        messages = job['messages']
        for level in messages:
        	print(level)
        	for message in messages[level]:
        		print(message)
        print()
    except KeyboardInterrupt:
    	print("\nOperation canceled")
    except Exception as e:
    	print("\nError:\t" + str(e))


def download():
	try:
		search_name = input('Enter search name: ')
		db = loadDB()
		if not search_name in db.keys():
			print("The search name doesn't exists\n")
			return False
		sid = db[search_name]
		dump_filename = input('Enter file name to save results: ')
		service = splunkConnection()
		job = service.job(sid)

		if bool(int(job['isDone'])) == True:
			rr = results.ResultsReader(job.results(count=0))
			df = pd.DataFrame(list(rr))
			if(int(job['resultCount']) > 0):
				print ("\nSaving results...")
				df.to_csv(dump_filename, index=False)
				print ("\nDownloaded!")
			else:
				print("The search has 0 results\n")            
		else:
			print("\nThe search is not finished\n")
	except KeyboardInterrupt:
		print("\nOperation canceled")
	except Exception as e:
		print("\nError:\t" + str(e))


def create():
	try:
		search_name = input('Enter search name: ')
		if search_name in loadDB().keys():
			print("The search name already exists\n")
			return False
		searchquery = input('Enter splunk search (oneline format):')
		earliest_time = input('Enter earliest time (format: 2021-11-03T0:0:0)": ')
		latest_time = input('Enter latest time (format: 2021-11-04T0:0:0): ')
		service = splunkConnection()
		kwargs_normalsearch = {"exec_mode": "normal", "earliest_time": earliest_time, "latest_time": latest_time}		
		job = service.jobs.create(searchquery, **kwargs_normalsearch)
		job.set_ttl(1000)
		job.refresh()
		saveDB([search_name, job['sid']])
		print("Done!")
	except KeyboardInterrupt:
		print("\nOperation canceled")
	except Exception as e:
		print("\nError:\t" + str(e))


def main():
	printLogo()
	try:

		while True:
			option = input('>> ')
			if option == 'create':
			    create()
			elif option == 'status':
			    status()
			elif option == 'delete':
			    delete('')
			elif option == 'download':
			    download()
			elif option == 'cancel':
			    cancel()
			elif option == 'clear':
			    clear()
			elif option == 'help':
			    printHelp()
			elif option == 'list':
			    listDB()
			elif option == 'load':
			    loadSid()
			elif option == 'login':
				login()
			elif option == 'quit' or option == 'exit':
			    print('\n Goodbye!!')
			    exit()
			else:
			    print("Invalid option. Plese enter a valid comand or 'help' to print all commands.")

	except KeyboardInterrupt:
		print("\nOperation canceled")


if __name__ == "__main__":
    main()