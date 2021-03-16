# System import
import os
import unittest
import unittest.mock as mock
from unittest.mock import patch, mock_open
from collections import Counter

# Package import
from text_mining import (get_words, get_text, count_words,
                         count_phrases, file_download, main)


class TestTextMining(unittest.TestCase):
    """ Test the text mining script.
    """

    def setUp(self):
        """ Setup test.
        """
        self.url = "http://www.gutenberg.org/files/84/84-0.txt"
        self.output_dir = "/tmp"
        self.filepath = "/tmp/84-0.txt"
        self.start_delim = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN \*\*\*"
        self.end_delim = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN \*\*\*"
        self.text = """
        This is sample text, including word counts?

        *** START OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN ***
        This is sample text, including word counts. Here is: a-sentence !
        Including word counts?

        -----

        *** END OF THE PROJECT GUTENBERG EBOOK FRANKENSTEIN ***
        Including word counts?

        """
        self.content = """
        This is sample text, including word counts. Here is: a-sentence !
        Including word counts?

        -----

        """
        self.words = ["this", "is", "sample", "text", "including", "word",
                      "counts", "here", "is", "a", "sentence",
                      "including", "word", "counts"]
        self.word_counts = Counter(
            {'this': 1,
            'is': 2,
            'sample': 1,
            'text': 1,
            'including': 2,
            'word': 2,
            'counts': 2,
            'here': 1,
            'a': 1,
            'sentence': 1}
        )
        self.phrases_count = Counter({
            ('this', 'is', 'sample'): 1,
            ('is', 'sample', 'text'): 1,
            ('sample', 'text', 'including'): 1,
            ('text', 'including', 'word'): 1,
            ('including', 'word', 'counts'): 2,
            ('word', 'counts', 'here'): 1,
            ('counts', 'here', 'is'): 1,
            ('here', 'is', 'a'): 1,
            ('is', 'a', 'sentence'): 1,
            ('a', 'sentence', 'including'): 1,
            ('sentence', 'including', 'word'): 1}
        )


    def tearDown(self):
        """ Run after each test.
        """
        pass


    def test_file_download(self):
        """ Test the file_download function.
        """
        fp = file_download(self.url, self.output_dir)
        self.assertEqual(fp, self.filepath)
        self.assertTrue(os.path.isfile(fp))


    def test_get_text(self):
        """ Test the get_text function.
        """
        with patch("builtins.open", mock_open(read_data=self.text)) \
                as mock_file:
            res = get_text(self.filepath, self.start_delim, self.end_delim)
            mock_file.assert_called_with(self.filepath)
            self.assertEqual(res, self.content)


    def test_get_text_must_throw_exception_no_delimiters(self):
        """ Test that get_text function throws exception when
            no text matches delimiters.
        """
        bad_text = "no data"
        with patch("builtins.open", mock_open(read_data=bad_text)) \
                as mock_file:
            self.assertRaises(AssertionError,
                              get_text,
                              self.filepath,
                              self.start_delim,
                              self.end_delim)
            mock_file.assert_called_with(self.filepath)


    def test_get_words(self):
        """ Test the get_words function.
        """
        res = get_words(self.content)
        self.assertEqual(res, self.words)


    def test_count_words(self):
        """ Test the count_words function.
        """
        res = count_words(self.words)
        self.assertDictEqual(res, self.word_counts)


    def test_count_phrases(self):
        """ Test the count_phrases function.
        """
        res = count_phrases(self.words)
        self.assertDictEqual(res, self.phrases_count)


    @mock.patch("text_mining.file_download")
    @mock.patch("text_mining.get_text")
    def test_main(self, mock_get_text, mock_file_download):
        """ Test the word count function.
        """
        mock_file_download.return_value = self.filepath
        mock_get_text.return_value = self.content
        res = main(self.url, self.output_dir, self.start_delim, self.end_delim)
        self.assertDictEqual(res[0], self.word_counts)
        self.assertDictEqual(res[1], self.phrases_count)


if __name__ == "__main__":
    unittest.main()
