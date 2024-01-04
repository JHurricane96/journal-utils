import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirement_list = [r.strip() for r in open("requirements.txt", "r").readlines() if r]

setuptools.setup(
    name="journal-utils",
    install_requires=requirement_list,
    version="0.1",
    author="Arun Ramachandran",
    author_email="ramachandran.arun@outlook.com",
    description="CLI tool with utilities to maintain a markdown journal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhurricane96/journal-utils",
    packages=setuptools.find_packages(),
    license="MIT",
    entry_points={"console_scripts": ["jrnl=journal_utils.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
    ],
)
