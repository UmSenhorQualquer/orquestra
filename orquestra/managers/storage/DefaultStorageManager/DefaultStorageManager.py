import Utils.owncloud as owncloud, os
from django.conf import settings
from opencsp.storagemanagers.RemoteFile import RemoteFile
from django.utils import timezone
import subprocess

def get_thumb(fileinfo, size=32):
	if fileinfo.file_type=='dir': return "/static/icons/folder{0}.png".format(size)

	file_extension = os.path.splitext( fileinfo.path )[1]

	if 	file_extension=='.avi' or \
		file_extension=='.mpg' or \
		file_extension=='.mp4': return '/static/icons/movie%d.png' % size

	if 	file_extension=='.png' or \
		file_extension=='.jpg' or \
		file_extension=='.jpeg':
		return '/static/icons/image%d.png' % size
	
	return '/static/icons/file%d.png' % size




class DefaultStorageManager(object):

	def __init__(self, user): self._user = user
		
	def __login(self):
		self._oc = owncloud.Client(settings.OWNCLOUD_LINK)

		
		self._oc.login(self._user.username, settings.OWNCLOUD_PASSWORD)

	def __logout(self):
		self._oc.logout()

	def __parseFile(self, f):
		fileobj = RemoteFile()
		fileobj.filename 		= f.get_name()
		fileobj.fullpath 		= f.path[:-1] if f.file_type=='dir' else f.path
		fileobj.size 			= int(f.attributes.get('{http://owncloud.org/ns}size', f.attributes.get('{DAV:}getcontentlength', 0) ))
		fileobj.lastmodified 	= f.attributes.get('{DAV:}getlastmodified', None)
		fileobj.type 			= f.file_type
		fileobj.small_thumb 	= get_thumb(f, 32)
		fileobj.big_thumb 		= get_thumb(f, 180)
		fileobj.download_link 	= 'javascript:openFolder("{0}")'.format(fileobj.fullpath) if f.file_type=='dir' else "{0}/index.php/apps/files/ajax/download.php?dir={1}&files={2}".format(settings.OWNCLOUD_LINK, f.get_path(), f.get_name() )
		fileobj.open_link 		= 'javascript:openFolder("{0}")'.format(fileobj.fullpath) if f.file_type=='dir' else "{0}/index.php/apps/files/ajax/download.php?dir={1}&files={2}".format(settings.OWNCLOUD_LINK, f.get_path(), f.get_name() )
		return fileobj

	def put_file_contents(self, remote_path, data):
		self.__login()
		res = self._oc.put_file_contents(remote_path, data)
		self.__logout()
		return res

	def put_file(self, remote_path, local_source_file, **kwargs):
		self.__login()
		res = self._oc.put_file(remote_path, local_source_file, kwargs)
		self.__logout()
		return res

	def get_file_handler(self, path):
		self.__login()
		res = self._oc.get_file_handler(path)
		self.__logout()
		return res

	def delete(self, path):
		self.__login()
		res = self._oc.delete(path)
		self.__logout()
		return res

	def list(self, path):
		self.__login()
		for f in self._oc.list(path):  yield self.__parseFile(f)
		self.__logout()

	def file_info(self, path):
		self.__login()
		res = self.__parseFile( self._oc.file_info(path) )
		self.__logout()
		return res

	def mkdir(self, path):
		self.__login()
		res = self._oc.mkdir(path)
		self.__logout()
		return res

	def public_link(self, path):
		self.__login()
		res = self._oc.share_file_with_link(path)
		self.__logout()
		return res

	def public_download_link(self, path): 
		link = self.public_link(path)
		return "{1}/index.php/s/{0}/download".format(link.token, settings.OWNCLOUD_LINK)
		