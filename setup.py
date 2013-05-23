#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='pilot-client',
      version=version,
      description="Pilot CLI",
      long_description="""\
Pilot command-line interface utilities""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Lev Shamardin',
      author_email='shamardin@theory.sinp.msu.ru',
      url='https://github.com/grid4hpc/',
      license='Apache',
      packages=find_packages(exclude=["tests", "tests.*", "*.tests"]),
      package_data = {'pilot/client': ['schema/*.js']},
      include_package_data=True,
      zip_safe=False,
      install_requires = ["pytz>=2013a",
                          "M2Crypto>=0.16",
                          ],
      entry_points = {
          'console_scripts': [
              'pilot-job-submit=pilot.cli.job_submit:main',
              'pilot-job-status=pilot.cli.job_status:main',
              'pilot-job-info=pilot.cli.job_info:main',
              'pilot-job-cancel=pilot.cli.job_cancel:main',
              'pilot-job-pause=pilot.cli.job_pause:main',
              'pilot-job-resume=pilot.cli.job_resume:main',
              'pilot-job-matchmake=pilot.cli.job_matchmake:main',
              'pilot-job-generate-rsl=pilot.cli.job_generate_rsl:main',
              'pilot-cancel-my-jobs=pilot.cli.cancel_my_jobs:main',
              'pilot-query-jobs=pilot.cli.query_jobs:main',
              'pilot-task-status=pilot.cli.task_status:main',
              'pilot-uri-helper=pilot.cli.uri_helper:main',
              'pilot-server-version=pilot.cli.server_version:main',
              'pilot-delegation-list=pilot.cli.delegation:list',
              'pilot-delegation-create=pilot.cli.delegation:create',
              'pilot-delegation-update=pilot.cli.delegation:update',
              'pilot-delegation-destroy=pilot.cli.delegation:destroy',
              ],
         },
      tests_require = ["mock", "nose"],
      test_suite="nose.collector",
      )
