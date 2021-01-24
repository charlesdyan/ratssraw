from setuptools import find_packages
from setuptools import setup

setup(
    name='ratssraw',
    version='1',
    author='Charles Yan',
    author_email='charles4yan@gmail.com',
    description='simple server for vh',
    url='https://github.com/charlesdyan/ratssraw',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',
        'Flask-Caching'],
    extras_require={'test': ['pytest']}
)