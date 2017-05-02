from setuptools import setup


setup(name='InstaGaana',
      version='1.1',
      description='Instant music downlaoder for Saavn',
      url='https://github.com/LinuxSDA',
      author='Sumit Dhingra',
      author_email='LinuxSDA@gmail.com',
      license='MIT',
      packages=['InstaGaana'],
      install_requires=[
          'BeautifulSoup4',
          'eyed3',
          'requests',
          'urllib3',
          'wget',
      ],
      entry_points={
        "console_scripts": [
            "InstaGaana = InstaGaana.InstaGaana:main"
        ]
      },

      )
