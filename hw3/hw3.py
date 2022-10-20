import requests
import os
import codecs
import hashlib 
from boilerpy3 import extractors
from shutil import copyfile
from io import StringIO 
import sys
import subprocess


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

def extract_text(uri_list, raw_directory, processed_directory):
    link_index = 1
    num_processed = 0
    extractor = extractors.ArticleExtractor()
    for uri in uri_list:
        if link_index == 1000: break
        try:
            # hash URI to create filename
            filename = hashlib.md5(uri.encode('utf-8')).hexdigest()
            if os.path.exists(os.path.join(processed_directory, filename)):
            # file has already been created, go to the next uri
                print('file already exists, skipping uri')
                link_index += 1
                continue
            # request URI
            resp = requests.get(uri, timeout=5)
            raw_html = resp.text
            # pass HTML to Extractor
            content = extractor.get_content(resp.text)
            # check if any text was obtained, if not, skip
            if (content == ''): 
                print('nothing extracted from: ' + uri)
                link_index += 1
                continue
            else:
                print('content from: ' + uri)
            # open txt file and write raw text content to it
            raw_html_file = codecs.open(os.path.join(raw_directory, str(filename)), "w", encoding='utf8')
            raw_html_file.write(uri + "\r\n")
            raw_html_file.write(raw_html)
            raw_html_file.close()
            # open txt file and write processed text content to it
            text_content_file = codecs.open(os.path.join(processed_directory, str(filename)), "w", encoding='utf8')
            text_content_file.write(uri + "\r\n")
            text_content_file.write(content)
            text_content_file.close()
            # keep track of how many URI text content obtained
            num_processed+=1
            link_index+=1
        except Exception as e:
            print('error requesting URI or extracting content, skipping to next.')
            print(e)
            link_index += 1
            continue
    print('{} URIs stripped.'.format(num_processed))

def count_query_term(directory):
    num_docs_w_term = 0
    # list of all files with stripped text content
    html_list = os.listdir(directory)
    os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440")
    # creating new folder for documents with query terms
    query_directory = os.path.join(os.getcwd(),'query')
    if not os.path.exists(query_directory):
        os.mkdir(query_directory)
    # loop through stripped text content files and 
    # see how many of the query term are in each
    for doc in html_list:
        os.chdir(directory)
        output = os.popen('cat ' + doc + ' | grep -c Ukraine').read()
        # count the number of docs that have the query term
        if int(output) > 0: num_docs_w_term += 1
        # if there is more than 15 instances, copy file to folder created earlier
        if int(output) >= 15:
            f = open(doc, 'r')
            uri = f. readline()
            num_words = len(f.read().split())
            print('Term occurence: {} - Word count: {} - URI: {}'.format(str(output),num_words,uri))
            copyfile(os.path.join(directory,doc), os.path.join(query_directory,doc))
    print('Number of documents with query term: {}'.format(num_docs_w_term))



if __name__ == "__main__":

    links = read_unique_links_file('unique_uris.txt')
    os.chdir("/Users/sofiahuang/Documents/WM/FALL2022/DATA440")
    processed_directory = os.path.join(os.getcwd(),'processed_text_content')
    if not os.path.exists(processed_directory):
        os.mkdir(processed_directory)
    raw_directory = os.path.join(os.getcwd(),'raw_html_content')
    if not os.path.exists(raw_directory):
        os.mkdir(raw_directory)
    extract_text(links, raw_directory, processed_directory)
    #count_query_term("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/text_content")
