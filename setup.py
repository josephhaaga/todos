import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="todos",
    version="1.0.0",
    description="Manage tasks from the command line",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/josephhaaga/todos",
    author="Joseph Haaga",
    author_email="haaga.joe@gmail.com",
    license="MIT",
    packages=["todos"],
    include_package_data=True,
    install_requires=["tinydb", "click"],
    entry_points={"console_scripts": ["todo=todos.__main__:main",]},
)
