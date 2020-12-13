import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_graph",
    version="0.1.0",
    author="Jiaying Wang",
    author_email="jiaying@sjzu.edu.cn",
    description="A simple graph package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiayingwang/simple_graph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['elegant-structure'],
    python_requires='>=3.6',
)