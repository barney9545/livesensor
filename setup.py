from setuptools import setup,find_packages

#->list[str] this is used for readablity of code and specifies that output is string
def get_requirements():

    requirements =[]

    return requirements

setup(
    name='sensor',
    version='0.0.1',
    author='darshan',
    packages=find_packages(),
    install_requires=get_requirements()
)