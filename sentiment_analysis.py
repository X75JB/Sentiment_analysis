# Jackson Blackman
# 251344173
# Jblackm8
# 2023-11-15
# This file is a small modal of functions that will be utilized within the main file

import csv


def read_keywords(keyword_file_name):
    # This function will take a file name input and create a dictionary of words and scores to use in other functions
    keyword_dict = {}
    try:
        with open(keyword_file_name, 'r') as keywords:
            for line in keywords:
                # split the lines into word and score
                word, score = line.strip().split('\t')
                # convert the score from str -> int
                score = int(score)
                # apply to the new dictionary
                keyword_dict[word] = score
    except IOError:
        print('Could not open file ' + keyword_file_name + '!')
    return keyword_dict


def clean_tweet_text(tweet_text):
    # This will take a string and remove all but english letters and spaces while making it all lower case
    allowed = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x',
               'c', 'v', 'b', 'n', 'm', ' ']
    final = ''
    for letter in tweet_text.lower():
        if letter in allowed:
            final = final + letter
        else:
            continue
    return final


def calc_sentiment(tweet_text, keyword_dict):
    # This will calculate the sentiment score of a tweet based off of inputted text and the keyword dictionary
    total_sentiment_score = 0

    word_list = tweet_text.split()
    for word in word_list:
        if word in keyword_dict:
            total_sentiment_score += keyword_dict[word]
        else:
            continue
    return total_sentiment_score


def classify(score):
    # This function will simply take a score and assign it a positive, negative, or neutral based off of the score
    if score < 0:
        return 'negative'
    elif score > 0:
        return 'positive'
    else:
        return 'neutral'


def read_tweets(tweet_file_name):
    # This will take a file of tweets and will create a list with a dictionary for each tweet
    tweets_dict_list = []

    try:
        with open(tweet_file_name, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                tweets_dict_list.append({
                    'date': row[0],
                    'text': clean_tweet_text(row[1]),
                    'user': row[2],
                    'retweet': int(row[3]),
                    'favorite': int(row[4]),
                    'lang': row[5],
                    'country': row[6],
                    'state': row[7],
                    'city': row[8],
                    'lat': float(row[9]) if row[9] != 'NULL' else 'NULL',
                    'lon': float(row[10]) if row[10] != 'NULL' else 'NULL'

                })
    except IOError:
        print('Could not open file ' + tweet_file_name + '!')

    return tweets_dict_list


def make_report(tweet_list, keyword_dict):
    # This file will take the list of tweet dictionaries and the keyword dictionary and compile the information
    # needed for the report


    total_tweets = 0
    average_sentiment_unedited = 0
    positive_sentiments = 0
    neutral_sentiments = 0
    negative_sentiments = 0
    favourite_tweets = 0
    average_sentiment_fav_unedited = 0
    retweeted_tweets = 0
    average_sentiment_retweet_unedited = 0
    country_sentiment = {}
    country_tweet_count = {}

    for tweet in tweet_list:
        # Adds to total amount of tweets total
        total_tweets += 1
        # Adds to positive tweets
        if classify(calc_sentiment(tweet['text'], keyword_dict)) == 'positive':
            average_sentiment_unedited += calc_sentiment(tweet['text'], keyword_dict)
            positive_sentiments += 1
        # Adds to negative tweets total
        elif classify(calc_sentiment(tweet['text'], keyword_dict)) == 'negative':
            average_sentiment_unedited += calc_sentiment(tweet['text'], keyword_dict)
            negative_sentiments += 1
        # Adds to neutral tweets total
        else:
            average_sentiment_unedited += calc_sentiment(tweet['text'], keyword_dict)
            neutral_sentiments += 1

    for tweet in tweet_list:
        if tweet['favorite'] >= 1:
            # Adds to total favourite tweets
            favourite_tweets += 1
            # Adds to the total sentiment score of favourite tweets
            average_sentiment_fav_unedited += calc_sentiment(tweet['text'], keyword_dict)

    for tweet in tweet_list:
        if tweet['retweet'] >= 1:
            # Adds to total retweeted tweets
            retweeted_tweets += 1
            # Adds to the total sentiment score of retweeted tweets
            average_sentiment_retweet_unedited += calc_sentiment(tweet['text'], keyword_dict)

    for tweet in tweet_list:
        if tweet['country'] not in country_sentiment:
            country_sentiment[tweet['country']] = 0
            country_tweet_count[tweet['country']] = 0
        country_sentiment[tweet['country']] += calc_sentiment(tweet['text'], keyword_dict)
        country_tweet_count[tweet['country']] += 1

    # Calculates the avg sentiment with the total sentiment and total tweets
    try:
        average_sentiment = average_sentiment_unedited / total_tweets
    except:
        average_sentiment = 'NAN'
    # Calculates the avg sentiment for favourite tweets with the total sentiment for favourite tweets and total
    # favourite tweets
    try:
        average_sentiment_fav = average_sentiment_fav_unedited / favourite_tweets
    except:
        average_sentiment_fav = 'NAN'
    # Calculates the avg sentiment for retweeted tweets with the total sentiment for retweeted tweets and total
    # retweeted tweets
    try:
        average_sentiment_retweet = average_sentiment_retweet_unedited / retweeted_tweets
    except:
        average_sentiment_retweet = 'NAN'
    # Calculates the avg sentiment for each country with the total sentiment for the given country tweets and total
    # tweets in that country
    try:
        average_sentiment_country = {country: country_sentiment[country] / country_tweet_count[country] for country in
                                     country_sentiment}
    except:
        average_sentiment_country = 'NAN'

    # Sorts all the countries in order to get the top 5 countries
    if 'NULL' in average_sentiment_country:
        del average_sentiment_country['NULL']

    top_5 = sorted(average_sentiment_country, key=average_sentiment_country.get, reverse=True)[:5]
    top_five = ''
    for country in top_5:
        if top_five != '':
            top_five += ', '
        top_five += country

    # Compiles the report data
    report_dict = {
        'avg_sentiment': round(average_sentiment, 2),
        'num_tweets': total_tweets,
        'num_positive': positive_sentiments,
        'num_negative': negative_sentiments,
        'num_neutral': neutral_sentiments,
        'num_favorite': favourite_tweets,
        'avg_favorite': round(average_sentiment_fav, 2),
        'num_retweet': retweeted_tweets,
        'avg_retweet': round(average_sentiment_retweet, 2),
        'top_five': top_five
    }

    return report_dict


def write_report(report, output_file):
    # This simply prints all the report information into a chosen output file
    with open(output_file, 'w') as file:
        print('Average sentiment of all tweets:', report['avg_sentiment'], file=file)
        print('Total number of tweets:', report['num_tweets'], file=file)
        print('Number of positive tweets:', report['num_positive'], file=file)
        print('Number of negative tweets:', report['num_negative'], file=file)
        print('Number of neutral tweets:', report['num_neutral'], file=file)
        print('Number of favorited tweets:', report['num_favorite'], file=file)
        print('Average sentiment of favorited tweets:', report['avg_favorite'], file=file)
        print('Number of retweeted tweets:', report['num_retweet'], file=file)
        print('Average sentiment of retweeted tweets:', report['avg_retweet'], file=file)
        print('Top five countries by average sentiment:', report['top_five'], file=file)
