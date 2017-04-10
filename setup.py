from setuptools import setup, find_packages

setup(
    name='pongmented-reality',
    version='0.0.1',
    packages=find_packages(),
    license='WTFPL',
    author='matan129, ronissim, tomerli97',
    description='Pong + Kinect = <3',
    install_requires=['pygame', 'logbook', 'numpy', 'pykinect', 'enum34'],
    entry_points={
        'console_scripts': [
            'run_pongmented = pongmented.game:main'
        ]
    }
)
