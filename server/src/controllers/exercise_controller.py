from fastapi import APIRouter, Query, Request
from repositories.exercise_repository import get_exercises_by_translation_pair_and_word, get_learnable_words
from models.api_models import TranslationPair, LearnableWord, TranslationPairWrapper, Exercise, \
    translation_pair_to_internal_translation_pair, ExerciseType
from typing import List

router = APIRouter()

translation_pair_query_doc = 'The left side is the source language and the right side the target language to be ' \
                             'learned. For example the pair <code>"uk->de"</code> should be used for learning German ' \
                             'for Ukrainians. '


@router.get(
    "/translation-pairs",
    tags=["Exercise"],
    summary="Get translation pairs",
    description="""This endpoint exposes a list of translation pairs which are supported by this API. A translation 
    pair consists of a source and a target language for which this API has exercises.""",
    response_description="List of translationPairs",
    response_model=List[TranslationPairWrapper]
)
async def translation_pairs() -> List[TranslationPairWrapper]:
    return [
        TranslationPairWrapper(translationPair=TranslationPair.UK_DE)
    ]


@router.get(
    "/exercises",
    tags=["Exercise"],
    summary="Get a list of exercises",
    response_model=List[Exercise]
)
async def exercises(
        request: Request,
        word: str = Query(
            description='The target word for which to return exercises. The word is expected to be in '
                        'the target language to be learned.'),
        translationPair: TranslationPair = Query(
            description=translation_pair_query_doc),
        exerciseType: ExerciseType = Query(
            ExerciseType.BITMARK_ESSAY,
            description='Specifies what type of exercise should be returned.'
        ),
) -> List[Exercise]:
    base_url = request.base_url
    result = await get_exercises_by_translation_pair_and_word(base_url,
        translation_pair_to_internal_translation_pair(translationPair), word, exerciseType)
    return list(result)


@router.get(
    "/words",
    tags=["Exercise"],
    summary="Get a list of learnable words",
    response_model=List[LearnableWord]
)
async def words(translationPair: TranslationPair = Query(
    description=translation_pair_query_doc)
) -> List[LearnableWord]:
    return await get_learnable_words(translation_pair_to_internal_translation_pair(translationPair))
