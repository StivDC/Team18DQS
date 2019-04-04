import csv
import html 
import requests


biglist = [] 
with open ('data.csv', 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	next(csvreader)
	for row in csvreader: 
		biglist.append(row)
		print(biglist)


def sort():
        biglist.sort(key=i: x[1])
        print(biglist)


test_list= [] 
def match(x):
        counter_1 = 0
        for x in biglist:
                while biglist[counter_1][1] == biglist[counter_1+1][1]:
                       test_list.append(biglist[counter_1])
                       counter_1 += 1
        test_list.append(biglist[counter_1])            
        print(test_list)
        


def average(x):
        counter_3 = 0
        counter_2 = 0 
        total = 0
        for i in test_list:
                counter_3 +=1
                questionno = i[3]
                counter_2 += int(i[2])
                average = ((float(counter_2) / float((questionno))))
                total += average
                print(total)
                final = (float(total) / float(counter_3) * 100)
                counter_2 = 0
        print(float(final))

def attempts_per_student(x):
        counter_4 = 0
        counter_5 = 0
        for i in test_list:
                counter_4 +=1
                counter_5 += int(i[4])
        attempts = float(counter_5) / float(counter_4)
        print(float(attempts))


def main():
        sort()
        match(biglist)
        average(test_list)
        attempts_per_student(test_list)
                
        


