DROP TABLE IF EXISTS user_skill_levels;
CREATE TABLE user_skill_levels
(
    username    VARCHAR(255),
    language    VARCHAR(255),
    skill_Level INTEGER,
    PRIMARY KEY (username, language)
);

DROP TABLE IF EXISTS sentences;
CREATE TABLE sentences
(
    id              INTEGER PRIMARY KEY,
    language        VARCHAR(255),
    text            TEXT,
    author          VARCHAR(255),
    translated_from INTEGER REFERENCES sentences (id),
    word_count      INTEGER
);
CREATE INDEX idx_sentences_language ON sentences (language);

DROP TABLE IF EXISTS translations;
CREATE TABLE translations
(
    id INTEGER PRIMARY KEY autoincrement,
    s1 INTEGER REFERENCES sentences (id),
    s2 INTEGER REFERENCES sentences (id)
);
CREATE INDEX idx_translations_s1 ON translations (s1);
CREATE INDEX idx_translations_s2 ON translations (s2);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags
(
    name        VARCHAR(255),
    sentence_id INTEGER REFERENCES sentences (id),
    PRIMARY KEY (name, sentence_id)
);

DROP TABLE IF EXISTS lemmata;
CREATE TABLE lemmata
(
    id   INTEGER PRIMARY KEY,
    language VARCHAR(255),
    word VARCHAR(255)
);
CREATE INDEX idx_lemmata_word ON lemmata(word);

DROP TABLE IF EXISTS sentence_lemma;
CREATE TABLE sentence_lemma
(
    sentence_id INTEGER REFERENCES sentences (id),
    lemma_id    INTEGER REFERENCES lemmata (id),
    PRIMARY KEY (sentence_id, lemma_id)
);
CREATE INDEX idx_sl_lemma_id ON sentence_lemma (lemma_id);

DROP TABLE IF EXISTS vocabulary;
CREATE TABLE vocabulary
(
    id       INTEGER PRIMARY KEY,
    language VARCHAR(255),
    word     VARCHAR(255),
    length   INTEGER
);
CREATE INDEX idx_vocabulary_language ON vocabulary (language);
CREATE INDEX idx_vocabulary_word ON vocabulary (word);
CREATE INDEX idx_vocabulary_length ON vocabulary (length);

DROP TABLE IF EXISTS sentence_vocabulary;
CREATE TABLE sentence_vocabulary
(
    sentence_id REFERENCES sentences (id),
    vocabulary_id REFERENCES vocabulary (id),
    PRIMARY KEY (sentence_id, vocabulary_id)
);
CREATE INDEX idx_sv_vocabulary_id ON sentence_vocabulary (vocabulary_id);

CREATE TABLE exercise
(
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    translation_id INTEGER NOT NULL,
    target_word VARCHAR(255) NOT NULL,
    similar_words JSON,
    source_sentence_id INTEGER NOT NULL,
    target_sentence_id INTEGER NOT NULL,
    FOREIGN KEY (translation_id) REFERENCES translations(id),
    FOREIGN KEY (source_sentence_id) REFERENCES sentences(id),
    FOREIGN KEY (target_sentence_id) REFERENCES sentences(id)
);
CREATE INDEX idx_exercise_target_word ON exercise (target_word);
