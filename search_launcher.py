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
    print (" load     -\tload search from sid")
    print (" status   -\tview search status")  
    print (" quit     -\texit\n")


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


def loadSid():
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


def clear():
	sure = input("This option deleted all local database, but not the splunk searches. Are you sure? y/(n): ")
	if sure == "Y" or sure == "y":
		print("\nBye Bye dabase...\n")
		os.remove(db_name)
	else:
		print("\nDon't touch my database!!\n")

def main():

	printLogo()

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
		elif option == 'quit' or option == 'exit':
		    print('\n Goodbye!!')
		    exit()
		else:
		    print("Invalid option. Plese enter a valid comand or 'help' to print all commands.")


if __name__ == "__main__":
    main()