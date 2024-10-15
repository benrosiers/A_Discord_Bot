# A/setup.py

from setuptools import setup, find_packages

setup(
    name='discord-voice-bot',
    version='0.8.3',
    packages=find_packages(),
    install_requires=[
        'discord.py[voice]',
        'gTTS',
        'pynput',
    ],
    entry_points={
        'console_scripts': [
            'discord-voice-bot=main:main',
        ],
    },
    author='Benoit Desrosiers',
    author_email='benoitdesrosiers1980@gmail.com',
    description='A Discord bot that reads text commands and speaks in voice channels.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/benrosiers/A_Discord_Bot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
