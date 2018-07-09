import csv
import pickle

if __name__ == '__main__':
    uncertain_verified = pickle.load(open('uncertain_verified.pickle', 'rb'))
    certain_csv = csv.reader(open('certain_tweets.csv'))

    merged_list = [r[0] for r in certain_csv] + uncertain_verified

    print('Number of tweets before removing duplicates', len(merged_list))

    merged_list = list(set(merged_list))

    print('Number of tweets after removing duplicates', len(merged_list))

    outcsv = open('../finalized_data.csv', 'w', encoding='utf-8')
    csv.writer(outcsv).writerows([t] for t in merged_list)
    pickle.dump(merged_list, open('../finalized_data.pickle', 'wb'))


    exit(0)