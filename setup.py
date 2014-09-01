import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
]

tests_require = []

testing_requires =  tests_require + [
    'nose',
    'coverage',
    ]

setup(name='usingnamespace-client',
      version='0.0',
      description='Command line tools for Usingnamespace',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Bert JW Regeer',
      author_email='bertjw@regeer.org',
      url='http://usingnamespace.com/',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='uns.tests',
      install_requires=requires,
      tests_require=tests_require,
      extras_require = {
          'testing': testing_requires,
          },
      entry_points="""\
      [console_scripts]
      uns = uns.client:main
      """,
      )
