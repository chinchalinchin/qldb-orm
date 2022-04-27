import settings
import logging
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)


def test_info():
    settings.LOG_LEVEL = 'INFO'
    assert settings.get_log_level() == logging.INFO


def test_debug():
    settings.LOG_LEVEL = 'DEBUG'
    assert settings.get_log_level() == logging.DEBUG


def test_error():
    settings.LOG_LEVEL = 'ERROR'
    log_level = settings.get_log_level()
    print(log_level)
    assert settings.get_log_level() == logging.ERROR


def test_notset():
    settings.LOG_LEVEL = None
    assert settings.get_log_level() == logging.NOTSET
