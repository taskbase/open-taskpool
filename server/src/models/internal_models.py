from enum import Enum
from typing import List
import json


class TranslationPair(str, Enum):
    UK_DE = "uk->de"
    DE_EN = "de->en"


class Language(str, Enum):
    uk = "uk"
    de = "de"
    en = "en"


class InternalTranslationPair:
    def __init__(self, source_language: Language, target_language: Language):
        self.source_language = source_language
        self.target_language = target_language


class InternalExercise:
    def __init__(self, id: str, translation_id: int, target_word: str, similar_words: List[str],
                 source_sentence_id: int,
                 source_sentence_text: str,
                 source_sentence_language: Language,
                 target_sentence_id: int,
                 target_sentence_text: str,
                 target_sentence_language: Language):
        self.id = id
        self.translation_id = translation_id
        self.target_word = target_word
        self.similar_words = similar_words
        self.source_sentence_id = source_sentence_id
        self.target_sentence_id = target_sentence_id
        self.source_sentence_text = source_sentence_text
        self.source_sentence_language = source_sentence_language
        self.target_sentence_text = target_sentence_text
        self.target_sentence_language = target_sentence_language


def tuple_to_internal_exercise(row: tuple) -> InternalExercise:
    return InternalExercise(
        id=row[0],
        translation_id=row[1],
        target_word=row[2],
        similar_words=json.loads(row[3]),
        source_sentence_id=row[4],
        target_sentence_id=row[5],
        source_sentence_text=row[6],
        source_sentence_language=row[7].lower(),
        target_sentence_text=row[8],
        target_sentence_language=row[9].lower()
    )
