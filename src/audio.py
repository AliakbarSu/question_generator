from pymongo import MongoClient
from pymongo.server_api import ServerApi
from question import Question, Option
import os
import json
import boto3

BUCKET_NAME = "practicemed-audio-mcqs"


def save_audio_to_s3(audio_file_path, bucket_name, object_name):
    """
    Save audio to S3.
    """
    s3 = boto3.client("s3")
    try:
        # Upload the file
        s3.upload_file(audio_file_path, bucket_name, object_name)
        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        print(f"Audio file uploaded successfully. S3 URL: {s3_url}")
        return s3_url

    except Exception as e:
        print(f"Error uploading audio file to S3: {e}")
        return None


def text_to_speech(text, output_format="mp3", voice_id="Joanna"):
    """
    Converts text to speech using AWS Polly.

    Parameters:
    - text: The input text to convert to speech.
    - output_format: The desired audio output format (default is 'mp3').
    - voice_id: The ID of the voice to use (default is 'Joanna').

    Returns:
    - The audio data in bytes.
    """
    # Create a Polly client
    polly = boto3.client("polly")
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=text, OutputFormat=output_format, VoiceId=voice_id
        )
        # Extract the audio data
        audio_data = response["AudioStream"].read()
        print("Text converted to speech successfully.")
        return audio_data

    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return None


def generate_text_for_audio(question: Question):
    """
    Generate text for polly model.
    """
    return f"{question.text}. Options are: Option {question.options[0].alpha} - {question.options[0].text}. Option {question.options[1].alpha} - {question.options[1].text}. Option {question.options[2].alpha} - {question.options[2].text}. Option {question.options[3].alpha} - {question.options[3].text}. Option {question.correct_option.alpha} is correct, because, {question.correct_option.explanation}."


def geneate_audio():
    with open("questions.json", "r") as f:
        questions = json.load(f)
        for question in questions:
            question = Question(
                text=question["text"],
                options=[
                    Option(
                        alpha=option["alpha"],
                        text=option["text"],
                        is_correct=option["is_correct"],
                        explanation=option["explanation"],
                    )
                    for option in question["options"]
                ],
            )
            text = generate_text_for_audio(question)
            audio_data = text_to_speech(text)

            if audio_data:
                file_name = f"./files/question={question.uuid}.mp3"
                with open(file_name, "wb") as f:
                    f.write(audio_data)
                save_audio_to_s3(file_name, BUCKET_NAME, file_name)


if __name__ == "__main__":
    geneate_audio()
