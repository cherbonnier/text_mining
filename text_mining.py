
# System import
import os
import re
import urllib.request
from collections import Counter


def file_download(url, dest_dir):
    """ Performs file download from given url.
    Parameters
    ----------
    url: string
        the url of the ressource to download.
    dest_dir: string
        the directory where the file will be downloaded.
    Returns
    -------
    filepath: string
        the file path of the downloaded file.
    """
    filepath = os.path.join(dest_dir, os.path.basename(url))
    urllib.request.urlretrieve(url, filepath)
    return filepath


def count_phrases(words):
    """ Count the occurences of phrases (3 consecutive words).
    Parameters
    ----------
    words: list
        the list of words ordered as they appear in the original text.
    Returns
    -------
    counter: Counter
        the phrases counter - keys are three words tuples (word1, word2, word3)
    """
    counter = Counter()
    for w_0, w_1, w_2 in zip(words, words[1:], words[2:]):
        counter[(w_0, w_1, w_2)] += 1
    return counter


def count_words(words):
    """ Count the occurences of extracted words.
    Parameters
    ----------
    words: list
        the list of words.
    Returns
    -------
    counter: Counter
        the words counter
    """
    return Counter(words)


def get_text(filepath, start_str, end_str):
    """ Read text file and extract text between two delimiters.
    Parameters
    ----------
    filepath: string
        the path to the text file.
    start_str: string
        the start delimiter.
    start_str: string
        the end delimiter.
    Returns
    -------
    r: string
        the extracted text
    """
    with open(filepath) as f:
        buf = f.read()
    r = re.findall(rf'{start_str}(.*?){end_str}', buf, re.DOTALL)
    assert len(r) == 1, "Could not find text between these delimiters"
    return r[0]


def get_words(text):
    """ Extract words from text using simple regular expression
        and convert them to lower case.
    Parameters
    ----------
    text: string
        the original text.
    Returns
    -------
    words: list
        the extracted words
    """
    words = re.compile(r'\w+').findall(text)
    words = [w.lower() for w in words]
    return words


def main(url, dest_dir, start_str, end_str):
    """ Main function.
    Parameters
    ----------
    url: string
        the url of the ressource to download.
    dest_dir: string
        the directory where the file will be downloaded.
    start_str: string
        the start delimiter.
    end_str: string
        the end delimiter.
    Returns
    -------
    words_counter: Counter
        the words counter
    phrases_counter: Counter
        the phrases counter - keys are three words tuples (word1, word2, word3)
    """
    fp = file_download(url, dest_dir)
    content = get_text(fp, start_str, end_str)
    all_words = get_words(content)
    words_counter = count_words(all_words)
    phrases_counter = count_phrases(all_words)
    return words_counter, phrases_counter


if __name__ == '__main__':
    text_url = "http://www.gutenberg.org/files/84/84-0.txt"
    output_dir = "/tmp"
    start_delim = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN \*\*\*"
    end_delim = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN \*\*\*"
    word_c, phrases_c = main(text_url, output_dir, start_delim, end_delim)
    print(f"Most common words : {word_c.most_common(3)}")
    print(f"Most common phrases : {phrases_c.most_common(3)}")
