#! /usr/bin/python
#@author: mani-iyer(mani.waran@gmail.com)

import os
from time import sleep
from datetime import datetime
import subprocess

####################################################################
#Setting the parameters that will be used for searching the log file
####################################################################

#Strings that you want the script to search for
#Put the words the you want to search for in the list
w = ['OutOfMemoryError','ERROR','WARN','EXCEPTION', 'Invalid']

#Log file that the script needs to search for errors
#Path to file
file_name ='[PATH-TO-FILE]'

#The log where the errors if found  will be logged
#The location where you want to store the result file
monitoring_log = '[PATH-TO-FILE]'

#New name of the log that needs to be renamed after logging
#The error_log file will be renamed in the end to reflect the log name
new_name = 'catalina_'

#log location to where the logs needs to be stored
#The place where you will finally store the error logs
#Usually this is a shared directory so that the logs can be accessed from anywhere
log_location = '/data/filer_01/monitoring/logs/api/'

#Set the sleep time so that it can loop for ever
sleep_in_seconds=3600

#Set the line number as 0 for the first iteration
#The script will start iterating from line 1 and in the 
#subsequent iterations it will take the stored value 
#from the script 
line_num = 1

#################################################################
#Starting the loop
#################################################################

while True:
	#Using the try method to find if the file exists
        try:
                file = open(file_name, 'r')
		            file.seek(line_num)
        except IOError:
                print "File ", file_name, " not found at the specified location"
                sys.exit(1)

        #Open the error_log file for writing
	log = open(monitoring_log, 'a')

	#Finding the current time for logging information
        curr_time = str(datetime.now())
        log.write ("logging monitoring info at:")
        log.write (curr_time)
        log.write ('\n')
        log.write ("--------------------------------------------------------------------------")
        log.write ('\n')

	#Iterating through the Log file to find the errors and print them in the error_log
        for line in file:
                for word in w:
                        if word in line:
                                log.write(line)
                                log.write ('\n')
        log.write ('\n')
        log.write ("***************END LOGGING***************")
        log.write ('\n')

	#Close the error_log file
        log.close()

	#Finding the line number to be used after reopening the file
	line_num = file.tell()

	#Close the log file
	file.close()

	#Log Rollover
        filename = new_name+curr_time+'.txt'
        os.rename(monitoring_log, filename)
	subprocess.call(["mv", filename, log_location])

	#The sleep process or the forever loop
        sleep (sleep_in_seconds)
