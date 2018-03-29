import sys
import json

MODEL_FILE_PATH = "nbmodel.txt"
NUMBER_OF_CLASSES = 2


def create_model():
    training_data_path = sys.argv[1];
    if training_data_path is None:
        print("Enter path to training data")
        exit(1)

    input_file = open(training_data_path, 'r', encoding='utf-8')
    output = parse_input_file(input_file)
    output_file = open(MODEL_FILE_PATH, "w")
    json.dump(output, output_file)


def parse_input_file(input_file):
    prior_class_count = {}
    line_count = 0
    class_word_count = {}
    classes = []
    total_word_count = {}
    unique_words = set()

    for line in input_file:
        words = line.split(" ") # TODO incorporate multi-separators here.

        for index, word in enumerate(words):
            if index in range(1, NUMBER_OF_CLASSES + 1):
                classes.append(word)
                add_one(prior_class_count, word)
            else:
                for class_name in classes:
                    increment_word_count(class_word_count, class_name, word)
                    add_one(total_word_count, class_name)
            unique_words.add(word)

        line_count += 1
        classes.clear()

    output = {
        "class_word_count": class_word_count,
        "prior_class_count": prior_class_count,
        "line_count": line_count,
        "total_word_count": total_word_count,
        "unique_word_count": len(unique_words)
    }

    return output


# Increment the word count in the class' dictionary
def increment_word_count(dictionary, class_name, word):
    if class_name not in dictionary:
        dictionary[class_name] = {}
    class_frequencies = dictionary[class_name]
    add_one(class_frequencies, word)


def add_one(dictionary, key):
    if key not in dictionary:
        dictionary[key] = 1
    else:
        dictionary[key] += 1


if __name__ == "__main__":
    create_model()