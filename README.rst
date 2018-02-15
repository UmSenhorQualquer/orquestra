sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install mysql-server
sudo apt-get install python-mysql.connector python-mysqldb
sudo apt-get install python-pip
sudo apt-get install git
sudo apt-get install language-pack-pt
sudo pip install simplejson
sudo pip install django==1.10.6
sudo pip install lockfile
sudo pip install sorl-thumbnail
sudo pip install dill
sudo pip install filelock
sudo pip install django-allauth
sudo pip install git+https://github.com/UmSenhorQualquer/pyforms.git
sudo pip install git+https://github.com/UmSenhorQualquer/django-jfu.git
sudo pip install git+https://UmSenhorQualquer@bitbucket.org/UmSenhorQualquer/pyforms-web.git --upgrade
sudo pip install git+https://UmSenhorQualquer@bitbucket.org/UmSenhorQualquer/orquestra.git --upgrade
sudo pip install git+https://UmSenhorQualquer@bitbucket.org/fchampalimaud/funding-opportunities-models.git --upgrade
sudo pip install git+https://UmSenhorQualquer@bitbucket.org/fchampalimaud/funding-opportunities-apps.git --upgrade
cd /var/www/
git clone https://UmSenhorQualquer@bitbucket.org/fchampalimaud/research-core.git


Create file at /etc/apache2/sites-available/[project-name].conf with the content:

Alias /media/ /var/www/[project-name]/media/
Alias /static/ /var/www/[project-name]/static/
WSGIScriptAlias / /var/www/[project-name]/[project-name-settings]/wsgi.py
WSGIPythonPath /var/www/[project-name]
<Directory /var/www/[project-name]>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
<Directory /var/www/[project-name]/static>
	Require all granted
</Directory>
<Directory /var/www/[project-name]/media>
	Require all granted
</Directory>

cd /var/www/[project-name]
python manage.py install_plugins
python manage.py collectstatic
sudo a2ensite [project-name].conf
sudo service restart apache2

