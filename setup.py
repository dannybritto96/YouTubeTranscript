import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YouTubeTranscript",
    version="1.0",
    author="Danie Britto",
    author_email="danieb1996@live.com",
    description="YouTube Transcript Downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dannybritto96/YouTubeTranscript",
    install_requires=[
        "youtube-dl",
        "bs4",
        "requests"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
