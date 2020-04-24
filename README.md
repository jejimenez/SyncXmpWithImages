# SyncXmpWithImages
Syncronyze netadata in XMP, JPG, NEF files


This script takes a initial path to search for the xmp files, and take the metadata (subject initially) and syncronice with the related files. Example if the path have DSC_001.xmp, DSC_001.jpg, DSC_001.nef ; it takes the metadata of xmp file to set the same metadata in jpg and nef files which have the same name.

It's ideal to syncronice the files created by lightroom o darktable when editing tags keywords and syncronice these metadata with the revealed image files.

To build: pyinstaller pySidecardXmpSync.py --nowindowed --onefile
