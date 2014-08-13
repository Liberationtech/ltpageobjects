from distutils.core import setup

# Requirements
install_requires = [
    'selenium',
]

setup(name='ltpageobjects',
      version='0.1',
      description='Liberationtech Page Objects',
      author='Oivvio Polite',
      author_email='oivvio@liberationtech.net',
      url='https://github.com/Liberationtech/ltpageobjects',
      install_requires=install_requires,
      packages=['ltpageobjects'],
     )
