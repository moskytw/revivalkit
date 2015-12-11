from setuptools import setup, find_packages

import revival

setup(
    name='revival',
    version=revival.__version__,
    description='Revive from Ctrl-C or any exception!',
    long_description='Revive from Ctrl-C or any exception!',
    author='Mosky',
    author_email='mosky.tw@gmail.com',
    #url='',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    zip_safe=True,
)
