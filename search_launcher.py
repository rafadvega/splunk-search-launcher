import splunklib.client as client
import splunklib.results as results

__author__ = "Rafa de Vega"

def printLogo():
    print("""                         _       _                        _               
 ___  ___  __ _ _ __ ___| |__   | | __ _ _   _ _ __   ___| |__   ___ _ __ 
/ __|/ _ \/ _` | '__/ __| '_ \  | |/ _` | | | | '_ \ / __| '_ \ / _ \ '__|
\__ \  __/ (_| | | | (__| | | | | | (_| | |_| | | | | (__| | | |  __/ |   
|___/\___|\__,_|_|  \___|_| |_| |_|\__,_|\__,_|_| |_|\___|_| |_|\___|_| \n\n""")


def printHelp():
    print ("\n cancel   - cancel search jobs and delete local data of search")
    print (" create   - create new search")
    print (" download - download search results")
    print (" help     - print help")
    print (" list     - list searches")
    print (" load     - load search from sid")
    print (" status   - view search status")  
    print (" quit     - exit\n")


def create():
	print("pending...")


def status():
	print("pending...")


def download():
	print("pending...")


def cancel():
	print("pending...")


def list():
	print("pending...")


def load():
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
		    list()
		elif option == 'load':
		    list()
		elif option == 'quit' or option == 'exit':
		    print('\n Goodbye!!')
		    exit()
		else:
		    print("Invalid option. Plese enter a valid comand or 'help' to print all commands.")


if __name__ == "__main__":
    main()