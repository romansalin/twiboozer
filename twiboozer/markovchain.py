# -*- encoding: utf-8 -*-

from __future__ import division
try:
    import cPickle as pickle
except ImportError:
    import pickle
import sys
import random
import os
import re
import datetime


# TODO memorization previous tweet corpus
class MarkovChain(object):
    def __init__(self, db_file_path=None):
        self.db_file_path = db_file_path
        if not db_file_path:
            directory = "db"
            filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.db_file_path = os.path.join(directory, filename)
        try:
            with open(self.db_file_path, 'rb') as dbfile:
                self.db = pickle.load(dbfile)
        except IOError:
            sys.stdout.write('Database file not found, using empty database')
            self.db = {}
        except ValueError:
            sys.stdout.write('Database corrupt or unreadable, using empty database')
            self.db = {}

    def generate_database(self, text_sample, sentence_sep='[.!?\n]'):
        """Generate word probability database from raw content string."""
        # Get an iterator for the 'sentences'
        text_sample = self._word_iter(text_sample, sentence_sep)
        # We're using '' as special symbol for the beginning
        # of a sentence
        self.db = {"": {"": 0.0}}
        for line in text_sample:
            words = line.strip().split()  # split words in line
            if len(words) == 0:
                continue
            # first word follows a sentence end
            if words[0] in self.db[""]:
                self.db[""][words[0]] += 1
            else:
                self.db[""][words[0]] = 1.0
            for i in range(len(words) - 1):
                if words[i] in self.db:
                    # the current word has been found at least once
                    # increment parametrized wordcounts
                    if words[i + 1] in self.db[words[i]]:
                        self.db[words[i]][words[i + 1]] += 1
                    else:
                        self.db[words[i]][words[i + 1]] = 1.0
                else:
                    # word has been found for the first time
                    self.db[words[i]] = {words[i + 1]: 1.0}
            # last word precedes a sentence end
            if words[len(words) - 1] in self.db:
                if "" in self.db[words[len(words) - 1]]:
                    self.db[words[len(words) - 1]][""] += 1
                else:
                    self.db[words[len(words) - 1]][""] = 1.0
            else:
                self.db[words[len(words) - 1]] = {"": 1.0}

        # We've now got the db filled with parametrized word counts
        # We still need to normalize this to represent probabilities
        for word in self.db:
            wordsum = 0
            for nextword in self.db[word]:
                wordsum += self.db[word][nextword]
            if wordsum != 0:
                for nextword in self.db[word]:
                    self.db[word][nextword] /= wordsum
        # Now we dump the db to disk
        return self.dumpdb()

    def dumpdb(self):
        try:
            with open(self.db_file_path, 'wb') as dbfile:
                pickle.dump(self.db, dbfile)
            # It looks like db was written successfully
            return True
        except IOError:
            sys.stderr.write('Database file could not be written')
            return False

    def generate_string(self):
        """.Generate a "sentence" with the database of known text."""
        return self._accumulate_with_seed('')

    def generate_string_with_seed(self, seed):
        """Generate a "sentence" with the database and a given word."""
        # using str.split here means we're contructing the list in memory
        # but as the generated sentence only depends on the last word of the seed
        # I'm assuming seeds tend to be rather short.
        words = seed.split()
        if len(words) > 0 and words[len(words) - 1] in self.db:
            sen = ''
            if len(words) > 1:
                sen = words[0]
                for i in range(1, len(words) - 1):
                    sen = sen + ' ' + words[i]
                sen += ' '
            return sen + self._accumulate_with_seed(words[len(words) - 1])
        # Just pretend we've managed to generate a sentence.
        sep = ' '
        if seed == '':
            sep = ''
        return seed + sep + self.generate_string()

    @staticmethod
    def _word_iter(text, separator='.'):
        """
        An iterator over the "words" in the given text, as defined by
        the regular expression given as separator.
        """
        exp = re.compile(separator)
        pos = 0
        for occ in exp.finditer(text):
            sub = text[pos:occ.start()].strip()
            if sub:
                yield sub
            pos = occ.start() + 1
        if pos < len(text):
            # take case of the last part
            sub = text[pos:].strip()
            if sub:
                yield sub

    def _accumulate_with_seed(self, seed):
        """
        Accumulate the generated sentence with a given single word as a seed.
        """
        next_word = self._next_word(seed)
        sentence = [seed] if seed else []
        while next_word:
            sentence.append(next_word)
            next_word = self._next_word(next_word)
        return ' '.join(sentence)

    def _next_word(self, lastword):
        probmap = self.db[lastword]
        sample = random.random()
        # since rounding errors might make us miss out on some words
        maxprob = 0.0
        maxprobword = ""
        for candidate in probmap:
            # remember which word had the highest probability
            # this is the word we'll default to if we can't find anythin else
            if probmap[candidate] > maxprob:
                maxprob = probmap[candidate]
                maxprobword = candidate
            if sample > probmap[candidate]:
                sample -= probmap[candidate]
            else:
                return candidate
        return maxprobword
