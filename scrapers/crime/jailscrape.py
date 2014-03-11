import os
import requests
import csv
import lxml.html
import pickle

url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'

# Download the page
if os.path.exists('response.p'):
    with open('response.p', 'rb') as fp:
        response = pickle.load(fp)
else:
    response = requests.get(url)
    with open('response.p', 'wb') as fp:
        pickle.dump(response, fp)

# Open the HTML file and turn it into a BeautifulSoup object for parsing
raw = response.text
html = lxml.html.fromstring(raw)

# Now we start reading the website. Let's get the table that contains the results.
only_table = html.cssselect('table.resultsTable')[0]

output_trs = [] # The list that's going to store all of our output rows

# First we need to loop through all the rows in the table
for tr in only_table.cssselect('tr'):

    # And next, we want to get all the cells within each of the rows
    tds = tr.cssselect('td')

    # We'll store all of the values for each given row in a list
    output_tds = []
    for td in tds:
        output_tds.append(td.text_content().replace('&nbsp;', '')) # Delete annoying tab character

    # And we'll add that list to our broader list of results
    output_trs.append(output_tds)

# Finally, we'll write our results to a file
handle = open('out.csv', 'a')
outfile = csv.writer(handle)

outfile.writerows(output_trs)
