import os
import re


def get_lang_reserved_words(lang):
    """
    Load the reserved words of the specified language

    :param lang: str, the name of the language
    :return: list, all the reserved keywords
    """
    join, dirname, abspath = os.path.join, os.path.dirname, os.path.abspath
    nirpath = dirname(dirname(abspath(__file__)))
    root_path = join(nirpath, "resources")  # root_path = "../resources"
    supported_lang = [fn.replace(".txt", "") for fn in os.listdir(root_path)]
    if lang not in supported_lang:
        raise ValueError("Reserved words for language {lang} is not available. Please choose from %s" %
                         ",".join(supported_lang))

    with open(os.path.join(root_path, f"{lang}.txt")) as f:
        reserved_words = [word.strip() for word in f]

    return reserved_words


def code_tokenize(sent, return_str=True, lowercase=True):
    """
    Tokenize according to camelCase and snake_case

    :param sent: str, the sentence to remove non-alphabetic
    :param return_str: bool, return str when set to True, otherwise return tokenized list. default True
    :return: str, the sentense after camel and snake case is tokenized
    """
    # tokenize according to camel
    camel_patterns = [re.compile("(.)([A-Z][a-z]+)"), re.compile("([a-z0-9])([A-Z])")]
    for pattern in camel_patterns:
        sent = pattern.sub(r"\1 \2", sent)

    # tokenize according to snake
    sent = sent.replace("_", " ")
    if lowercase:
        sent = sent.lower()
    sent = sent.split()  # remove consecutive whitespace

    if return_str:
        sent = " ".join(sent)

    return sent


def remove_non_alphabet(sent, return_str=True):
    """
    Remove all non-alphabetic character

    :param sent: str, the sentence to remove non-alphabetic
    :param return_str: bool, return str when set to True, otherwise return tokenized list. default True
    :return: str, the sentense after non-alphabetics are removed
    """
    sent = re.sub("[^A-Za-z ]", " ", sent)
    sent = sent.split()  # remove consecutive whitespace

    if return_str:
        sent = " ".join(sent)

    return sent


def remove_unicharacter(sent, return_str=True):
    """
    Remove the single letter from the sentence

    :param sent: str, the sentence to remove non-alphabetic
    :param return_str: bool, return str when set to True, otherwise return tokenized list. default True
    :return: str, the sentense after single characters are removed
    """
    sent = [word for word in sent.split() if len(word) > 1]

    if return_str:
        sent = " ".join(sent)

    return sent
