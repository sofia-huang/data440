import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import urljoin
from urllib3.exceptions import NewConnectionError


def request_url(url):
    # try to request url, catches exception if invalid url is input
    try:
        response = requests.get(url)
    except NewConnectionError:
        print(f'Invalid URL: "{url}"')
    except Exception as e:
        print('There was an exception that occured when requesting the URL')
        print(e)
        return

    # get html text using BeautifulSoup
    soup = BeautifulSoup(response.text,features="html.parser")
    # counter to track how many pdf links on web page
    pdf_link_count = 0
    # loop through all links on web page
    for links in soup.find_all('a'):
        # make sure the full url is obtained from the href attribute
        href = links.get('href')
        full_url = urljoin(url, href)
        link_response = requests.get(full_url)
        # use regex to see if link is a pdf using its content type header
        pattern = re.compile('([a-z]+\/)(pdf)')
        m = pattern.match(link_response.headers['Content-Type'])
        # if link is pdf, print necessary info
        if (m != None):
            # print URI
            print ("URI: {}".format(link_response.url))
            # print final URI, following redirects if necessary
            if (str(link_response.status_code)[0] != '3'):
                print ("Final URI: {}".format(link_response.url))
            else:
                redirect_response = requests.get(link_response.url)
                while (str(link_response.status_code)[0] == '3'):
                    redirect_response = requests.get(link_response.url)
                print ("Final URI: {}".format(redirect_response.url))
            # print content length
            print ("Content-Length: {:,} bytes \n".format(int(link_response.headers['Content-Length'])))
            pdf_link_count += 1
        
    print('Number of pdf links: {}'.format(pdf_link_count))

'''     
    link_response = requests.get(href, allow_redirects=False)
        
    if (link_response.headers['Content-Type'][-3:] == 'pdf'):
        print ("URI: {}\n".format(link_response.url))
        print ("Content-Length: {} bytes".format(link_response.headers['Content-Length']))

    print ("Content-Type: {}".format(link_response.headers['Content-Type']))
    print(links.get('href'))

    #url_pattern = re.compile('(https?:\/\/)(.+)')
    #match_url = url_pattern.match(full_url)
    #if (match_url != None):
        #link_response = requests.get(full_url)
    #else: 
        #link_response = requests.get("{}{}".format(url, href))

    print ("Status Code: {}".format(response.status_code))
    print ("URI: {}\n".format(response.url))

    print ("Headers: {}\n".format(response.headers))
    print ("Date: {}".format(response.headers['Date']))
    print ("Content-Type: {}".format(response.headers['Content-Type']))
    print ("Content-Length: {}".format(response.headers['Content-Length']))
'''


if __name__ == "__main__":
    # https://alexandernwala.com/files/teaching/fall-2022/week-2/2018_wsdl_publications.html
    # https://haipeng-chen.github.io/
    # http://www.math.wm.edu/~rrkinc/teaching.html
    input_url = str(sys.argv[1])
    request_url(input_url)

    '''
    references:
    https://stackoverflow.com/questions/4007302/regex-how-to-match-an-optional-character
    https://stackoverflow.com/questions/17972496/using-beautiful-soup-to-get-the-full-url-in-source-code
    https://www.geeksforgeeks.org/response-status_code-python-requests/

    '''