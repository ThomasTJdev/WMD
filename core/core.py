#!/usr/bin/env python3
#
# MIT - (c) 2016 ThomasTJ (TTJ)
#


import configparser
import logging
from logging.config import fileConfig


def config():
    config = configparser.ConfigParser()
    try:
        config.read('core/config.ini')
    except:
        config.read('config.ini')
    return config


def log():
    try:
        fileConfig('core/config_logging.ini')
    except:
        fileConfig('config_logging.ini')        
    return logging.getLogger()
