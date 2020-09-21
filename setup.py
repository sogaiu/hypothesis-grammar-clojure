from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hypothesis-grammar-clojure",
    version="0.0.1",
    author="sogaiu",
    description="Hypothesis Strategies for Clojure Grammars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sogaiu/hypothesis-grammar-clojure",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    py_modules=[
        "hypothesis_grammar_clojure",
    ],
    install_requires=[
        "hypothesis",
    ],
)
