try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Kodistubs',
    version='0.0.1',
    py_modules=[
        'xbmc', 'xbmcaddon', 'xbmcgui', 'xbmcplugin', 'xbmcvfs', 'xbmcdrm'
    ],
    install_requires=['typing'],
    zip_safe=False,
    description='Stub modules that re-create Kodi Python API',
    license='GPLv3',
    keywords="kodi documentation inspection",
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
