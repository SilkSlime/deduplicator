import re
import os


class TItem:
    def __init__(self, filepath) -> None:
        self.origin = filepath
        self.path_to_dir, filename = os.path.split(self.origin)
        name, self.ext = os.path.splitext(filename)
        self.ext = self.ext.lower()
        self.tags = set(
            map(lambda x: x.lower(), re.findall(r"(?<=\[).*?(?=\])", name)))
        self.name = re.sub(r"(?<=\[).*?(?=\])", "",
                           name).replace('[]', '').strip()

    def add(self, tag) -> None:
        self.tags.add(tag.lower())

    def remove(self, tag) -> None:
        self.tags.discard(tag.lower())

    def remove_all(self, tag) -> None:
        self.tags = set()

    def contains(self, tag) -> bool:
        return tag in self.tags

    def old(self) -> str:
        return self.origin

    def new(self) -> str:
        tags = ''.join(sorted(map(lambda tag: '['+tag+']', self.tags)))
        return os.path.join(self.path_to_dir, self.name+tags+self.ext)
