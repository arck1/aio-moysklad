from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

version = '0.1'

setup(
    name='aio-moysklad',
    version=version,

    author='arck1',
    author_email='a.v.rakhimov@gmail.com',

    description="Async API wrapper for moysklad.ru",
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/arck1/aio-moysklad',
    download_url='https://github.com/arck1/aio-moysklad/archive/v{}.zip'.format(
        version
    ),
    install_requires=[
        'aiohttp>=3.5.4',
        'ujson>=1.35',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='moysklad.ru moysklad aio asyncio wrapper api'
)
