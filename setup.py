from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='lootgenerator',
      version='0.2.0',
      description='Tabletop RPG loot generator',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Utilities'
      ],
      keywords='rpg loot',
      url='http://github.com/tengro/lootgenerator',
      author='Andrew Liashchuk',
      author_email='tengro@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
