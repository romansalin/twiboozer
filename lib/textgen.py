import re
from random import uniform
from collections import defaultdict


class TextGen(object):

    r_alphabet = re.compile(u'[а-яА-Яa-zA-Z0-9-]+|[.,:;?!/]+')

    # TODO
