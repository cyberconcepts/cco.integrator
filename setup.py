from setuptools import setup, find_packages
import os

version = '0.1.2'

setup(name='cco.integrator',
      version=version,
      description="actor-based data and application integration",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # https://pypi.org/classifiers
      classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 2 - Pre Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Communications",
        ],
      keywords='',
      author='cyberconcepts.org team',
      author_email='helmutm@cy55.de',
      url='https://www.cyberconcepts.org',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cco'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'aiohttp',
        'pyyaml',
        'mypy',
        'jsonschema',
        #'prance',
        #'strawberry-graphql',
        # -*- Extra requirements: -*-
      ],
      entry_points="""
        [console_scripts]
        dmypy = mypy.dmypy.client:console_entry
        mypy = mypy.__main__:console_entry
        stubgen = mypy.stubgen:main
        jsonschema = jsonschema.cli:main
        # -*- Entry points: -*-
      """,
      )
