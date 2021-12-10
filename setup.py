import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid19_dashboard",
    version="0.0.1",
    author="Max Bennett",
    author_email="mab262@exeter.ac.uk",
    description="A personalized dashboard which maps up to date covid data to a web template",
    long_description="Using a webpage template this package creates a dashboard displaying up to date covid data from "
                     "an api, it also contains news articles obtained from a news api and you can remove articles and "
                     "schedule updates for yourself",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)

