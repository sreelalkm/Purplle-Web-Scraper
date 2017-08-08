import json
import requests
from bs4 import BeautifulSoup

brands = ["L'Oreal", "Tresemme", "Dove"]
resObj = {'result':[]}                                  # JSON response object

def generateSearchURL(keyword, page_num):
    """For URLifying search keyword"""
    url = "https://www.purplle.com/searchnew/ajaxresults?list_type=search&list_type_value=" + keyword + "&page="\
             + str(page_num) + "&sort_by=rel&req_type=ajax&&type=next"
    return url

def addToJson(keyword, ranks):
    """Adding the calculated rank info to the json response object"""
    position = {'loreal': ranks[0], 'tresemme': ranks[1], 'dove': ranks[2]}
    resStruct = {'keyword': keyword, 'position': position}
    resObj['result'].append(resStruct)

def calculateRank(item_list):
    """Calculating rank for each brand"""
    ranks = [0, 0, 0]
    count = 1
    for item in item_list:
        name = item['item_name']
        for i in range(len(brands)):
            if (brands[i].lower() in name.lower()) & (ranks[i]==0):
                ranks[i] = count                                # Setting rank
        count = count + 1
    return ranks

def parse(keyword):
    """Parse the search results for the given keyword"""
    search_value = keyword
    search_value.replace(" ", "%20")
    curr_page = 1
    has_more = 1
    item_list = []

    while( (len(item_list) <= 100) & (has_more!=0) ):
        url = generateSearchURL(search_value, curr_page)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        elem_list = soup.find_all(class_="item")
        item_list.extend(elem_list)
        has_more = soup.find(id="has_more")['value']
        curr_page = curr_page + 1

    ranks = calculateRank(item_list)
    addToJson(keyword, ranks)

def main():
    """Main function.... Input and output"""
    print "Enter number of keywords: "
    N = int(input())
    keywords = []
    print "\nEnter keywords"
    for i in range(N):
        print "\nKeyword", i + 1, ":"
        x = raw_input()
        keywords.append(x)
    print "\nProcessing.... Please wait\n"
    for key in keywords:
        parse(key)
    with open('result.json', 'w') as outfile:                   # Writing to a JSON file
        json.dump(resObj, outfile)
    print json.dumps(resObj, indent=4)                          # Printing the JSON data

if __name__ == "__main__":
    main()