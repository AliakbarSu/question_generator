# Question Generator

This simple python app generates AMC MCQ like questions using ChatGTP and saves the questions to MongoDB.

## Installation

- Navigate to the project directory
- Run `poetry install`

## Running the application

- Make sure the have exported the environment variables `OPENAI_API_KEY` and `MONGODB_URI`. e.g `export OPENAI_API_KEY=some_key`
- Run `poetry run python main.py`

## Generating questions

The interface for this application is very simple. Once you start the app, a question will be generated by selecting `Generate` from the option list. You can save the question by selecting `Save` or `Generate` to generate another question.
