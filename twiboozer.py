from lib.textgen import TextGen
from lib.twibot import TwiBot


def main():
    twibot = TwiBot()
    tweets = twibot.get_timeline()

    # TODO gen text and tweet it


if __name__ == '__main__':
    main()
