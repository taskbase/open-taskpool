import random
import re
from enum import Enum
from typing import List, Optional, Callable, Dict
from pydantic import BaseModel, Field
from models.internal_models import TranslationPair, InternalExercise, InternalTranslationPair, Language


class HealthStatus(BaseModel):
    healthy: bool
    status: str


def translation_pair_to_internal_translation_pair(pair: TranslationPair) -> InternalTranslationPair:
    match pair:
        case TranslationPair.UK_DE:
            return InternalTranslationPair(Language.uk, Language.de)
    raise Exception("Non exhaustive match statement")


class TranslationPairWrapper(BaseModel):
    translationPair: TranslationPair = Field(
        description='The left side is the source language and the right side the target language to be learned. For '
                    'example the pair "uk->de" should be used for learning German for Ukrainians.')


class LearnableWord(BaseModel):
    word: str


def tuple_to_learnable_word(row: tuple) -> LearnableWord:
    return LearnableWord(
        word=row[0]
    )


class ExerciseType(str, Enum):
    BITMARK_ESSAY = "bitmark.essay",
    BITMARK_CLOZE = "bitmark.cloze",
    BITMARK_MULTIPLE_CHOICE_TEXT = "bitmark.multiple-choice-text",
    ALL = "all"


class SourceSentence(BaseModel):
    text: str


class TargetSentence(BaseModel):
    word: str
    similar_words: List[str] = Field(alias="similarWords")
    text: str


class Meta(BaseModel):
    language: Optional[Language] = Field(
        default="uk",
        description="This is the language a Bit is written in - i.e. the source language.")
    learningLanguage: Optional[Language] = Field(
        default="de",
        description="For language learning material, this is the language to be learned/taught."
    )
    subject: str = Field(
        description="Title of the exercise."
    )


class FeedbackEngine(BaseModel):
    feedbackId: str = Field(
        description='Identifier needed for the <a href="https://bitmark-api.taskbase.com/documentation">fedback '
                    'engine</a> to group together inputs for the same quizz.')
    userId: str = Field(
        default="",
        description='Anonymous and unique identifier for the <a '
                    'href="https://bitmark-api.taskbase.com/documentation">fedback engine</a>. Make sure to overwrite '
                    'this field. For a complete and accurate student model, make sure to provide the same anonymous '
                    'and unique identifier for each student. Can be for example the hash of the user e-mail.')
    timeOnTask: int = Field(
        default=0,
        description="The time in seconds it took the user to answer the bit. While this field is not mandatory, "
                    "it may eventually impact the performance of bit recommendations for the student. Hence, "
                    "it is recommended to track and set this field.")


class Answer(BaseModel):
    text: str = Field(default="", description="Answer of the student")


class Audio(BaseModel):
    format: str = "mp3"
    src: str = Field(description="A URL pointing to the audio for the target sentence.")


class Resource(BaseModel):
    type: str = "audio"
    audio: Audio


class EssayBit(BaseModel):
    format: str = Field(description='The format of this bit. The API supports only <code>"text"</code>')
    meta: Optional[Meta] = Field(description="Object holding meta information about the bit.")
    feedbackEngine: FeedbackEngine = Field(description="Object holding data necessary for the feedback engine.")
    instruction: str = Field(description="The exercise instruction that should be presented to the learner.")
    type: str = "essay"
    sampleSolution: str = Field(description="The sample solution - i.e. the sentence in the target language.")
    answer: Answer = Field(description="The object holding the learners input. Needed for the feedback engine.")
    resource: Resource = Field(description="The object holding information about the audio file.")


class ClozeBitType(str, Enum):
    GAP = "gap"
    TEXT = "text"


class ClozeBitBodyElement(BaseModel):
    type: ClozeBitType


class ClozeBitBodyElementGap(ClozeBitBodyElement):
    type: ClozeBitType = ClozeBitType.GAP
    solutions: List[str]
    answer: Answer = Field(description="The object holding the learners input. Needed for the feedback engine.")


class ClozeBitBodyElementText(ClozeBitBodyElement):
    type: ClozeBitType = ClozeBitType.TEXT
    text: str


class ClozeBit(BaseModel):
    format: str = Field(example="text", description='The format of this bit. The API supports only <code>"text"</code>')
    meta: Optional[Meta] = Field(description="Object holding meta information about the bit.")
    feedbackEngine: FeedbackEngine = Field(description="Object holding data necessary for the feedback engine.")
    instruction: str = Field(description="The exercise instruction that should be presented to the learner.")
    type: str = "cloze"
    body: List[ClozeBitBodyElementGap | ClozeBitBodyElementText] = Field(
        example=[
            ClozeBitBodyElementText(text="Tim lives in a big"),
            ClozeBitBodyElementGap(solutions=["house"], answer=Answer())
        ],
        title="ClozeBitBodyElement",
        description='The main object of the <code>"cloze"</code> bit type.')


class MultipleChoiceTextBodyElement(BaseModel):
    type: str


class MultipleChoiceTextChoice(BaseModel):
    choice: str = Field(description="The actual choice to present to the learner.")
    isCorrect: bool = Field(title="isCorrect", description="Signals if this is the correct choice.")
    isSelected: bool = Field(
        title="isSelected",
        description='Signals if this is the selected choice by the learner. The API will always '
                    'return false for all choices. The student interaction should switch one '
                    'choice to <code>true</code>.')


class MultipleChoiceTextBodyElementChoices(MultipleChoiceTextBodyElement):
    type: str = "choices"
    choices: List[MultipleChoiceTextChoice]


class MultipleChoiceTextBodyElementText(MultipleChoiceTextBodyElement):
    type: str = "text"
    text: str


class MultipleChoiceTextBit(BaseModel):
    format: str = Field(description='The format of this bit. The API supports only <code>"text"</code>')
    meta: Optional[Meta] = Field(description="Object holding meta information about the bit.")
    feedbackEngine: FeedbackEngine = Field(description="Object holding data necessary for the feedback engine.")
    instruction: str = Field(description="The exercise instruction that should be presented to the learner.")
    type: str = "multiple-choice-text"
    body: List[MultipleChoiceTextBodyElementChoices | MultipleChoiceTextBodyElementText] = Field(
        title="MultipleChoiceTextBodyElement",
        description='The main object of the <code>"multiple-choice-text"</code> bit.')


class BitMark(BaseModel):
    essay: Optional[EssayBit] = Field(description='Object holding the <code>"essay"</code> bit.')
    cloze: Optional[ClozeBit] = Field(description='Object holding the <code>"cloze"</code> bit.')
    multipleChoiceText: Optional[MultipleChoiceTextBit] = Field(
        description='Object holding the <code>"multipleChoiceText"</code> bit.')


class Exercise(BaseModel):
    sourceSentence: SourceSentence = Field(description="Object holding data about the source sentence.")
    targetSentence: TargetSentence = Field(description="Object holding data about the target sentence.")
    bitmark: BitMark = Field(description="The object holding the bitmark quizzes.")


def create_instruction(exerciseType: ExerciseType, source_sentence_text: str) -> str:
    if exerciseType == ExerciseType.ALL:
        raise ValueError("ExerciseType.ALL is not a valid type to create an instruction. Use a specific type when "
                         "calling this method.")

    # If multiple instruction languages are required nest the languages per ExerciseType (need exercise language)
    instruction_map: Dict[ExerciseType, str] = {
        ExerciseType.BITMARK_ESSAY: "Перекладіть речення: \"{}\"",
        ExerciseType.BITMARK_CLOZE: "Дано: \"{}\", запишіть пропущене слово",
        ExerciseType.BITMARK_MULTIPLE_CHOICE_TEXT: "Дано: \"{}\", виберіть пропущене слово",
    }
    return instruction_map[exerciseType].format(source_sentence_text)


def create_bitmark_essay(exercise: InternalExercise, exerciseType: ExerciseType, base_url: str) -> Optional[EssayBit]:
    if not (exerciseType == ExerciseType.BITMARK_ESSAY or exerciseType == ExerciseType.ALL):
        return None
    return EssayBit(
        format="text",
        meta=Meta(
            language=exercise.source_sentence_language,
            learningLanguage=exercise.target_sentence_language,
            subject=exercise.target_word
        ),
        feedbackEngine=FeedbackEngine(
            feedbackId=exercise.id + "-essay"
        ),
        instruction=create_instruction(
            exerciseType=ExerciseType.BITMARK_ESSAY,
            source_sentence_text=exercise.source_sentence_text
        ),
        type="essay",
        sampleSolution=exercise.target_sentence_text,
        answer={
            "text": ""
        },
        resource=Resource(
            audio=Audio(
                src="{}{}{}-{}.mp3".format(base_url, "audio/", exercise.target_sentence_language.upper(),
                                           exercise.target_sentence_id)
            )
        )
    )


def get_parts(exercise: InternalExercise) -> List[str]:
    # split only if target word is not inside a word
    # target word = "target", sentence="targeting the target?" -> "targeting the ", "target", "?"
    return re.split(r'(?:^|)({})(|$|[,.;:"\'%?!])'.format(exercise.target_word), exercise.target_sentence_text)


def build_body(
        parts: List[str],
        target_word: str,
        text_builder: Callable[[str], any],
        gap_builder: Callable[[str], any]
) -> List[any]:
    gaps = []

    for part in parts:
        if part.strip() == '':
            continue
        elif part == target_word:
            gaps.append(gap_builder(part))
        else:
            gaps.append(text_builder(part))

    return gaps


def create_bitmark_cloze(exercise: InternalExercise, exerciseType: ExerciseType):
    if not (exerciseType == ExerciseType.BITMARK_CLOZE or exerciseType == ExerciseType.ALL):
        return None

    gaps = build_body(
        parts=get_parts(exercise),
        target_word=exercise.target_word,
        text_builder=lambda x: ClozeBitBodyElementText(text=x),
        gap_builder=lambda x: ClozeBitBodyElementGap(solutions=[x], answer=Answer())
    )

    return ClozeBit(
        format="text",
        meta=Meta(
            language=exercise.source_sentence_language,
            learningLanguage=exercise.target_sentence_language,
            subject=exercise.target_word
        ),
        feedbackEngine=FeedbackEngine(
            feedbackId=exercise.id + "-cloze"
        ),
        instruction=create_instruction(
            exerciseType=ExerciseType.BITMARK_CLOZE,
            source_sentence_text=exercise.source_sentence_text
        ),
        type="cloze",
        body=gaps
    )


def create_bitmark_multiple_choice(
        exercise: InternalExercise,
        exerciseType: ExerciseType
) -> Optional[MultipleChoiceTextBit]:
    if not (exerciseType == ExerciseType.BITMARK_MULTIPLE_CHOICE_TEXT or exerciseType == ExerciseType.ALL):
        return None

    choices = []
    for word in exercise.similar_words:
        choices.append(
            MultipleChoiceTextChoice(
                choice=word,
                isCorrect=False,
                isSelected=False
            )
        )
    choices.append(
        MultipleChoiceTextChoice(
            choice=exercise.target_word,
            isCorrect=True,
            isSelected=False
        )
    )
    random.shuffle(choices)

    gaps = build_body(
        parts=get_parts(exercise),
        target_word=exercise.target_word,
        text_builder=lambda x: MultipleChoiceTextBodyElementText(text=x),
        gap_builder=lambda x: MultipleChoiceTextBodyElementChoices(choices=choices)
    )

    return MultipleChoiceTextBit(
        format="text",
        meta=Meta(
            language=exercise.source_sentence_language,
            learningLanguage=exercise.target_sentence_language,
            subject=exercise.target_word
        ),
        feedbackEngine=FeedbackEngine(
            feedbackId=exercise.id + "-multiple-choice-text"
        ),
        instruction=create_instruction(
            exerciseType=ExerciseType.BITMARK_MULTIPLE_CHOICE_TEXT,
            source_sentence_text=exercise.source_sentence_text
        ),
        type="multiple-choice-text",
        body=gaps
    )


def internal_exercise_to_exercise(exercise: InternalExercise, exerciseType: ExerciseType, base_url: str) -> Exercise:
    return Exercise(
        sourceSentence=SourceSentence(
            text=exercise.source_sentence_text
        ),
        targetSentence=TargetSentence(
            word=exercise.target_word,
            similarWords=exercise.similar_words,
            text=exercise.target_sentence_text
        ),
        bitmark=BitMark(
            essay=create_bitmark_essay(exercise=exercise, exerciseType=exerciseType, base_url=base_url),
            cloze=create_bitmark_cloze(exercise=exercise, exerciseType=exerciseType),
            multipleChoiceText=create_bitmark_multiple_choice(exercise=exercise, exerciseType=exerciseType)
        )
    )
