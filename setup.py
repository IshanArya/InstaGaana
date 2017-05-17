from setuptools import setup


setup(name='InstaGaana',
      version='1.3.5',
      description='Instant music downloader for Saavn',
      url='https://github.com/LinuxSDA',
      author='Sumit Dhingra',
      author_email='LinuxSDA@gmail.com',
      license='MIT',
      packages=['InstaGaana'],
      install_requires=[
          'BeautifulSoup4',
          'eyed3>=0.8.0b1',
          'requests',
          'urllib3',
          'wget',
          'pathlib',    # eyeD3 v0.8 dependency, may not install automatically.
      ],
      dependency_links=['https://github.com/nicfit/eyeD3/tarball/master'],
      entry_points={
        "console_scripts": [
            "InstaGaana = InstaGaana.InstaGaana:main"
        ]
      },

      )
