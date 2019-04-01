#!/usr/bin/env python3#!/usr/bin/env python3
import os

# Get the list of existing names
def get_names():
    with open('./face_operations/current_names.txt', 'r') as f:
        names = map(lambda s: s.strip(), f.readlines())

    return list(names)

# Add the name
def add_name(new_name):
    with open('./face_operations/current_names.txt', 'a') as f:
        if os.stat('./face_operations/current_names.txt').st_size == 0:
            f.write(new_name)
        else:
            f.write('\n' + new_name)

# Delete name by replacing it with None
def del_name(name_to_del):
    with open('./face_operations/current_names.txt', 'r+') as f:
        names = f.readlines()
        names = list(map(lambda s: s.strip(), names))
        success = False
        try:
            ind = names.index(name_to_del)
            del names[ind]
            f.seek(0)
            f.truncate()
            for idx, name in enumerate(names):
                if idx != (len(names) - 1):
                    f.write(name+'\n')
                else:
                    f.write(name)

            success = True

        except ValueError:
            success = False

        return success

