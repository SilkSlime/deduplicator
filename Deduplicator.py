import os
import hashlib


class Deduplicator:

    def find_duplication_groups_by_hash(filenames):
        sizes = []
        hashes = []

        print("Calculating sizes...")
        for i, filename in enumerate(filenames):
            print("   [{}/{}]        ".format(i+1, len(filenames)), end='\r')
            sizes.append(os.path.getsize(filename))
            hashes.append(None)

        duplication_groups = set()
        for size in sizes:
            duplication_group = Deduplicator.find_list_duplications(
                sizes, size)
            if len(duplication_group) > 1:
                duplication_groups.add(tuple(sorted(duplication_group)))
        duplication_groups = sorted(duplication_groups)
        print("Finded {} duplication groups by size!".format(
            len(duplication_groups)))

        print("Calculating hashes...")
        for idx1, duplication_group in enumerate(duplication_groups):
            for idx2, i in enumerate(duplication_group):
                print("   [{}/{}][{}/{}]        ".format(idx1+1,
                      len(duplication_groups), idx2+1, len(duplication_group)), end='\r')
                if hashes[i] is None:
                    hashes[i] = Deduplicator.md5(filenames[i])

        duplication_groups = set()
        for hash in hashes:
            duplication_group = Deduplicator.find_list_duplications(
                hashes, hash)
            if len(duplication_group) > 1:
                duplication_groups.add(
                    tuple(sorted(map(lambda x: filenames[x], duplication_group))))
        print("Finded {} duplication groups by hash!".format(
            len(duplication_groups)))
        return duplication_groups

    def find_list_duplications(array, item):
        res = []
        for i in range(len(array)):
            if array[i] is not None and item is not None:
                if array[i] == item:
                    res.append(i)
        return res

    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
