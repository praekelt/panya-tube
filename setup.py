from setuptools import setup, find_packages

setup(
    name='panya-tube',
    version='0.0.3',
    description='Panya tube(channel, show, clip) app.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/panya-tube',
    packages = find_packages(),
    dependency_links = [
        'http://praekelt.github.com/public-eggs/',
    ],
    install_requires = [
        'panya',
        'pyffmpeg',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
