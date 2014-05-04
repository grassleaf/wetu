from data.models import *

class SourceIter:
	"""
	intro:	1.this class is designed to get the next result	in a list of Querysets, ordered by datatime.
			2.the instance of this class is an iterator.
			3.built by zzxx.
	"""
	def delnull(self):
		"""
		intro:	this method is to del None object in lst and con.
				both lst and con are small List instances.
		"""
		i = 0
		j = 0
		ln = len(self.con)
		while i < ln:
			if self.con[i] is not None:
				if i != j:
					self.con[j] = self.con[i]
					self.lst[j] = self.lst[i]
				j += 1
			i += 1
		while i > j:
			self.con.pop()
			slef.lst.pop()
			i -= 1

	def __init__(self, lst):
		"""
		intro:	this class will be built by me, so it's not a problem what should be in lst.
		"""
		self.lst = lst
		self.con = []
		for i in self.lst:	
			try:
				t = i.next()
			except StopIteration:
				t = None
			self.con.append(t)
		self.delnull()

	def next(self):
		"""
		intro:	return the next result from all the Querysets.
				return null if there is no next result.
		"""
		if self.con.__len__() == 0:
			return None
		i = 1
		x = 0
		ln = self.con.__len__()
		#get the lastest among the con, record index to x
		#code missing here !!!
		i = self.con[x]
		try:
			self.con[x] = self.lst[x].next()
		except StopIteration:
			self.con[x] = None
		self.delnull()
		return i

	def __iter__(self):
		"""
		intro:	this method probably means get the iterator.
				but I personally think it is useless. what's your opinion?
				P.S. this mothod must be overrided.
		"""
		return self

def getImageFromLocal(path):
	"""
	intro:	a small method
	input:	the absolute path of an image
	output:	return an instance of ContentFile of the image
	"""
	return ContentFile(open(path, 'rb').read())

def getSlug(ID):
	"""
	intro:	get the slug in string form
	"""
	pre = str(hashlib.md5(str(ID)).hexdigest())
	return pre[:6] + str(int(time.time() * 100))

def isEmailExists(Email):
	"""
	intro:	to check if the email address has been used
	"""
	return User.objects.filter(email = Email).exists()

def createAdmin(Username, Password, Email):
	"""
	intro:	this method is to create an Admin
	input:	Username - a string, the name of the user
			Password - a string, the password inputed by the user
			Email - a string, the email address used by the user
	output:	the instance of User
	notice:	1.I won't check if the email has been used
			2.Just like the 1st, the Username either.
	"""
	user = User.objects.create_user(Username, Email, Password)
	user.is_superuser = True
	user.save()
	return user

def createInfo(Username, Password, Email):
	"""
	intro:	this method is to create an instance of Info in database
			Info is designed for users' information
	input:	Username - a string, the name of the user
			Password - a string, the password inputed by the user
			Email - a string, the email address used by the user
	output:	an instance of Info
	notice:	1.here I won't check if email has already been used
			2.here I will create an new default album
			3.Actually it's necessary to check if the Username has been used,
				but I won't do this job.
	"""
	#create user
	user = User.objects.create_user(Username, Email, Password)

	#create Info
	self = Info(ID_id = user.id)
	self.slug = getSlug(user.id) 
	self.save()

	#create an default album
	createAlbum(
		Owner = user.id,
		Name = DAN,
		Intro = "This is the default album of %s " % Username
	)
	return self

def getAlbumIter(Owner):
	"""
	intro:	get the iterator of the list of instance of albums the Owner has
	input:	Owner - thd id of an instance of Info
	output:	the iterator of the list of albums
	notice:	1.I won't check if the Owner exists
	"""
	return Album.objects.filter(owner_id = Owner).iterator()

def getAlbumNameIter(Owner):
	"""
	intro:	get the iterator of the list of names of albums the Owner has
	input:	Owner - the id of an instance of Info
	output:	the iterator of the list of albums
	notice:	1.I won't check if the Owner exists
	"""
	return Album.objects.values(('name', 'ID_id')).filter(owner_id = Owner).iterator()

def getAlbumIdByName(Owner, Name):
	return Album.objects.filter(owner_id = Owner, name = Name).first().ID.id

def createPhoto(Name, Content, AlbumID, Isorginal = True, Intro = ""):
	"""
	intro:	this method is to create an instance of Image in database
	input:	Name - a string, the name of the image
			Content - the image itself, an instance of ContentFile
			AlbumID - the id of the album which this image belongs to
			Isorginal - is the image created by the owner
			Intro - a string introducing what the image is like
	output:	an instance of the Image
	notice: 1.I won't check if the album exists
			2.I will save the image into the picture server
			3.I don't care if the instance of the image is null
			4.the name of the image should has a suffix, otherwise Thumb won't work
	"""
	#create Obj
	p = Obj()
	p.save()
	#create Photo
	self = Photo(objID_id = p.id)
	self.name = Name
	t =  Name.rfind(".")
	self.suffix = Name[t:]
	self.intro = Intro
	self.isorginal = Isorginal
	self.date = datetime.datetime.now()
	self.slug = getSlug(p.id) 
	self.inalbum = Album.objects.get(ID_id = AlbumID)
	self.image.save(self.slug + self.suffix, Content)
	self.save()
	return self

def createAlbum(Owner, Name, Intro = ""):
	"""
	intro:	this method is to create an instance of Album in database
	input:	Owner - the id of an instrance of Info
			Name - a string representing the name of the album
			Intro - a string introducing what the album is like
	output:	an instance of Album
	notice:	1.I won't check if the name has been used before
	"""
	#build Obj
	p = Obj()
	p.save()
	#build Album
	self = Album(ID_id = p.id, owner_id = Owner)
	self.date = datetime.datetime.now()
	self.slug = getSlug(p.id) 
	self.name = Name
	self.intro = Intro
	self.save()
	return self

def getInfo(Id):
	"""
	"""
	return Info.objects.select_related().filter(ID__id = Id);