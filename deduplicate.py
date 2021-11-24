import os
import sys
from Deduplicator import Deduplicator
from TItem import TItem


def main(dirname):
    filepathes = sorted(map(lambda filename: os.path.join(
        dirname, filename), next(os.walk(dirname), (None, None, []))[2]))
    duplication_groups = Deduplicator.find_duplication_groups_by_hash(
        filepathes)
    for duplication_group in duplication_groups:
        file = TItem(duplication_group[0])
        for duplication in duplication_group[1:]:
            file.tags = file.tags.union(TItem(duplication).tags)
            os.remove(duplication)
        os.rename(file.old(), file.new())


if __name__ == "__main__":
    main(sys.argv[1])
