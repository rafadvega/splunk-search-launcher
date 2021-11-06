from getpass import getpass
import datetime
import sys
import splunklib.client as client
import splunklib.results as results
from prettytable import PrettyTable

__author__ = "Rafa de Vega"

######### CONFIGURATION ##########
host = 'mysplunk.org'
port = 8089
username = '' # if empty, script will request 
password = '' # if empty, script will request
db_name = 'launcher.db'
##################################

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

def main():
	try:
		service = splunkConnection()

		job = service.job(sys.argv[1])

		status = PrettyTable()
		status.field_names = ['State', 'Progress', 'Scanned', 'Matched', 'Results', 'Priority', 'Duration']
		status.add_row([job['dispatchState'], str(round(float(job['doneProgress'])*100,0))+"%", job['scanCount'], job['eventCount'], job['resultCount'], job['priority'], str(datetime.timedelta(seconds=round(float(job['runDuration']),0)))])

		print(status)
		print('\nMessages:\n')
		messages = job['messages']
		for level in messages:
			print(level)
			for message in messages[level]:
				print(message)

	except Exception as e:
		print("\nError:\t" + str(e))


if __name__ == "__main__":
    main()