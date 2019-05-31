from distutils.core import setup

setup(
    name='LocusSummerData',
    version='0.2019dev',
    packages=['LocusSummerData', ],
    author='Phillip Nguyen',
    author_email='pnguyen@locus.co',
    license='Not Very Useful Why Share This license',
    long_description=open('README.md').read(),
    install_requires=[
        'pandas',
        'tqdm',
        'glob3'
    ]
)
