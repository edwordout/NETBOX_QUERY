from setuptools import setup


with open('requirements.txt', 'r') as f:
    requirements_li = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='netbox_query',
    version='0.1.0',
    author='edwordout',
    author_email='e-gomes@live.com',
    description='A CLI client for querying NetBox devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/edwordout/netbox_query',
    packages=['package'],
    install_requires=requirements_li,
    entry_points={
        'console_scripts': [
            'netbox-query=package.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    python_requires='>=3.6',
)
