from HTMLParser import HTMLParser
import re
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fbusername= raw_input("Facebook username:")
pwd = getpass.getpass('Password:')

driver = webdriver.Firefox()
driver.get('http://www.facebook.com/');

#authenticate to facebook account
elem = driver.find_element_by_id("email")
elem.send_keys(fbusername)
elem = driver.find_element_by_id("pass")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)
time.sleep(5)

def getFBpage(url):
	time.sleep(2)
	driver.get(url);
	pos=-1
	posPrev=-1
	scrollHeight = 0
	while pos != scrollHeight:
		driver.execute_script("window.scrollBy(0,5000)");
		scrollHeight=driver.execute_script("return document.body.scrollHeight")
		pos=posPrev
		posPrev = scrollHeight
		print str(pos)+" "+str(scrollHeight)
		time.sleep(2)
		

	html_source = driver.page_source
	return html_source

def findFriendFromUrl(url):
	if re.search('com\/profile.php\?id=\d+\&',url) is not None:
		m=re.search('com\/profile.php\?id=(\d+)\&',url)
		friend=m.group(1)	
	else:
		m=re.search('com\/(.*)\?',url)
		friend=m.group(1)
	return friend	



class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
			if re.search('\?href|&href|hc_loca|\?fref', value) is not None:
				if re.search('.com/pages',value) is None:
					urls.append(value)


myUrl='http://www.facebook.com/'+fbusername+'/friends'
myFBlist=getFBpage(myUrl)

parser = MyHTMLParser()
urls=[]

parser.feed(myFBlist)
uniqUrls=set(urls)
outFile = open( 'edges_2.txt', 'w' )
num=1
for i in uniqUrls:
	f=findFriendFromUrl(i)
	print str(num)+ " of "+str(len(uniqUrls)) + " " +f
	outFile.write(fbusername+'\t'+f+'\n')
	url2='https://www.facebook.com/'+fbusername+'/friends?and=' + f
	urls=[]
	FBf=getFBpage(url2)
	parser.feed(FBf)
	fUrls=set(urls)
	for j in fUrls:
		ff=findFriendFromUrl(j)
		outFile.write(f+'\t'+ff+'\n')
	num=num+1

driver.quit()
outFile.close

