<p align=" center">
  <a href="https://bitmark-association.org/opentaskpool"><img src="https://tb-open-taskpool.s3.eu-central-1.amazonaws.com/open-taskpool.png" alt="open taskpool" style="height: 150px"/></a>
</p>
<p align="center">
  The open taskpool is an open source curated set of language learning tasks, free to use under<br><br>
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg" alt="Creative Commons" />
  <br>
  Creative Commons Attribution 4.0
  </a>
</p>

---

Currently supported are the following language learning tasks for UK 🇺🇦 - DE 🇩🇪:
- select the missing word
- write the missing word
- write what you hear
- translate the sentence

The data format used is the open source standard [Bitmark](https://bitmark-association.org/).

# Exercise Examples

Check out our [Showroom](https://showroom.taskbase.com/chapter/2/page/0) and see how open taskpool exercises and the 
[Taskbase Feedback Engine ©](https://www.taskbase.com/) can bring your language learning platform to the next level 🚀.

# Requirements

## Managed Hosting

None 😎 

A free hosted server is available at [https://taskpool.taskbase.com/](https://taskpool.taskbase.com/redoc)

## Self-hosting

- Python 3.10
- Package dependencies

    ```shell
    cd server
    pip3 install -r requirements.txt
    ```

However, you can also use Docker and run the server within a container. 

Check usage instructions on _"How to run the API server"_ below.

## Data Generation

- Python 3.7
- Jupyter Notebook
- Package dependencies:
    ```shell
    cd scripts
    pip3 install -r requirements.txt
    ```

# Usage

## With Managed Hosting

_This section is for you if you wish to integrate the open taskpool into your project but do not seek
to self-host or extend it yourself_.

The open taskpool ist hosted under [https://taskpool.taskbase.com](https://taskpool.taskbase.com/redoc).

All you will need are the two following endpoints:

1. `GET` [https://taskpool.taskbase.com/words?translationPair=uk->de](https://taskpool.taskbase.com/words?translationPair=uk->de)

    This endpoint gives you a list of all learnable words for the `"uk->de"` language pair. 

    A list of all supported language pairs you can get by doing a `GET` [https://taskpool.taskbase.com/translation-pairs](https://taskpool.taskbase.com/translation-pairs). However, by now only `"uk->de"` is supported, so you can skip this step.

1. `GET` [https://taskpool.taskbase.com/exercises?translationPair=uk->de&word={your_word}](https://taskpool.taskbase.com/exercises?translationPair=uk->de&word={your_word})

    This endpoint gives you exercises for the specified `{your_word}` which shall be a word from the list obtained in the previous step.
    Try for example the word: [Buchstabe](https://taskpool.taskbase.com/exercises?translationPair=uk->de&word=Buchstabe).

    By default, this endpoint returns the `bitmark.essay` exercise type, which represent the "translate the sentence" and "write what you hear" task.
    If you wish to get other exercise types, you can do so by specifying the `exerciseType` parameter.

Check out the [OpenAPI Specification](https://taskpool.taskbase.com/redoc) for more details.

### How do I get automatic feedback for students working with open taskpool exercises?

This is where the [Taskbase Feedback Engine ©](https://www.taskbase.com/) will help you.

It is accessible via a [Bitmark Feedback API](https://bitmark-api.taskbase.com/documentation) and
integrates seamlessly with the open taskpool. 

After aggregating the returned [Bit](https://docs.bitmark.cloud/bits_overview/) exercise with student input
you can do a `POST` to [computeFeedback](https://bitmark-api.taskbase.com/documentation#operation/computeFeedback), and you'll receive
automatic feedback to the student's input for the specific open taskpool exercise.


### Get a free trial to the Feedback API 

Coming Soon - stay tuned 🤓.

## With Self-hosting

### How to run the API server

_This section is for you if you wish to run the Taskpool API server yourself._

A seeded `taskpool.db` SQLite database with language learning exercises for UK 🇺🇦 - DE 🇩🇪 can be downloaded [here](https://tb-open-taskpool.s3.eu-central-1.amazonaws.com/taskpool.db). Download that file and place it inside the root of this repository.

Running the API server is possible via docker. Simply do the following from within the root:
   ```shell
   cd docker/local-dev-env
   docker-compose up
   ```

This will spin up a docker container and expose the API server under port [:58000](http://localhost:58000).
Visit [localhost:58000/redoc](http://localhost:58000/redoc) to access the OpenAPI Specification.


### How to generate your own exercises 

_This section is for you if you wish to better understand how the automatic task generation works, or you
would like to create your own exercises._

Under [./scripts](./scripts) you will find a [README.md](./scripts/README.md) and all required scripts and jupyter notebooks
that were used for generating the exercises. Following the steps there, you'll end up creating your own `taskpool.db` which
you can then expose via the API server. By adjusting parameters in the scripts you'll be able to create your own exercises
in the languages of your choice.

# Credits

## Data Sources

All source data currently used in the open taskpool comes from the [Tatoeba Project](https://tatoeba.org/en) and are made
available via the [Creative Commons Attribution 2.0](https://creativecommons.org/licenses/by/2.0/) License.

![Creative Common](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)