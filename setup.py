from os import path

from setuptools import find_packages, setup

from csob.version import get_version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='csob-paymentgateway',
    version=get_version(),
    description='Python library to connect to CSOB Payment gateway',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/druids/csob-paymentgateway',
    author='Filip Dobrovolny',
    author_email='brnopcman@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ],
    keywords='payments finance csob paymentgateway',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6, <4',
    install_requires=[
        'pycrypto',
        'import_string',
        'requests',
        'cached-property',
    ],
    extras_require={
        'dev': [
            'spinhx',
        ],
        'test': [
            'freezegun',
            'mock',
        ],
    },
    data_files=[('csob_keys', [
        'csob_keys/mips_platebnibrana.csob.cz.cer',
        'csob_keys/mips_platebnibrana.csob.cz.pub',
        'csob_keys/mips_iplatebnibrana.csob.cz.cer',
        'csob_keys/mips_iplatebnibrana.csob.cz.pub',
        'csob_keys/rsa_test_A3746UdxZO.key',
        'csob_keys/readme.txt',
    ])],
    project_urls={
        'Source': 'https://github.com/druids/csob-paymentgateway',
    },
)
