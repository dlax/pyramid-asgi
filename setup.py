import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'asgiref',
    'plaster_pastedeploy',
    'pyramid',
    'waitress',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
    'pytest-asyncio',
]

setup(
    name='pyramid_asgi',
    version='0.0',
    description='Pyramid ASGI',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Denis Laxalde',
    author_email='denis.laxalde@logilab.fr',
    url='http://hg.logilab.org/pyramid-asgi',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    python_requires='>=3.5',
    entry_points={
        'paste.app_factory': [
            'main = pyramid_asgi:main',
        ],
    },
)
