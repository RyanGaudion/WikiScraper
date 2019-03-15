import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

#CSV File:
#Each line is new page
#Commas between pages
#First page is the main page


def getLinksFromPage(page):
    linksarray = []
    #uses soup to access wiki homepage
    try:
        soup = BeautifulSoup(urlopen("https://en.wikipedia.org/wiki/"+page), 'lxml')
    except:
        return False
    #for each a tag in soup
    for link in soup.find_all("a"):
        #for each link get where it links to
        link = str(link.get("href"))
        #if link links to somewhere else on wiki
        if link[:5] == "/wiki":
            #remove /wiki from start of file
            link = link[5:]
            #make sure link is not a special page
            if link[:10] != "/Template:" and link[:6] != "/User:" and link[:9] != "/Special:" and link[:11] != "/Wikipedia:" and link[:8] != "/Portal:" and link[:6] != "/File:" and link[:6] != "/Talk:" and link[:6] != "/Help:" and link[:10] != "/Category:":
                #remove / from start of file and add to array
                linksarray.append(link[1:])
    return linksarray

def removeDuplicateLinks(array):
    NewArray = []
    for link in array:
        if link not in NewArray:
            NewArray.append(link)
        else:
            pass
    return NewArray

def isPageAlreadyInFile(name, file):
    doneArray = []
    with open(file, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            try:
                doneArray.append(row[0])
            except:
                pass
    if name in doneArray:
        return True
    else:
        return False

def addPageToFile(array,file,check):
    if check == 1:
        if isPageAlreadyInFile(array[0], file) == True:
            return "Check: True"
        
    with open(file, "a", newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(array)
            

def sortArray(array):
    return array.sort()

def fullPageToFile(page):
    linkArray = removeDuplicateLinks(getLinksFromPage(page))
    linkArray.sort()
    linkArray.insert(0,page.lower())
    addPageToFile(linkArray,"wikiscrape.csv",1)

def option1():
    page = input("What page would you like the links from?")
    linkArray = removeDuplicateLinks(getLinksFromPage(page))
    linkArray.sort()
    for link in linkArray:
        print(link)

def option2():
    page = input("What page would you like the links from?")
    fullPageToFile(page)

def option3():
    with open("wikiScrape.csv", "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            for item in row:
                if isPageAlreadyInFile(item, "wikiScrape.csv") == True:
                    pass
                else:
                    fullPageToFile(item)
                    print(item, "has been added!")
            input()

def Main():
    print("Options:")
    print("1 - print links from a certain page")
    print("2 - add 1 page to file")
    print("3 - auto update 1 line in csv")
    whatToDo = input()
    if whatToDo == "1":
        option1()
    elif whatToDo == "2":
        option2()
    elif whatToDo == "3":
        option3()

Main()
