# Jackson Blackman
# 251344173
# Jblackm8
# 2023-11-15
# This file takes an input, analyzes it, and gives an output of the given analysis

# Import the sentiment_analysis module
from sentiment_analysis import *


def main():
    # Main function takes the users input and inputs them into the functions in order to create their report
    tsv = False
    csv = False
    txt = False

    # takes in the tsv file and checks if it ends in .tsv
    tsv_file = str(input("Input keyword filename (.tsv file): "))
    if tsv_file.endswith('.tsv'):
        tsv = True
    if tsv is False:
        raise Exception('Must have a tsv file extension')

    # takes in the csv file and checks if it ends in .csv
    csv_file = str(input("Input tweet filename (.csv file): "))
    if csv_file.endswith('.csv'):
        csv = True
    if csv is False:
        raise Exception('Must have a csv file extension')
    # takes in the txt file and checks if it ends in .txt
    txt_file = str(input("Input filename to output report in (.txt file): "))
    if txt_file.endswith('.txt'):
        txt = True
    if txt is False:
        raise Exception('Must have a txt file extension')

    # Compiles the report and prints it to the output file
    keyword_dict = read_keywords(tsv_file)
    tweet_dict = read_tweets(csv_file)
    if len(tweet_dict) == 0 or len(keyword_dict) == 0:
        raise Exception('Tweet list or keyword dictionary is empty!')
    report = make_report(tweet_dict, keyword_dict)
    output_file = txt_file
    write_report(report, output_file)
    print("Wrote report to " + txt_file + '')


main()
