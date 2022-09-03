import sys
import os
import re
import pickle

# Method to open the data file and read in the text
def method1(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        f.readline()
        text_in = f.read()
    return text_in

# Person object to hold the data of the employees
class Person:

    def __init__(self):
        self.last = ''
        self.first = ''
        self.mi = ''
        self.id = ''
        self.phone = ''

# displays the employee info
    def display(self):
        print('Employee id: ' + self.id)
        print(self.first + ' ' + self.mi + ' ' + self.last)
        print(self.phone + '\n')

# Takes the text from the file and processes it, making the names, ids, and numbers uniform while checking for errors
def processtext(text):
    newtext = text.split("\n")
    pdict = {}
    for i in newtext:
        p = Person()
        line = i.split(",")
        p.last = line[0].lower().capitalize()
        p.first = line[1].lower().capitalize()
        if line[2] == '':
            p.mi = 'X'
        else:
            p.mi = line[2].capitalize()
        if re.match('[a-zA-Z]{2}\d{4}', line[3]):
            p.id = line[3].upper()
        else:
            print('ID invalid: ' + line[3] + '\nID is two letters followed by 4 digits')
            p.id = input('Please enter a valid ID: ').upper()

        num = [*line[4]]
        if len(num) == 10:
            _ = ""
            num.insert(3, '-')
            num.insert(7, '-')
            p.phone = _.join(num)
        elif num[3] == num[7]:
            _ = ""
            num[3] = '-'
            num[7] = '-'
            p.phone = _.join(num)
        else:
            print('Phone ' + line[4] + ' is invalid\nEnter phone number in form 123-456-7890')
            p.phone = input('Enter phone number: ')

# Adds the completed employee person to an employee dictionary, with their id as the key unless it exists already
        if p.id in pdict:
            print('Error: ID '+p.id+' already exists, person not added.')
        else:
            pdict[p.id] = p
    return pdict

# Checks if there is a system argument passed and if not returns an error
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
# If sys arg is passed, runs the process text method and adds the dictionary to a pickle file
        fp = sys.argv[1]
        data = method1(fp)
        list = processtext(data).copy()
        pickle.dump(list, open('dict.p', 'wb'))
        dict_in = pickle.load(open('dict.p', 'rb'))
        for i in dict_in:
            dict_in.get(i).display()
