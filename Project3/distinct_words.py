import os
import sys
import time

from HashTable import HashTable
from LiteraryFile import LiteraryFile


def count_distinct(filename = None, hash_method=None, SIZE_FACTOR = None):
    available_texts = ["texts/"+x for x in os.listdir('texts/')]
    if filename:
        available_texts = [filename]
    hash_f = "PyHash"
    if hash_method:
        hash_f = hash_method

    files = [LiteraryFile(name) for name in available_texts]
    results = []
    for lf in files:
        exact_counter = set()

        estimated_words = lf.max_number_words()
        hash_structure = HashTable(estimated_words,SIZE_FACTOR,hash_f)
        print(f"File: {lf.filename}, Size Factor {hash_structure.SIZE_FACTOR}")
        print(f"Using Method {hash_f}")
        for normalized_array in lf.read_file():
            [hash_structure.put(key,1) for key in normalized_array]
            [exact_counter.add(key) for key in normalized_array]

        results.append((lf.filename,hash_structure.length(), len(exact_counter)))

    return results


if __name__ == "__main__":
    arguments = sys.argv[1:]
    size_factor = []
    arguments_arr = [None,None,None]
    if "-f" in arguments:
        arguments_arr[0] = arguments[arguments.index("-f")+1]
    if "-s" in arguments:
        arguments_arr[1] = float(arguments[arguments.index("-s")+1])
    if "-hash" in arguments:
        arguments_arr[2] = str(arguments[arguments.index("-hash") + 1])
        if arguments_arr[2] not in ["PyHash","PRHF"]:
            raise Exception(f"Method { arguments_arr[2]} not available, use PyHash or PRHF")

    r = count_distinct(arguments_arr[0],arguments_arr[2],arguments_arr[1])
    for filename,est,exact in r:
        print("File "+filename)
        print(f"Estimated Count {est}")
        print(f"Real Count {exact}")
        print(f"Number of Collisions {exact-est}")
        print("-"*20)
