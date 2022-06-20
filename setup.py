import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zet-cli",
    version="0.0.1",
    author="Matthew Wimberly",
    author_email="matthew.wimb@gmail.com",
    description="A Zettlekasten CLI implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattdood/zet-cli",
    project_urls={
        "Bug Tracker": "https://github.com/mattdood/zet-cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={
        "console_scripts": ["zet=zet.main:main"]
    },
    python_requires=">=3.6",
)
