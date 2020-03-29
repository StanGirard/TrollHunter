import re
import pandas as pd

def cleantext(text):
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^RT|http.+?", "", text).split())


def convert_elk_export_to_process_export(csvFileNames):
    if not isinstance(csvFileNames, list):
        csvFileNames = [csvFileNames]

    tab = [{'user': pd.read_csv(fileName), "fileName": fileName} for fileName in csvFileNames]

    for entry in tab:
        user = entry['user']
        fileName = entry['fileName']

        fields = pd.DataFrame(user[
            ['_source.user_id_str', '_source.tweet', '_source.mentions', '_source.datetime', '_source.datestamp',
             '_source.timestamp']])

        fields.rename(columns={'_source.user_id_str': 'user_id', '_source.tweet': 'text',
                               '_source.mentions': 'mentions', '_source.datetime': 'created_at'}, inplace=True)

        fields['created_at'] = fields['created_at'].apply(lambda x: int(x) * 1000)
        fields['created_str'] = fields['_source.datestamp'] + " " + fields['_source.timestamp']
        fields['user_id'] = fields['user_id'].apply(int)

        fields.drop(['_source.datestamp', '_source.timestamp'], axis=1)

        fields.insert(1, "retweet_count", 0.0)
        fields.insert(2, "retweeted", 0.0)
        fields.insert(3, "favorite_count", 0.0)

        fields.insert(5, "hashtags", "")

        res = fields[['user_id', 'retweet_count', 'retweeted', 'favorite_count', 'text',
                      'hashtags', 'mentions', 'created_at', 'created_str']]

        resFile = fileName + '.out'
        print(resFile)

        res = res.sort_values(by="created_at", ascending=True)
        res.to_csv(resFile, index=False)


if __name__ == '__main__':
    convert_elk_export_to_process_export("./user_813286.csv")