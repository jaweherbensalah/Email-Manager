import os
import re
import pandas as pd
from functools import reduce
import argparse
import sys


# ***************************************************
# Filtering the emails from csv file
# and converting it to a text file
# ***************************************************

#  This fct will extract emails from the original file last-email-pack.csv
# and save it to a text file emails/emails_from_csv.txt
def writeFile(listData, fileToWrite):
    file = open(fileToWrite, 'w+')
    strData = ""
    for item in listData:
        strData = strData+item+'\n'
    file.write(strData)


# Use list comprehension to remove the unwanted column in **usecol**
df = pd.read_csv("emails/last-email-pack.csv", sep=';')
# print(df.columns)
del (df['username'])
# this creats a list of lists of emails
list_emails = df.values.tolist()
# this creats a list of emails
output = reduce(lambda x, y: x+y, list_emails)
# this creats a text file of emails
writeFile(output, 'emails/emails_from_csv.txt')

# *********************************************************
# Task 1
# *********************************************************


def validateEmail(strEmail):
    # .* Zero or more characters of any type.
    if not re.match("(.*){1,}\@{1,1}(.*){1,}.[0-9a-zA-Z]{1,4}", strEmail):
        return True
    return False


def incorrect_emails():
    listEmail = []
    for filename in os.listdir("emails"):
        if filename.endswith('.txt'):
            with open(os.path.join("emails", filename), 'r') as file:
                listLine = file.readlines()
                for itemLine in listLine:
                    item = str(itemLine)
                    for delimeter in [',', ';']:
                        item = item.replace(str(delimeter), ' ')

                    wordList = item.split()
                    for word in wordList:
                        if(validateEmail(word)):
                            listEmail.append(word)

    if listEmail:
        writeFile(listEmail, 'task1.txt')
        print(f'Invalid emails: ({len(listEmail)})')
        for em in listEmail:
            print(em+'\n')
    else:
        print("No email found.")

# *****************************************
     # Task 2
# *****************************************


def search_by_text():
    listEmail = []
    fopen = open('emails/emails_from_csv.txt', mode='r+')
    fread = fopen.readlines()
    x = input("Enter the search string: ")
    for line in fread:
        if x in line:
            listEmail.append(line)
    if listEmail:
        writeFile(listEmail, 'task2.txt')
        print(f'Found emails: ({len(listEmail)})')
        for em in listEmail:
            print(em+'\n')
    else:
        print("No email found.")

# *****************************************
     # Task 3
# *****************************************
def group_by_domain():
    listDomains = []
    listEmails = []
    file = open("emails/emails_from_csv.txt")
    for line in file:
        line = line.strip()
        listEmails.append(line)
        domains = re.findall('@[0-9a-zA-z]+\.[0-9a-zA-z]+', line)
        # this for loop will extract the domains and save it to a list
        for domain in domains:
            if domain in line:
                listDomains.append(domain)

    emailSet = set(listEmails)
    emailSet = sorted(emailSet)
    domainSet = set(listDomains)
    domainSet = sorted(domainSet)
    em = []

    for d in domainSet:
        for e in emailSet:
            if re.search(d.strip(), e.strip()):
                em.append(e)
                writeFile(em, 'task3.txt')
                print(f'Domain {d} ({len(em)}):')
                for item in sorted(em):
                    print('     ', item)

            else:
                em = []

# ***************************************************
# Task 4
# ***************************************************


def feil_path_to_logs_file():
    # convert the logs file to acsv file
    read_file = pd.read_csv(r'email-sent.logs')
    read_file.to_csv('email-sent.csv', index=None)

    # Use list comprehension to remove the unwanted column in **usecol**
    df = pd.read_csv("email-sent.csv", sep="'")
    print(df.columns)
    # del (df['username'])
    # l=df.values.tolist()

    # Drop columns based on column index.
    # df2 = df.drop(df.columns[[0, 1]],axis = 1)
    # print(df.iloc[: , -2])
    emails_sent = df.iloc[:, -2].values.tolist()
    writeFile(emails_sent, 'task4.txt')

    listEmails = []
    file = open("emails/emails-pack-2.txt")
    for line in file:
        line = line.strip()
        listEmails.append(line)

    emailSet = set(listEmails)
    emailSet = sorted(emailSet)
    comp = [item for item in emailSet if item not in emails_sent]
    print(len(comp))


# ************************************************************
    # Creating commands for each task
# ************************************************************
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Task 1 : incorrect emails command.
parser_showtop20 = subparsers.add_parser('ic', help='List of incorrect emails')
parser_showtop20.set_defaults(func=incorrect_emails)

# Task 2 : Search emails by text command.
parser_listapps = subparsers.add_parser('search', help='Search emails by text')
parser_listapps.set_defaults(func=search_by_text)

# Task 3 : Group_by_domain command.
parser_listapps = subparsers.add_parser('gbd', help='Group emails by domain')
parser_listapps.set_defaults(func=group_by_domain)

# Task 4 : Find emails that are not in the logs file command.
parser_listapps = subparsers.add_parser(
    'feil_path_to_logs_file', help=' Find emails that are not in the logs file')
parser_listapps.set_defaults(func=feil_path_to_logs_file)

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()

# Run the appropriate function (in this case ic or search ...etc)
options.func()

# If you add command-line options, consider passing them to the function,
# e.g. `options.func(options)`
