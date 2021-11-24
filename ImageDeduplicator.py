import os
import numpy as np
from PIL import Image
import imagehash


class ImageDeduplicator:

    def find_similar_images_groups(filenames, hash_size=8, phash_diff=12, colorhash_diff=2):
        print("Hash Size:", hash_size)
        print("pHash max diff:", phash_diff)
        print("ColorHash max diff:", colorhash_diff)
        phashes = []
        colorhashes_glob = []
        for filename in filenames:
            colorhashes_glob.append(None)

        if phash_diff is not None:
            print("Calculating phashes...")
            for i, filename in enumerate(filenames):
                print("   [{}/{}]        ".format(i +
                      1, len(filenames)), end='\r')
                phashes.append(ImageDeduplicator.phash(filename))
                colorhashes_glob.append(None)

            similars_groups = set()
            for phash in phashes:
                similars_group = ImageDeduplicator.find_similars(
                    phashes, phash, phash_diff)
                if len(similars_group) > 1:
                    similars_groups.add(tuple(sorted(similars_group)))
            print("Finded {} duplication groups by phash!".format(
                len(similars_groups)))
        else:
            print("Skipping phashes calculation...")
            similars_groups = set()
            similars_groups.add(tuple(range(len(filenames))))

        if colorhash_diff is not None:
            print("Calculating colorhashes...")
            similars_groups_new = set()
            for idx1, similars_group in enumerate(similars_groups):
                colorhashes = []
                for idx2, i in enumerate(similars_group):
                    print("   [{}/{}][{}/{}]        ".format(idx1+1,
                          len(similars_groups), idx2+1, len(similars_group)), end='\r')
                    if colorhashes_glob[i] is None:
                        colorhashes_glob[i] = ImageDeduplicator.colorhash(
                            filenames[i])
                    colorhashes.append(colorhashes_glob[i])

                for colorhash in colorhashes:
                    color_similars_group = ImageDeduplicator.find_similars(
                        colorhashes, colorhash, colorhash_diff)
                    if len(color_similars_group) > 1:
                        similars_groups_new.add(tuple(sorted(map(lambda idx2: filenames[idx2], map(
                            lambda idx: similars_group[idx], color_similars_group)))))

            similars_groups = sorted(similars_groups_new)
            print("Finded {} similars groups by colorhash!".format(
                len(similars_groups)))
        else:
            print("Skipping colorhash calculation...")
            similars_groups = sorted(map(lambda group: sorted(
                map(lambda i: filenames[i], group)), similars_groups))

        return similars_groups

    def phash(filename):
        blocked_exts = [".mp4", ".webm"]
        ext = os.path.splitext(filename)[1].lower()
        if (ext not in blocked_exts):
            with Image.open(filename) as img:
                return imagehash.phash(img)
        return None

    def colorhash(filename):
        blocked_exts = [".mp4", ".webm"]
        ext = os.path.splitext(filename)[1].lower()
        if (ext not in blocked_exts):
            with Image.open(filename) as img:
                return imagehash.colorhash(img)

    def find_similars(hashes, hash, diff=0, colorhash_debug=False):
        res = []
        for i in range(len(hashes)):
            if hashes[i] is not None and hash is not None:
                if colorhash_debug:
                    if hashes[i] - hash <= diff:
                        res.append(i)
                        continue
                if np.count_nonzero(hashes[i].hash != hash.hash) <= diff:
                    res.append(i)
        return res
