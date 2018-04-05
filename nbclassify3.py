import sys
import json
import math
from nblearn3 import filter_word

MODEL_FILE_PATH = "nbmodel.txt"
OUTPUT_FILE_PATH = "nboutput.txt"


def classify():
    model = open(MODEL_FILE_PATH, 'r', encoding='utf-8')
    model = json.load(model)
    test_file_path = sys.argv[1]

    test_data = open(test_file_path, 'r', encoding='utf-8')
    output_file = open(OUTPUT_FILE_PATH, 'w')
    for line in test_data:
        output = find_class(line, model)
        print("{} {} {}".format(output['hash'], output['class1'], output['class2']))
        output_file.write("{} {} {}\n".format(output['hash'], output['class1'], output['class2']))


def find_class(sentence, model):
    classes = ['Fake', 'True', 'Neg', 'Pos']
    words = sentence.split(" ")
    class_probabilities = {}
    output = {}

    # Initialize the probability for each class with the prior probabilities.
    for class_name in classes:
        prior_class_count = model['prior_class_count'][class_name]
        class_probabilities[class_name] = math.log(prior_class_count/model['line_count'])

    for index, word in enumerate(words):
        if index == 0:
            output['hash'] = word
        else:
            for class_name in classes:
                word = filter_word(word)
                word_freq = word_frequency(word, model, class_name)
                class_frequency = (model['total_word_count'][class_name] + model['unique_word_count'])
                word_probability = (word_freq + 1)/class_frequency
                class_probabilities[class_name] += math.log(word_probability)

    output['class1'] = 'Fake' if class_probabilities['Fake'] > class_probabilities['True'] else 'True'
    output['class2'] = 'Pos' if class_probabilities['Pos'] > class_probabilities['Neg'] else 'Neg'
    return output


def word_frequency(word, model, class_name):
    if word not in model['class_word_count'][class_name]:
        freq = 0
    else:
        freq = model['class_word_count'][class_name][word]
    return freq


if __name__ == "__main__":
    classify()
