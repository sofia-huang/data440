import csv
import matplotlib.pyplot as plt  
import pandas as pd  
import numpy as np
import json

def plot_friends(df, filename):
    # sort df values and reset index
    df = df.sort_values('FRIENDCOUNT')
    df = df.reset_index(drop=True)
    index = np.arange(1,99)
    df['INDEX'] = index
    # add Prof. Nwala's data to the df
    df2 = {'USER': 'Alexander Nwala', 'FRIENDCOUNT': 98, 'INDEX': 'U'}
    line = pd.DataFrame(df2, index=[10])
    df2 = pd.concat([df.iloc[:10], line, df.iloc[10:]]).reset_index(drop=True)
    # plot the bar graph and fix details
    plt.figure(figsize=(36, 8))

    ax = plt.gca()
    ax.margins(x=0)

    plt.bar(df2.index, df2['FRIENDCOUNT'], width=0.6)
    plt.xticks(np.arange(len(df2['INDEX'])), df2['INDEX'],fontsize='18')
    plt.xlabel('Users', fontsize=24)
    plt.ylabel('Friend Count', fontsize=24)
    plt.title('Friendship Paradox', fontsize=30)
    # save plot to file

    plt.tight_layout()
    plt.savefig(filename)
    #plt.show()

def get_followers_followers(jsonl_file):
    f = open(jsonl_file)
    # read in all the lines
    lines = f.readlines()  
    followers_stats = {}
    # add a header entry to dictionary for the csv later
    followers_stats.update({'USER':'FRIENDCOUNT'})
    # each line is a json 
    for line in lines:
        follower_data = json.loads(line)
        # get my follower count
        num_my_followers = follower_data['meta']['result_count']
        print(num_my_followers)
        # loop through my followers and get their username + follower count
        # to add to a dictionary
        for i in range(num_my_followers):
            follower_username = follower_data['data'][i]['username']
            follower_followers =  follower_data['data'][i]['public_metrics']['followers_count']
            print('username: {} \nfollower_count: {}'.format(follower_username, follower_followers))
            followers_stats.update({follower_username:follower_followers})
    # add myself to the dictionary
    followers_stats.update({'_sofiahuang':num_my_followers})

    # open file for writing dictionary to csv file
    w = csv.writer(open("/Users/sofiahuang/Documents/WM/FALL2022/DATA440/followers_followers.csv", "w"))
    # loop over dictionary keys and values
    for key, val in followers_stats.items():
        # write every key and value to file
        w.writerow([key, val])


if __name__ == "__main__":
    df = pd.read_csv('/Users/sofiahuang/Documents/WM/FALL2022/DATA440/acnwala_friends_friends_count.csv')
    print('The mean of the number of friends that the user\'s friends have: {}'.format(np.mean(df[' "FRIENDCOUNT"'])))
    print('The median of the number of friends that the user\'s friends have: {}'.format(np.median(df[' "FRIENDCOUNT"'])))
    print('The standard deviation of the number of friends that the user\'s friends have: {}'.format(np.std(df[' "FRIENDCOUNT"'])))
    df.rename(columns={' "FRIENDCOUNT"': 'FRIENDCOUNT'}, inplace=True)
    plot_friends(df, '/Users/sofiahuang/Documents/WM/FALL2022/DATA440/friendship_paradox_barplot2.png')

    #get_followers_followers('/Users/sofiahuang/Desktop/myfollowers.jsonl')

    df_twitter = pd.read_csv('/Users/sofiahuang/Documents/WM/FALL2022/DATA440/followers_followers.csv')
    print('The mean of the number of friends that my friends have on Twitter: {}'.format(np.mean(df_twitter['FRIENDCOUNT'])))
    print('The median of the number of friends that my friends have on Twitter: {}'.format(np.median(df_twitter['FRIENDCOUNT'])))
    print('The standard deviation of the number of friends that my friends have on Twitter: {}'.format(np.std(df_twitter['FRIENDCOUNT'])))


