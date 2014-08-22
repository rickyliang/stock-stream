try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Richard Liang',
    'url': 'Not yet available.',
    'download_url': 'Not yet available.',
    'author_email': 'Not yet available.',
    'version': '0.1',
    'install_requires': ['nose', 'alembic', 'requests'],
    'packages': ['stream'],
    'scripts': [],
    'name': 'Stock-Stream'
}

setup(**config)