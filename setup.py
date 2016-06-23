import os; from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme: README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='orquestra',
	version='0.0',
	packages=find_packages(),
	include_package_data=True,
	license='BSD License',  # example license
	description='A simple Django app to conduct Web-based polls.',
	long_description=README,
	url='https://www.example.com/',
	author='Your Name',
	author_email='yourname@example.com',
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Framework :: Django :: 1.9',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',  # example license
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
	package_data={'orquestra': [
		'static/*.js',
		'static/jquery-ui/*.js',
		'static/jquery-ui/*.css',
		'static/jquery-ui/images/*.png',
		'static/*.css',
		'static/semantic-ui/*.css',
		'static/semantic-ui/*.js',
		'static/semantic-ui/components/*.css',
		'static/semantic-ui/components/*.js',
		'static/semantic-ui/themes/basic/assets/fonts/*.*',
		'static/semantic-ui/themes/default/images/*.png',
		'static/semantic-ui/themes/default/assets/fonts/*.*',
		'templates/*.html',
		'templates/account/*.html',
		'templates/plugins/*.js',		
		]
	},
)