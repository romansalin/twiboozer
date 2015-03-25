# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="TwiBoozer",
    author="Roman Salin",
    author_email="romansalin1990@gmail.com",
    description="Simple Markov chain text generator integrated with your "
                "Twitter account and based on timeline",
    keywords="markov chain text generator twitter tweet bot",
    url="https://github.com/romansalin/twiboozer",
    version="0.1",
    install_requires=["twitter>=1.16", "PyMarkovChain>=1.7"],
    packages=find_packages(),
)
