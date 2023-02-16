from fastapi.testclient import TestClient
from . import client, app

# expected common data
sentence_to_translate = "дуже сильний дощ."
essay_instruction = f"Перекладіть речення: \"{sentence_to_translate}\""
cloze_instruction = f"Дано: \"{sentence_to_translate}\", запишіть пропущене слово"
multiple_choice_instruction = f"Дано: \"{sentence_to_translate}\", виберіть пропущене слово"
sample_solution = "Es regnet sehr stark."
answer = {
    "text": ""
}
target_word = "stark"
target_sentence = {
    "word": target_word,
    "similarWords": [
        "scharf",
        "krank",
        "hart"
    ],
    "text": sample_solution
}
format = "text"
meta = {
    "language": "uk",
    "learningLanguage": "de",
    "subject": target_word
}


def feedback_engine(exercise_type: str):
    return {
        "feedbackId": "feedback-id-" + exercise_type,
        "userId": "",
        "timeOnTask": 0
    }


def test_translation_pairs(client: TestClient):
    response = client.get("/translation-pairs")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {
            "translationPair": "uk->de"
        },
        {
            "translationPair": "de->en"
        }
    ]


def test_words_missing_pairs(client: TestClient):
    response = client.get("/words/")
    assert response.status_code == 422


def test_words_present(client: TestClient):
    response = client.get("/words?translationPair=uk->de")
    assert response.status_code == 200
    assert response.json() == [
        {
            "word": target_word
        }
    ]


def test_contains_correct_exercise_type(client: TestClient):
    response_all = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType=all")
    response_essay = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType=bitmark.essay")
    response_cloze = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType=bitmark.cloze")
    response_multiple_choice_text = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType"
                                               f"=bitmark.multiple-choice-text")

    assert response_all.status_code == 200
    assert response_essay.status_code == 200
    assert response_cloze.status_code == 200
    assert response_multiple_choice_text.status_code == 200

    # test common data
    for response in [response_all, response_essay, response_cloze, response_multiple_choice_text]:
        assert len(response.json()) == 1
        response_json = response.json()[0]
        assert response_json["targetSentence"] == target_sentence

    # test data contained is only what we expect
    response_all_bitmark = response_all.json()[0]["bitmark"]
    assert response_all_bitmark["essay"] is not None
    assert response_all_bitmark["cloze"] is not None
    assert response_all_bitmark["multipleChoiceText"] is not None

    # essay
    response_essay_bitmark = response_essay.json()[0]["bitmark"]
    assert response_essay_bitmark["essay"] is not None
    assert response_essay_bitmark["essay"]["instruction"] == essay_instruction
    assert response_essay_bitmark["cloze"] is None
    assert response_essay_bitmark["multipleChoiceText"] is None

    # cloze
    response_cloze_bitmark = response_cloze.json()[0]["bitmark"]
    assert response_cloze_bitmark["essay"] is None
    assert response_cloze_bitmark["cloze"] is not None
    assert response_cloze_bitmark["cloze"]["instruction"] == cloze_instruction
    assert response_cloze_bitmark["multipleChoiceText"] is None

    # multiple-choice
    response_multiple_choice_text_bitmark = response_multiple_choice_text.json()[0]["bitmark"]
    assert response_multiple_choice_text_bitmark["essay"] is None
    assert response_multiple_choice_text_bitmark["cloze"] is None
    assert response_multiple_choice_text_bitmark["multipleChoiceText"] is not None
    assert response_multiple_choice_text_bitmark["multipleChoiceText"]["instruction"] == multiple_choice_instruction


def test_exercises_bitmark_content(client: TestClient):
    response_all = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType=all")
    response_essay = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType=bitmark.essay")
    response_cloze = client.get(f"/exercises?translationPair=uk->de&word={target_word}&exerciseType=bitmark.cloze")
    response_multiple_choice_text = client.get("/exercises?translationPair=uk->de&word="
                                               f"{target_word}&exerciseType=bitmark.multiple-choice-text")

    # test essay
    all_json = response_all.json()[0]
    essay_json = response_essay.json()[0]
    assert all_json["bitmark"]["essay"] == essay_json["bitmark"]["essay"]
    essay = all_json["bitmark"]["essay"]
    assert essay["format"] == format
    assert essay["meta"] == meta
    assert essay["feedbackEngine"] == feedback_engine(essay["type"])
    assert essay["instruction"] == essay_instruction
    assert essay["type"] == "essay"
    assert essay["sampleSolution"] == sample_solution
    assert essay["answer"] == answer
    assert essay["resource"] == {
        "type": "audio",
        "audio": {
            "format": "mp3",
            "src": "http://testserver/audio/DE-2.mp3"
        }
    }

    # test cloze
    cloze_json = response_cloze.json()[0]
    assert all_json["bitmark"]["cloze"] == cloze_json["bitmark"]["cloze"]
    cloze = all_json["bitmark"]["cloze"]
    assert cloze["format"] == format
    assert cloze["meta"] == meta
    assert cloze["feedbackEngine"] == feedback_engine(cloze["type"])
    assert cloze["instruction"] == cloze_instruction
    assert cloze["type"] == "cloze"
    assert cloze["body"] == [
        {
            "type": "text",
            "text": "Es regnet sehr "
        },
        {
            "type": "gap",
            "solutions": [
                target_word
            ],
            "answer": {
                "text": ""
            }
        },
        {
            "type": "text",
            "text": "."
        }
    ]

    # test cloze
    multiple_choice_text_json = response_multiple_choice_text.json()[0]
    # sort choices for comparison
    all_json["bitmark"]["multipleChoiceText"]["body"][1]["choices"] = \
        sorted(all_json["bitmark"]["multipleChoiceText"]["body"][1]["choices"],
               key=lambda t: t["choice"])
    multiple_choice_text_json["bitmark"]["multipleChoiceText"]["body"][1]["choices"] = \
        sorted(multiple_choice_text_json["bitmark"]["multipleChoiceText"]["body"][1]["choices"],
               key=lambda t: t["choice"])

    assert all_json["bitmark"]["multipleChoiceText"] == multiple_choice_text_json["bitmark"]["multipleChoiceText"]
    multiple_choice_text = all_json["bitmark"]["multipleChoiceText"]
    assert multiple_choice_text["format"] == format
    assert multiple_choice_text["meta"] == meta
    assert multiple_choice_text["feedbackEngine"] == feedback_engine(multiple_choice_text["type"])
    assert multiple_choice_text["instruction"] == multiple_choice_instruction
    assert multiple_choice_text["type"] == "multiple-choice-text"
    assert multiple_choice_text["body"] == [
        {
            "type": "text",
            "text": "Es regnet sehr "
        },
        {
            "type": "choices",
            "choices": [
                {
                    'choice': 'hart',
                    'isCorrect': False,
                    'isSelected': False
                },
                {
                    'choice': 'krank',
                    'isCorrect': False,
                    'isSelected': False
                },
                {
                    'choice': 'scharf',
                    'isCorrect': False,
                    'isSelected': False
                },
                {
                    'choice': target_word,
                    'isCorrect': True,
                    'isSelected': False
                }
            ]
        },
        {
            "type": "text",
            "text": "."
        }
    ]
