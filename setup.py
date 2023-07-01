from setuptools import find_packages, setup
from typing import List

hyphen_e_dot = '-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    this funciton returns the list of requirements
    '''
    requirements =[]
    with open(file_path) as file_1:
        requirements = file_1.readlines()
        requirements = [req.replace("\n", " ") for req in requirements]

        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)

    return requirements

setup(
    name = "Mlproject",
    version = "0.0.1",
    author = "prince",
    author_email = 'prince.gurung@selu.edu',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)