from setuptools import find_packages,setup
from typing import List

requirements_file_name = "requirements.txt"

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

setup(
    name='Smoke_Detection',
    version='1.0',
    description='Real-time Smoke Detection with AI-based Sensor Fusion',
    author='Pritam Bhakta',
    author_email='pritambhakta97@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements()
    )