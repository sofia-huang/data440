# get_tweets.py - Credit: MCW

import sys
import json
from twarc import Twarc2, expansions
from configparser import ConfigParser
import re
from subprocess import call
import requests
import os
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt  
import pandas as pd  

TWARC_CONFIG_FILE = "/Users/sofiahuang/Library/Application Support/twarc/config"
OUTPUT_FILE = "/Users/sofiahuang/Documents/WM/FALL2022/DATA440/tweets.jsonl"   # line-oriented JSON
MAX_TWEETS = 100

def get_tweets(input_search_term):
    # read Twitter API keys from twarc config file, setup twarc2 object
    config = ConfigParser(interpolation=None)
    with open(TWARC_CONFIG_FILE) as twarc_config:
        config.read_string("[TWARC]\n" + twarc_config.read())
    bearer_token = config['TWARC']['bearer_token'].strip('\'')
    t = Twarc2(bearer_token=bearer_token)

    search_term = input_search_term

    # limit search results to English language, with links, and no retweets
    query = search_term + " lang:en has:links -is:retweet"

    search_results = t.search_recent(query=query, max_results=MAX_TWEETS)
    # max_results is the number of results per page

    num_tweets = 0
    for page in search_results:
    # use expansions.flatten to get all the information in a single JSON
        result = expansions.flatten(page)

    # open the file and write one JSON object per new line (jsonl format)
        with open(OUTPUT_FILE, 'a+') as filehandle:   # if you want to append, change 'w' to 'a+'
            for tweet in result:
                print(tweet)
                filehandle.write('%s\n' % json.dumps(tweet))
                num_tweets = num_tweets + 1
                if num_tweets == MAX_TWEETS:
                # must include this to stop after a certain # of tweets
                    search_results.close()

    print (num_tweets, "tweets written to " + OUTPUT_FILE + " for query \"" + query + "\"\n");

def get_links():
    f = open(OUTPUT_FILE)
    # read in all the lines
    lines = f.readlines()  
    links = []
    resolved_links = []
    # each line is a json 
    for line in lines:
        tweet_data = json.loads(line) 
        # collect links 
        if 'urls' in tweet_data['entities']:
            for link in tweet_data['entities']['urls']:
                # check if link leads to a Twitter or video/audio only page using regex
                pattern = re.compile('(https:\/\/)(www\.|.*)(twitter|youtube|youtu|tiktok|twitch|soundcloud)(\.com|\.be)(.*)')
                m = pattern.match(link['expanded_url'])
                if (m == None):
                    # add to list if link leads to an acceptable page (not Twitter or video/audio)
                    links.append(link['expanded_url'])
                    #print('original: ' + link['expanded_url'])
                    try:
                        # resolve links to their final URI
                        resolved_link = requests.head(link['expanded_url'], allow_redirects=True, timeout=5).url
                        resolved_links.append(resolved_link)
                        #print('final: ' + resolved_link)
                    except:
                        continue
    print('Originally ' + str(len(links)) + ' links.')
    print('Resolved ' + str(len(resolved_links)) + ' links.')
    os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440")
    # create txt file to store the resolved links
    resolved_uri_file = os.path.join(os.getcwd(), 'resolved_uris.txt')
    for link in resolved_links:
        try:
            with open(resolved_uri_file, 'a+') as f:
                f.write("\n%s" % link)
                print(link)
        except Exception as e:
            print(e)
    return resolved_links

def read_unique_links_file(txt_filename):
    # check if we are in the correct directory
    os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440")
    summary_filename = os.path.join(os.getcwd(), txt_filename)
    # read the resolved links txt file into a list to be returned
    try:
        summary_file = open(summary_filename, 'r')
        url_data = summary_file.read()
        unique_list = url_data.split("\n")
        summary_file.close()
        print(str(len(unique_list)))
        return unique_list
    except Exception as e:
        print(e)
        return []

def get_timemaps(list, directory):
    # to keep track of how many URIs timemaps are obtained for
    # and to name the timemaps json file returned from MemGator
    link_index = 1
    for uri in list:
        filename = str(link_index) + ".json"
        # create a folder to store the timemaps
        if os.path.exists(os.path.join(directory, filename)):
            # file has already been created, just increment index and go to the next file
            print("Skipping url " + uri + ", file already exists")
            link_index += 1
            continue
        else:
            # run MemGator on each URI in the unique links list
            print('running memgator on: ' + uri)
            time.sleep(1)
            os.system('/Users/sofiahuang/Downloads/memgator-darwin-amd64 -F 2 -f JSON ' + uri + ' > /Users/sofiahuang/Documents/WM/FALL2022/DATA440/timemaps/' + filename)
            time.sleep(2)

def count_mementos():
    # create dictionary and add entry for URI-Rs with 0 mementos
    mem_dict = {0:0}
    os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/timemaps")
    file_count = 0
    # iterate over json files
    for json_file in os.listdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/timemaps"):
        # open json file
        f = open(json_file, 'r')
        if (json_file == '.DS_Store'):
            continue
        # if file is 0 bytes, don't read, just add data to dictionary
        if (os.stat(json_file).st_size == 0):
            current_val = mem_dict.get(0)
            mem_dict.update({0: current_val+1})
            file_count+=1
            continue
        # read json file
        data = json.loads(f.read())
        # get number of mementos and add to dictionary, 
        # checking if key is already in the dictionary
        mementos = data['mementos']['list']
        mem_count = len(mementos)
        if mem_count in mem_dict:
            current_val = mem_dict.get(mem_count)
            mem_dict.update({mem_count: current_val+1})
        else:
            mem_dict.update({mem_count: 1})
        f.close()
        file_count+=1
        print(file_count)

    # open file for writing dictionary to csv file
    w = csv.writer(open("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/memento_counts.csv", "w"))
    # loop over dictionary keys and values
    for key, val in mem_dict.items():
        # write every key and value to file
        w.writerow([key, val])

def get_memento_age():
    # create dictionary and add entry for URI-Rs with 0 mementos
    mem_dict = {0:0}
    os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/timemaps")
    file_count = 0
    memento_counts = []
    memento_ages = []
    uris = []
    # iterate over json files
    for json_file in os.listdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/timemaps"):
        # open json file
        f = open(json_file, 'r')
        # if file is 0 bytes, don't read
        if (os.stat(json_file).st_size == 0):
            continue
        # read json file
        data = json.loads(f.read())
        # get earliest date 
        memento_earliest_date_str = data['mementos']['list'][0]['datetime']
        memento_earliest_date = datetime.strptime(memento_earliest_date_str[0:10], '%Y-%m-%d')
        memento_age = (datetime.today() - memento_earliest_date).days
        # add data to lists
        memento_ages.append(memento_age)
        memento_counts.append(len(data['mementos']['list']))
        uris.append(data['mementos']['list'][0]['uri'])
        f.close()
        file_count+=1
    # zip lists in dataframe and store as .csv file
    df = pd.DataFrame(list(zip(uris, memento_ages, memento_counts)))
    df = df.rename(columns={"0": "uri", "1": "age", "2": "num_memento"})
    df.to_csv("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/memento_ages_counts.csv", index=False)
    # open file for writing dictionary to csv file
    #w = csv.writer(open("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/memento_ages.csv", "w"))
    # loop over dictionary keys and values
    #for key, val in mem_dict.items():
        # write every key and value to file
        #w.writerow([key, val])

def memento_age_scatterplot():
    # load data into dataframe
    df = pd.read_csv('/Users/sofiahuang/Documents/WM/FALL2022/DATA440/memento_ages_counts.csv')
    # rename columns
    df.rename(columns={"0": "uri", "1": "age", "2": "num_memento"}, inplace=True)
    plt.figure(figsize=(8, 4))
    # create scatterplot, add grid, axis labels, and save plot
    plt.scatter(df['age'], df['num_memento'], c ="lightskyblue", alpha=0.5, edgecolors='steelblue')
    plt.grid()
    plt.xlabel('Age in Days')
    plt.ylabel('Number of Mementos')
    plt.title('Age of Mementos')
    plt.savefig('/Users/sofiahuang/Documents/WM/FALL2022/DATA440/memento_age_scatter.png')

if __name__ == "__main__":
    #search_terms = ['Queen', 'hurricane', 'Ukraine', 'NASA', 'Biden']
    #for term in search_terms:
        #for i in range(25):
            #get_tweets(term)

    #final_links = get_links()

    #links = read_unique_links_file('unique_uris.txt')
    #os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440")
    #timemap_directory = os.path.join(os.getcwd(),'timemaps')
    #if not os.path.exists(timemap_directory):
        #os.mkdir(timemap_directory)
    #get_timemaps(links, timemap_directory)

    #count_mementos()
    get_memento_age()
    memento_age_scatterplot()


    