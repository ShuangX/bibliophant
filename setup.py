from setuptools import setup, find_packages

setup(
    name="bibliophant",
    version="0.1",
    description="a tool for managing bibliography data and PDF documents",
    packages=find_packages(),
    author="Markus Lohmayer",
    author_email="markus.lohmayer@gmail.com",
    url="https://github.com/MarkusLohmayer/bibliophant",
    include_package_data=True,
    install_requires=["Click", "prompt_toolkit >= 2.0", "sqlalchemy", "ipython"],
    entry_points="""
        [console_scripts]
        bib=bibliophant.cli.main:bib
    """,
)
