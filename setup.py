from distutils.core import setup


setup(name='ltpageobjects',
        version='0.1',
        description='Liberationtech Page Objects',
        author='Oivvio Polite',
        author_email='oivvio@liberationtech.net',
        url='https://github.com/Liberationtech/ltpageobjects',
        install_requires=['selenium'],
        packages=['ltpageobjects'],
        license="MIT",

        classifiers=(
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT Licenser',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            )
        )
