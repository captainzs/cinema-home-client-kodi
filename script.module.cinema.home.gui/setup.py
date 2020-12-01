try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='CinemaHomeGui',
    version='0.0.1',
    install_requires=['typing'],
    zip_safe=False,
    license='GPLv3',
    keywords="kodi cinema home gui",
    classifiers=[
        'Environment :: Plugins',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
