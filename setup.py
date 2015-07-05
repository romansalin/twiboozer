# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages


VERSION = "1.1"


setup(
    name="twiboozer",
    author="Roman Salin",
    author_email="romansalin1990@gmail.com",
    description="Simple Markov chain text generator integrated with your "
                "Twitter account and based on timeline",
    keywords="markov chain text generator twitter tweet bot",
    url="https://github.com/romansalin/twiboozer",
    version=VERSION,
    include_package_data=True,
    zip_safe=False,
    install_requires=["twitter>=1.17"],
    packages=find_packages(exclude=["tests*"]),
)
