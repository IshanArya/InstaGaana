from setuptools import setup


setup(name='InstaGaana',
      version='1.0',
      description='Instant music downlaoder for Saavn',
      url='https://github.com/LinuxSDA',
      author='Sumit Dhingra',
      author_email='LinuxSDA@gmail.com',
      license='MIT',
      scripts=['InstaGaana'],
      install_requires=[
          'BeautifulSoup4',
          'eyed3',
          'requests',
          'urllib3',
          'wget',
      ])
