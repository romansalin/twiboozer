from setuptools import setup, find_packages


setup(
    name="TwiBoozer",
    author="Roman Salin",
    author_email="romansalin1990@gmail.com",
    description="Simple delirium generator for Twitter account based on the "
                "tweets of followers",
    keywords="twitter tweet bot delirium generator",
    url="https://github.com/romansalin/twiboozer",
    version="0.1",
    install_requires=["twitter>=1.16"],
    packages=find_packages(),
)
