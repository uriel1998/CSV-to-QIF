'''**************************************************************************/
#
#    @file    CSV_to_QIF.py
#    @author   Mario Avenoso (M-tech Creations)
#    @contributor   Steven Saus (uriel1998)
#    @license  MIT (see license.txt)
#
#    Program to convert from a CSV to a QIF file using a definitions
#    to describe how the CSV is formatted
#
#    @section  HISTORY
#    v0.3 - added multiple columns, multiple file export based on account name, etc
#    v0.2 - Added payee ignore option  1/18/2016 feature update
#    v0.1 - First release 1/1/2016 beta release
#
'''#**************************************************************************/


import os
import sys
import re
import csv

#
#     @brief  Takes given CSV and parses it to be exported to a QIF
#
#     @params[in] inf_
#     File to be read and converted to QIF
#     @params[in] outf_
#     File that the converted data will go
#     @params[in] deff_
#     File with the settings for converting CSV
#
#
def readCsv(inf_,deff_,tofile_): #will need to receive input csv and def file

    csvdeff = csv.reader(deff_, delimiter=',')

    next(csvdeff,None)


    for settings in csvdeff:
        date_= int(settings[0])  #convert to int
        amount_ = int(settings[2])  #How much was the transaction
        memo_ = int(settings[3])  #discription of the transaction
        payee_ = int(settings[4])  #Where the money is going
        deli_ = settings[5] #How the csv is separated
        header_ = int(settings[6])  #Set if there is a header to skip

        if len(settings) <= 7:  #for backward compatibility
            sign_ = -1
            category_ = -1
            account_ = tofile_  #a string instead of a handle so it works with everything
        else:
            sign_ = int(settings[7])  #Which direction of sign
            category_ = int(settings[8])  #Which direction of sign
            account_ = int(settings[9])  #Which account this is
            
        
    csvIn = csv.reader(inf_, delimiter=deli_)  #create csv object using the given separator
    
    if header_ >= 1: #If there is a header skip the fist line
        next(csvIn,None)  #skip header
    
    if len(settings) <= 7:  #for backward compatibility
        for row in csvIn:
            writeFile(row[date_],row[amount_],row[memo_],row[payee_],sign_,category_,tofile_,tofile_)  #export each row as a qif entry
    
    else:
    
        for row in csvIn:
            writeFile(row[date_],row[amount_],row[memo_],row[payee_],row[sign_],row[category_],row[account_],tofile_)  #export each row as a qif entry

#
#     @brief Receives data to be written to and its location
#
#     @params[in] date_
#     Data of transaction
#     @params[in] amount_
#     Amount of money for transaction
#     @params[in] memo_
#     Description of transaction
#     @params[in] payee_
#     Transaction paid to
#     @params[in] filelocation_
#     Location of the Output file
#
#
# https://en.wikipedia.org/wiki/Quicken_Interchange_Format
#


# because this function opens and closes the file each call (nice!) it's
# trivial then for me to substitute in filenames per ACCOUNT. 

def writeFile(date_,amount_,memo_,payee_,sign_,category_, account_, filelocation_):

    
    if filelocation_ == "builtin":
        suffix = '.qif'
        tofile = os.path.join(os.getcwd(), account_ + suffix)
    else:
        tofile = account_


    outFile = open(tofile,"a")  #Open file to be appended
    outFile.write("!Type:Cash\n")  #Header of transaction, Currently all set to cash
    outFile.write("D")  #Date line starts with the capital D
    outFile.write(date_)
    outFile.write("\n")
    
    outFile.write("T")  #Transaction amount starts here
    if(sign_!=-1):
        if sign_ in ('debit', 'DEBIT'):           
            aamount_ = 0 - float(amount_)
            outFile.write(str(aamount_))
        elif sign_ in ('credit', 'CREDIT'):           
            outFile.write(amount_)
    else:    
        outFile.write(amount_)
    
    outFile.write("\n")

    outFile.write("M")  #Memo Line
    outFile.write(memo_)
    outFile.write("\n")

    if(category_!=-1):   #for backward compatibility
        outFile.write("L")  #Category
        outFile.write(category_)
        outFile.write("\n")    


    if(payee_!=-1):
        outFile.write("P")  #Payee line
        outFile.write(payee_)
        outFile.write("\n")

    outFile.write("^\n")  #The last line of each transaction starts with a Caret to mark the end
    outFile.close()

def convert():

    error = 'Input error!____ Format [import.csv] [output.csv] [import.def] ____\n\n\
            OR -builtin [import.csv] [import.def]\n\
            [import.csv] = File to be converted\n\
            [output.qif] = File to be created OR switch\n\
            [import.def] = Definition file describing csv file\n'

    if (len(sys.argv) != 4):  #Check to make sure all the parameters are there
        print error
        exit(1)

    if sys.argv[1].lower() == "--builtin":   # for backward compatibility
        tofile = "builtin"

        if os.path.isfile(sys.argv[2]):
            fromfile = open(sys.argv[2],'r')
        else:
            print '\nInput error!____ import.csv: ' + sys.argv[2] + ' does not exist / cannot be opened !!\n'
            exit(1) 
        if os.path.isfile(sys.argv[3]):
            deffile = open(sys.argv[3],'r')
        else:
            print '\nInput error!____ import.def: ' + sys.argv[3] + ' does not exist / cannot be opened !!\n'
            exit(1)
    else:
        
        if os.path.isfile(sys.argv[1]):
            fromfile = open(sys.argv[1],'r')
        else:
            print '\nInput error!____ import.csv: ' + sys.argv[1] + ' does not exist / cannot be opened !!\n'
            exit(1)
            
        try:
            tofile   = open(sys.argv[2],'a')
        except:
            print '\nInput error!____ output.csv: ' + sys.argv[2] + ' cannot be created !!\n'
            exit(1)

        tofile.close()
        tofile = sys.argv[2]   # changed this from a file handle to a string for backward compatibility.
        
        if os.path.isfile(sys.argv[3]):
            deffile = open(sys.argv[3],'r')
        else:
            print '\nIDDDnput error!____ import.def: ' + sys.argv[3] + ' does not exist / cannot be opened !!\n'
            exit(1)
        
    readCsv(fromfile,deffile,tofile)

    fromfile.close()
    deffile.close()

convert()#Start
