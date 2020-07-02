import re


def code_tokenize(sent, return_str=True):
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
    sent = sent.replace("_", " ").split()

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
    sent = re.sub("^[A-Za-z ]", " ", sent)
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
