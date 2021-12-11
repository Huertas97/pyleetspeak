from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Transform casual text into a leetspeak version.'
LONG_DESCRIPTION = 'Transform casual text into a leetspeak version. You can modify the probability of different transformation and the frequency of that transformation. Currently only Basic Leet mode is available: every vowel is substituted for a number.'

# Setting up
setup(
    name="pyleetspeak",
    version=VERSION,
    author="Álvaro Huertas García",
    author_email="<alvaro.huertas.garcia@alumnos.upm.es>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['Unidecode'],
    keywords=['leetspeak'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
