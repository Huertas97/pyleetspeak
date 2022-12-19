from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import codecs
import os
import re
import ast

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("pyleetspeak/__init__.py", "rb") as f:
    VERSION = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()
with open("README.md", mode="r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

DESCRIPTION = "Transform casual text into a leetspeak and word camouflage version."
LONG_DESCRIPTION = "Transform casual text into a leetspeak version. You can modify the probability of different transformation, the frequency of that transformation, the type of substitutions applied among other parameters (see examples of use below)."

# Setting up
#  python setup.py sdist bdist_wheel
# python -m twine upload  dist/*  --repository testpypi
# Para probarlo
# pip install  --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyleetspeak

# cuando todo funcione vas a Pypi legacy
# python -m twine upload  dist/*  --repository pypi+



setup(
    name="pyleetspeak",
    version=VERSION,
    author="Álvaro Huertas García",
    author_email="<alvaro.huertas.garcia@alumnos.upm.es>",
    url="https://github.com/Huertas97/pyleetspeak",
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
        "yake==0.4.8",
    ],
    setup_requires=["nltk"],
    keywords=[
        "leetspeak",
        "woord camouflage",
        "content evasion",
        "information disorders",
        "social media",
        "data augmentation",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
)
