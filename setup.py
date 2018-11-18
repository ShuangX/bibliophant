from setuptools import setup, find_packages

setup(
    name="bibliophant",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "prompt_toolkit >= 2.0", "sqlalchemy"],
    entry_points="""
        [console_scripts]
        bib=bibliophant.cli.main:bib
    """,
)
