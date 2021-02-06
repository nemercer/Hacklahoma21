import pandas as pd
import re


def preprocess():
    df = pd.read_csv('data/labeled_data.csv')
    df = df.drop(df.columns[[0, 1, 2, 3, 4]], axis=1)  # Remove columns 0-4.

    # Remove various garbage from tweets.
    df['tweet'] = [re.sub(r'&.*;', '', tweet) for tweet in df['tweet']]  # Remove emojis.
    df['tweet'] = [" ".join(filter(lambda x:x[0] != '@', tweet.split())) for tweet in df['tweet']]  # Remove @.
    df['tweet'] = [" ".join(filter(lambda x:x[0] != '#', tweet.split())) for tweet in df['tweet']]  # Remove #.
    df['tweet'] = [re.sub(r'https://.*', '', tweet) for tweet in df['tweet']]  # Remove https://
    df['tweet'] = [re.sub(r'http://.*', '', tweet) for tweet in df['tweet']]  # Remove http://

    return df


if __name__ == '__main__':
    print(preprocess())
