from setuptools import setup

setup(name='Scheduler',
      version='0.1',
      description='Scheduler for computing project',
      author='Charlie Robinson',
      license='MIT',
      packages=['Scheduler'],
      install_requires=[
        'pyqt5',
        'matplotlib',
        'pony'
      ],
    scripts=['bin/scheduler-gui'],
    test_suite='nose.collector',
    tests_require=['nose'],
    python_requires=">=3.3"
    zip_safe=False)
