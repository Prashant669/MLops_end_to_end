import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'models'))

from helper import clean_text


def test_lowercase():
    assert clean_text("HELLO WORLD") == "hello world"


def test_removes_html_tags():
    assert clean_text("good <br> movie") == "good  movie"


def test_removes_punctuation():
    assert clean_text("hello, world!") == "hello world"


def test_removes_digits():
    assert clean_text("movie 123 review") == "movie  review"


def test_combined():
    assert clean_text("GREAT <b>movie</b>!!! 10/10") == "great movie "
