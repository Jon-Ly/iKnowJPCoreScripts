import json
import re
import os

MEMRISE_FORMAT = 1
QUIZLET_FORMAT = 2
ANKI_FORMAT = 3

def generate_csv(json_data, format):
    result = ''
    data_range = range(0, len(json_data['goal_items'])) # number of words

    for item_position in data_range:
        item = json_data['goal_items'][item_position]['item']
        sentences = json_data['goal_items'][item_position]['sentences']

        kanji = item['cue']['text']
        hiragana = item['cue']['transliterations']['Hira']
        english = item['response']['text'].replace(',', ';') # replaces commas due to csv format being screwed up

        if format == MEMRISE_FORMAT:
            if hiragana == kanji: # no kanji exists
                result += f'{hiragana},{english}'
            else:
                result += memrise_format(hiragana, english, kanji)
        elif format == QUIZLET_FORMAT:
            result += quizlet_format(hiragana, english, kanji)
        elif format == ANKI_FORMAT:
            result += anki_sentence_format(item, sentences)

        if item_position+1 < len(json_data['goal_items']):
            result += '\n'

    return result

def quizlet_format(hiragana, english, kanji):
    return f'{kanji} ({hiragana}),{english}'

def memrise_format(hiragana, english, kanji):
    return f'{hiragana},{english},{kanji}'

def anki_sentence_format(item, sentences):
    kanji = item['cue']['text']
    hiragana = item['cue']['transliterations']['Hira']
    english = item['response']['text'].replace(',', ';') # replaces commas due to csv format being screwed up
    english_sentence_text = ''
    japanese_sentence_text = ''

    result = ''

    for i in range(0, len(sentences)):
        english_sentence_text = sentences[i]['response']['text']
        japanese_sentence_text = '<h3>' + removeCharacters(sentences[i]['cue']['text']) + '</h3><h6>' + removeCharacters(sentences[i]['cue']['transliterations']['Hira']) + '</h6>'
        if i == len(sentences)-1:
            result += f'{english_sentence_text};{japanese_sentence_text}'
            break
        
        result += f'{english_sentence_text};{japanese_sentence_text}\n'

    return result

def removeCharacters(input):
    return re.sub('<(/*)([A-Za-z]*)>', '', input).replace(' ', '')

def __main__():
    try:
        os.mkdir('csvFiles')
    except OSError as error:
        print(error)

    for core_id in range(1, 7): # 6 cores
        for step_id in range(1, 11): # 10 steps per core
            json_data = json.loads(open(f'jcoreJson/Japanese_Core_{core_id}_{step_id}.txt', 'r', encoding='utf-8-sig').read())
            csv_data = generate_csv(json_data, ANKI_FORMAT)
            new_file = open(f'csvFiles/Japanese_Core_CSV_{core_id}_{step_id}.txt', 'w+', encoding='utf-8-sig')
            new_file.write(csv_data)
            new_file.close()

__main__()