from setuptools import setup, find_packages

setup(
    name='pillboxtools',
    version='0.2',
    author='Vincent van Gelder',
    author_email='vincent@ixlhosting.nl',
    url='http://ixlhosting.nl/',
    license='Apache Software License',
    packages=['pillbox'],
    include_package_data=True,
    install_requires=["simplejson","requests","Click","bcrypt","tabulate","ansible_vault"],
    entry_points={
        'console_scripts': [
            'turret-op=pillbox.turret_op:cli', 
            'turret-secret=pillbox.turret_secret:cli'
        ]
    }
)
