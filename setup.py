from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()
with open("README.md", mode="r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

VERSION = '0.2.8'
DESCRIPTION = 'Transform casual text into a leetspeak and word camouflage version.'
LONG_DESCRIPTION = 'Transform casual text into a leetspeak version. You can modify the probability of different transformation, the frequency of that transformation, the type of substitutions applied among other parameters (see examples of use below).'

# Setting up
#  python setup.py sdist bdist_wheel
# python -m twine upload  dist/*  --repository testpypi
# Para probarlo
# pip install  --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyleetspeak

# cuando todo funcione vas a Pypi legacy
# python -m twine upload  dist/*  --repository pypi
setup(
    name="pyleetspeak",
    version=VERSION,
    author="Álvaro Huertas García",
    author_email="<alvaro.huertas.garcia@alumnos.upm.es>",
    url='https://github.com/Huertas97/pyleetspeak',
    description=DESCRIPTION,
    long_description=readme,  # long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "codetiming",
        "keybert",
        "matplotlib",
        "nltk==3.6.7",
        "numpy==1.21.5",
        "Pyphen",
        "scikit_learn==1.0.2",
        "setuptools",
        "spacy==3.4.3",
        "tqdm",
        "Unidecode",
    ],
    keywords=['leetspeak', "woord camouflage", "content evasion",
              "information disorders", "social media"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
