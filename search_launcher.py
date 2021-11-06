import splunklib.client as client
import splunklib.results as results
import pickle
from prettytable import PrettyTable
import os

__author__ = "Rafa de Vega"

def printLogo():
    print("""                         _       _                        _               
 ___  ___  __ _ _ __ ___| |__   | | __ _ _   _ _ __   ___| |__   ___ _ __ 
/ __|/ _ \/ _` | '__/ __| '_ \  | |/ _` | | | | '_ \ / __| '_ \ / _ \ '__|
\__ \  __/ (_| | | | (__| | | | | | (_| | |_| | | | | (__| | | |  __/ |   
|___/\___|\__,_|_|  \___|_| |_| |_|\__,_|\__,_|_| |_|\___|_| |_|\___|_| \n\n""")


######### CONFIGURATION ##########
host = 'mysplunk.org'
port = 8089
username = '' # if empty, script will request 
password = '' # if empty, script will request
db_name = 'launcher.db'
##################################


def printHelp():
    print ("\n cancel   - cancel search jobs and delete local data of search")
    print (" create   - create new search")
    print (" download - download search results")
    print (" help     - print help")
    print (" list     - list searches")
    print (" load     - load search from sid")
    print (" status   - view search status")  
    print (" quit     - exit\n")

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


def create():
	print("pending...")


def status():
	print("pending...")


def download():
	print("pending...")


def cancel():
	print("pending...")


def loadSid():
	print("pending...")


def main():

	printLogo()

	while True:

		option = input('>> ')
		if option == 'create':
		    create()
		elif option == 'status':
		    status()
		elif option == 'download':
		    download()
		elif option == 'cancel':
		    cancel()
		elif option == 'help':
		    printHelp()
		elif option == 'list':
		    listDB()
		elif option == 'load':
		    loadSid()
		elif option == 'quit' or option == 'exit':
		    print('\n Goodbye!!')
		    exit()
		else:
		    print("Invalid option. Plese enter a valid comand or 'help' to print all commands.")


if __name__ == "__main__":
    main()