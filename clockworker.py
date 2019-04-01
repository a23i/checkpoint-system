#!/usr/bin/env python3
"""
Clear current_names file every day.
"""
import time

start_time = time.time()
day = 60 * 60 * 24

while True:

	# Sleep nearbly dat
	time.sleep(day - 10)

	open('./face_operations/current_names.txt', 'w').close()
	print('[INFO] Current names released (',day,' s past) ')


