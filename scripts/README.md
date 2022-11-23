# How to generate exercises

1. First you'll have to download the Tatoeba dataset. Run
   ```shell
   ./download-data.sh
   ```
   You will find the data under `data-tatoeba/` inside this folder. 
   
2. Download [any required sentence pairs](https://tatoeba.org/en/downloads) you are interested in and place it in `data-tatoeba/`.\
   As this sentence pairs are always created on the fly, this step has to happen manually.\
   Sentence pair data should be named `sentences_{SRC_LANG}_{TGT_LANG}.tsv`, where `SRC_LANG` and `TGT_LANG` are lowercased two-letter language codes.
   For example `sentences_uk_de.tsv`.

3. Run the `./generate_data.ipynb` notebook to process raw data into TSVs. Change input variables as needed.

4. Run the `./import_sql.ipynb` notebook to import the generated CSVs into a local SQLite database.

5. Run the `./generate_exercise_precursors.ipynb` notebook to generate exercise precursors.

6. Run the `./similar_words.ipynb` notebook to generate similar words.

7. Optionally run the `./generate_sentence_audio` notebook to generate audio files.

8. Optionally do a manual quality control check over the generated data.

9. To populate the exercise table which is the main entity in the API server, run
   ```shell
   python3 populate_exercise_table.py
   ```
   The script expects the following two files to exist (they have to be moved to that folder manually): 
   1. `data-import/exercise-import.tsv`: which is the output of the `./generate_exercise_precursors.ipynb` notebook 
   2. `data-import/similar-words-import.tsv`: which is the output of the `./similar_words.ipynb` notebook

After all those above steps. You should have a ready-to-use `tasbkpool.db` SQLite DB in the parent folder which
will be used by the API server.
