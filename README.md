# Deduplicator v1.0

## deduplicate.py

### Description

Removes all md5 duplicates in selected directory.

### Usage

```
python deduplicate.py [source]
```
`source` - the directory in which the search and removal of duplicates will be performed.

### Usage Example

```
python deduplicate.py .\myimages\
```
## similar.py

### Description

Searches similar images in selected directory.

### Usage

```
python similar.py [source] [destination] [max_content_diff] [max_color_diff] [action] [action_type]
```
`source` - directory where similar images will be searched.
`destination` - directory where found groups of similar images will be copied or moved.
`max_content_diff` - the maximum value of the difference between the content of the images to be defined in one group. Accepted values: `[0-64]` or `ignore`.
`max_color_diff` - the maximum value of the difference between the color of the images to be defined in one group. Accepted values: `[0-12]` or `ignore`.
`action` - action that will be applied to found groups of similar images. Accepted values: `move` or `copy`.
`action_type` - a parameter that determines how exactly the action will be performed. Accepted values: `onedir` - all groups of images will be in one directory or `muldir` - each group of images (duplicates are possible) will be in a separate directory within the specified directory.

### Usage Example

```
python similar.py .\test\ .\_Similar\ 12 2 copy onedir
```