from logging import basicConfig, getLogger, StreamHandler, ERROR, INFO
import sys


basicConfig()
logger = getLogger('MulTweet')
logger.setLevel(INFO)


log = logger.log
