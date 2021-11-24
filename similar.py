import os
import sys
from ImageDeduplicator import ImageDeduplicator
from TItem import TItem
import shutil
import deduplicate


def main(dirname, to, phash_diff='12', colorhash_diff='2', move='copy', move_type='onedir'):
    if move_type != 'onedir' and move_type != 'muldir':
        print("ERROR: Move type param must be onedir or muldir!")
        return

    if move != 'move' and move != 'copy':
        print("ERROR: Move param must be move or copy!")
        return

    if phash_diff != 'ignore':
        if not int(phash_diff) in range(0, 65):
            print("ERROR: phash_diff must in range [0, 64]!")
            return
        else:
            phash_diff = int(phash_diff)
    else:
        phash_diff = None

    if colorhash_diff != 'ignore':
        if not int(colorhash_diff) in range(0, 13):
            print("ERROR: colorhash_diff must in range [0, 13]!")
            return
        else:
            colorhash_diff = int(colorhash_diff)
    else:
        colorhash_diff = None

    processed = []
    filepathes = sorted(map(lambda filename: os.path.join(
        dirname, filename), next(os.walk(dirname), (None, None, []))[2]))
    similar_groups = ImageDeduplicator.find_similar_images_groups(
        filepathes, 8, phash_diff, colorhash_diff)
    for i, similar_group in enumerate(sorted(similar_groups)):
        for j, filepath in enumerate(sorted(similar_group)):
            if filepath not in processed:
                file = TItem(filepath)
                file.name = "{}_{}__{}".format(i+1, j+1, file.name)
                file.path_to_dir = to
                if move_type == 'muldir':
                    path_to_dir = os.path.join(to, str(i+1))
                    if not os.path.exists(path_to_dir):
                        os.mkdir(path_to_dir)
                    file.path_to_dir = path_to_dir
                if move == 'move':
                    os.rename(file.old(), file.new())
                else:
                    shutil.copyfile(file.old(), file.new())
            processed.append(filepath)
    deduplicate.main(to)
    return


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3],
         sys.argv[4], sys.argv[5], sys.argv[6])
