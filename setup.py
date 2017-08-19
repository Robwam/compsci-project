from setuptools import setup, find_packages

setup(
  name='Scheduler',
  version='0.1',
  description='Scheduler for computing project',
  author='Charlie Robinson',
  author_email='charlie@begly.co.uk',
  url='',
  license='MIT',
  package_dir = {'': 'src'},
  packages=find_packages('src'),
  install_requires=[
    'pyqt5',
    'matplotlib',
    'pony'
  ],
  python_requires=">=3.3",
  scripts=['bin/scheduler-gui'],
  test_suite='nose.collector',
  tests_require=['nose'],
  zip_safe=False,
  include_package_data=True,
)
