import itertools
import re

import openai
import translators as ts

openai.api_key = "REPLACE_ME_WITH_YOUR_OPENAI_KEY"

LANGUAGE_CODE_TO_LANGUAGE = {"fr": "French", "es": "Spanish"}

def init_phrases():
    messages = [{"role": "system", "content":
        "You are teacher helping a language learner."}]
    messages.append(
        {"role": "user", "content": "Tell me five common English sentences in quotation marks."},
    )

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message.content

    return messages, reply


def clean_phrases(raw_phrases: str):
    raw_phrases = raw_phrases.split("\n")
    cleaned_phrases = []
    for phrase in raw_phrases:
        start = phrase.find('"')
        if start != -1:
            phrase = phrase[start:]
        cleaned_phrases.append(phrase.strip().strip("'\""))

    return cleaned_phrases


def instruct_eng_to_other(phrases, language):
    for phrase in phrases:
        print(f"Here's a common English sentence. Please translate it to {LANGUAGE_CODE_TO_LANGUAGE[language]}.")
        print(f"\t{phrase}")
        user_translated = input("Type the translated phrase: ")
        user_translated_clean = re.sub(r'[^a-zA-Z ]+', '', user_translated)
        other_lang = ts.translate_text(phrase, translator='google', to_language=language)
        other_lang_clean = re.sub(r"[^a-zA-Z ']+", '', other_lang)

        top_score = len(other_lang_clean.split())
        user_score = 0
        for user_word, other_word in itertools.zip_longest(user_translated_clean.split(), other_lang_clean.split()):
            if user_word is None or other_word is None:
                break
            if user_word.lower() == other_word.lower():
                user_score += 1

        print(f"Your translation: {user_translated}")
        print(f"Our translation: {other_lang}")
        grade = round(user_score * 100 / top_score, 2)
        if grade == 100:
            print(f"Wow, you translated the phrase perfectly!!")
        elif grade >= 75:
            print(f"Congratulations, you scored: {grade}%!")
        elif grade >= 50:
            print(f"Not bad, you scored: {grade}%.")
        elif grade <= 50:
            print(f"Keep trying, you scored: {grade}%.")

        print()


def instruct_other_to_en(phrases, language):
    for phrase in phrases:
        other_lang = ts.translate_text(phrase, translator='google', from_language="en", to_language=language)
        phrase_clean = re.sub(r"[^a-zA-Z ']+", '', phrase)
        print(f"Here's a common {LANGUAGE_CODE_TO_LANGUAGE[language]} sentence. Please translate it to English.")
        print(f"\t{other_lang}")
        user_translated = input("Type the translated phrase: ")
        user_translated_clean = re.sub(r'[^a-zA-Z ]+', '', user_translated)

        top_score = len(phrase_clean.split())
        user_score = 0
        for user_word, other_word in itertools.zip_longest(user_translated_clean.split(), phrase_clean.split()):
            if user_word is None or other_word is None:
                break
            if user_word.lower() == other_word.lower():
                user_score += 1

        print(f"Your translation: {user_translated}")
        print(f"Our translation: {phrase}")
        grade = round(user_score * 100 / top_score)
        if grade == 100:
            print(f"Wow, you translated the phrase perfectly!!")
        elif grade >= 75:
            print(f"Congratulations, you scored: {grade}%!")
        elif grade >= 50:
            print(f"Not bad, you scored: {grade}%.")
        elif grade <= 50:
            print(f"Keep trying, you scored: {grade}%.")

        print()


def main():
    print("Welcome to the language learning tutorial!")
    raw_language = input("Which langugage would you like to learn today? Enter fr for French or es for Spanish: ")
    if raw_language not in LANGUAGE_CODE_TO_LANGUAGE:
        print(f"Error: Langugage {raw_language} not found, please enter fr or es")
        exit(1)

    choice = input(f"Enter 0 to learn by translating {LANGUAGE_CODE_TO_LANGUAGE[raw_language]}-to-English or 1 to learn by translating English-to-{LANGUAGE_CODE_TO_LANGUAGE[raw_language]}: ")
    try:
        choice = int(choice)
        if choice not in (0, 1):
            print(f"Error: Please choose a valid option")
    except ValueError:
        print(f"Error: Please choose a valid option")

    messages, raw_phrases = init_phrases()
    phrases = clean_phrases(raw_phrases)
    if choice == 0:
        instruct_other_to_en(phrases, raw_language)
    else:
        instruct_eng_to_other(phrases, raw_language)


if __name__ == '__main__':
    main()
