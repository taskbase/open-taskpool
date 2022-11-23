#!/usr/bin/env python

import os
import sys
import hashlib
import pandas as pd
import numpy as np
import sqlite3
import json

DB_FILE = "../taskpool.db"


def load_similar_words_data(similar_words_path: str):
    df = pd.read_csv(similar_words_path, sep='\t')

    def remove_nans(similar_words):
        return list(filter(lambda x: isinstance(x, str), similar_words))

    result = []
    for i in range(len(df.index)):
        row = df.iloc[i]
        filtered = remove_nans(row.to_list()[1:])
        result.append([row["word"], json.dumps(filtered)])

    return pd.DataFrame(result, columns=["word", "similar_words"])


def load_exercise_data(exercise_path: str) -> pd.DataFrame:
    df = pd.read_csv(exercise_path,
                     usecols=[
                         "word",
                         "translation_id",
                         "target_sentence_id",
                         "source_sentence_id"
                     ],
                     dtype={
                         "word": 'string',
                         "translation_id": np.int64,
                         "target_sentence_id": np.int64,
                         "source_sentence_id": np.int64
                     }, sep='\t', skiprows=0)

    def generate_id(row):
        return hashlib.md5("{}_{}".format(row["source_sentence_id"], row["target_sentence_id"]).encode("utf-8")) \
            .hexdigest()

    # add id
    df['id'] = pd.Series([generate_id(df.iloc[i]) for i in range(len(df.index))], dtype='string')

    return df


def find_or_exit(path):
    if not os.path.exists(path):
        print("cannot find", path)
        exit(1)


def main():
    print("Preparing data...")
    # default path
    exercise_path = "data-import/exercise-import.tsv"
    similar_words_path = "data-import/similar-words-import.tsv"

    if len(sys.argv) >= 2:
        exercise_path = sys.argv[1]

    if len(sys.argv) >= 3:
        similar_words_path = sys.argv[2]

    find_or_exit(exercise_path)
    find_or_exit(similar_words_path)

    print("Reading exercise data from ", exercise_path)
    print("Reading similar words data from", similar_words_path)

    df1 = load_similar_words_data(similar_words_path)
    df2 = load_exercise_data(exercise_path)

    print("Merging tables together")
    df = pd.merge(df1, df2, on="word").dropna(subset=["word"])
    df = df.rename(columns={
        "word": "target_word"
    })

    with sqlite3.connect(DB_FILE) as conn:
        print("Uploading {0} values to exercise table...".format(df.shape[0]))
        df.to_sql("exercise", conn, if_exists="replace", index=False)
        print('Done')


if __name__ == "__main__":
    main()
