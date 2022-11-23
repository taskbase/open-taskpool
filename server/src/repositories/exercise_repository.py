import sqlite3
from itertools import starmap
from typing import List
from models.api_models import LearnableWord, tuple_to_learnable_word, Exercise, internal_exercise_to_exercise, \
    ExerciseType
from models.internal_models import TranslationPair, tuple_to_internal_exercise, InternalTranslationPair
from settings import settings

con = sqlite3.connect(settings.taskpool_db_path, check_same_thread=False)


async def get_exercises_by_translation_pair_and_word(base_url: str, translation_pair: InternalTranslationPair,
                                                     word: str, exerciseType: ExerciseType) -> List[Exercise]:
    cursor = con.cursor()
    results = cursor.execute("""
    SELECT 
        e.id,
        e.translation_id,
        e.target_word,
        e.similar_words,
        e.source_sentence_id,
        e.target_sentence_id,
        s1.text, 
        s1.language, 
        s2.text, 
        s2.language
    FROM exercise as e
    JOIN sentences s1 ON s1.id = e.source_sentence_id
    JOIN sentences s2 on s2.id = e.target_sentence_id
    WHERE s1.language = :lang1 AND s2.language = :lang2 AND e.target_word = :word
    """, {
        "lang1": translation_pair.source_language.name.upper(),
        "lang2": translation_pair.target_language.name.upper(),
        "word": word
    }).fetchall()
    cursor.close()
    internal_exercises = list(map(tuple_to_internal_exercise, results))
    return list(starmap(internal_exercise_to_exercise, map(lambda e: [e, exerciseType, base_url], internal_exercises)))


async def get_learnable_words(translation_pair: InternalTranslationPair) -> List[LearnableWord]:
    cursor = con.cursor()
    results = cursor.execute("""
        SELECT DISTINCT exercise.target_word
        FROM exercise
        JOIN sentences s1 ON s1.id = exercise.source_sentence_id
        JOIN sentences s2 on s2.id = exercise.target_sentence_id
        WHERE s1.language = :lang1 AND s2.language = :lang2
        """, {
        "lang1": translation_pair.source_language.name.upper(),
        "lang2": translation_pair.target_language.name.upper()
    }).fetchall()
    cursor.close()
    return list(map(tuple_to_learnable_word, results))
