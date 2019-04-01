#!/usr/bin/env python3
from face_operations import user_names, current_names, face_recognition, face_add, face_training
import face_operations as fo


"""
This file is wrapper for face_operations package

face_operations package contains:
- face_add.py - add new user face with id
- face_training.py - train classifier with new user faces
- face_recognition.py - executable program

Ones from face_operations will not used directly (only imports)

"""


# Face op class
class FaceOperator:
	"""
	- add_face(string new_name, bool verobose, bool with_video) -
		[Params]
		:new_name: - string - user name
		:verbose (default=True): - bool - if true - print text logs
		:with_video (default=False): - bool - if true - init video logs

		[Description]
		create id for new user,
		take photos,
        	train classifier,
         	add new_name into names file,
        	add name into dict current_names,
        	print logs (if verbose == True)

		[Returns]
        	*no return*

	- del_face(string name_to_del) -
		[Params]
		:name_to_del: - string - user name

		[Description]
		replace name with 'None',
		remove photos from dataset for user with name_to_del

		[Returns]
        	True if successfull (face found -> deleted)
          	False if unsuccessfull (face not found -> terminated)


	- get_names() -
		[Params]
		*no params*

		[Description]
		get names list from names file (all known names)

		[Returns]
        	List of names (ex: ['Alex', 'Artem'])


	- get_current_names() -
		[Params]
		*no params*

		[Description]
		get names of people with indicator = 1


		[Returns]
        	List of names (ex: ['Alex', 'Artem'])
	"""

	@staticmethod
	def add_face(new_name, verbose=True, with_video=False):

		# Use len to get new id
		# Last id was len - 1
		new_id = len(user_names.get_names())

		# Add face to base
		face_add.user_face_add(new_id, with_video, verbose)

		# Train clf
		face_training.train_clf()

		# Add new name
		user_names.add_name(new_name)
		current_names.add_name(new_name)

		# Report
		names = user_names.get_names()
		if verbose:
			print('[INFO] User added with id =  ',new_id,'\n[INFO] Known name list = ',names,'\n[INFO] Length = ',len(names))


	@staticmethod
	def del_face(name_to_del):
		good_del_names = user_names.del_name(name_to_del)
		good_del_curr_names = current_names.del_name(name_to_del)

		return good_del_names, good_del_curr_names


	# Get all known names list
	@staticmethod
	def get_names():
                names = user_names.get_names()
                while 'None' in names:
                    names.remove('None')
                return names

	# Get current names list
	@staticmethod
	def get_current_names():
		return current_names.get_names()
