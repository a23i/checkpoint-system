#!/usr/bin/env python3

from face_operations import current_names, face_recognition


while True:
	detected_name = face_recognition.run()

	if detected_name == 'unknown' or detected_name == 'None':
                print('[INFO] Detected unknonw face. Continue...')
                continue

	# names in current_names file
	names_in_file = current_names.get_names()

	# change indicators
	if detected_name in names_in_file:
		current_names.del_name(detected_name)
		print('[INFO] ',detected_name,' status changed to 0')

	else:
		current_names.add_name(detected_name)
		print('[INFO] ',detected_name,' status changed to 1')


