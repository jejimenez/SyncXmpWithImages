#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pySidecardXmpSync.py

# Copyright (c) 2012-2014 Jaime Jiménez. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

# This file is part of pySidecardXmpSync.

from __future__ import unicode_literals

import os,  sys, string, argparse

from pyexiftoolsettags import exiftool


MAIN_EXTS = ['xmp','XMP'] # Exts used to identify the file with the metadata which will be copied to the other files
RELATED_EXTS = ['jpg','JPG','jpeg','JPEG','nef','NEF'] # Exts to identidy the files which will be replaced it's metadata with the main file
    
def is_main_file(filename, extensions = MAIN_EXTS):
    return any(filename.endswith(e) for e in extensions)

def is_related_file(filename, mainfilename, root, extensions = RELATED_EXTS):
    return any(filename.endswith(e) and filename.startswith(mainfilename) for e in extensions)

def main(path, recursive):
    et = exiftool.ExifTool("/usr/local/Cellar/exiftool/10.20/bin/exiftool", addedargs=["-overwrite_original"])
    if path is None:
        path = '.'
    # exiftool  -P -overwrite_original_in_place -ProcessingSoftware='pyExifToolGui 0.6' -xmp:Subject="CasaVieja, Granja, Ciudad, bogota" "/Users/jaimeenrrique/Documents/workspace/pysync_sidecard_with_imagefile/20_CCSantaFe/DSC_0405.JPG"

    #with et:
    #    actual_data = et.get_tags(["XMP:Subject"],'/Users/jaimeenrrique/Documents/workspace/pysync_sidecard_with_imagefile/20_CCSantaFe/DSC_0405.NEF.xmp')
    #    print(actual_data)
    
    #with et:
    #    actual_data = et.set_tags({"XMP:Subject":'"nature, ok1, ok2"'},'/Users/jaimeenrrique/Documents/workspace/pysync_sidecard_with_imagefile/20_CCSantaFe/DSC_0405.NEF.xmp')
    #    print(actual_data)
    
    #with et:
    #    actual_data = et.set_keywords(exiftool.KW_REPLACE,["nature", "red plant", "oki1"],'/Users/jaimeenrrique/Documents/workspace/pysync_sidecard_with_imagefile/20_CCSantaFe/DSC_0405.NEF.xmp')
    #    print(actual_data)
    
    cnt = 0
    for root, dirs, files in os.walk(path):
        print(filter(is_main_file, files))
        for filename in filter(is_main_file, files):
            print(str('.....................................'))
            print(str(os.path.join(root, filename)))
            print(os.path.basename(filename).split('.')[0])
            #filefilter = is_related_file(filename, mainfilename, extensions)
            related_files = filter(lambda x: is_related_file(x, os.path.basename(filename).split('.')[0], root), files)
            print(related_files)
            #print(filter(is_related_file, os.path.basename(filename).split('.')[0], files))
            with et:
                actual_data = et.get_tag("XMP:Subject",os.path.join(root, filename))
                if isinstance(actual_data, basestring):
                    actual_data = [actual_data]
                print(actual_data)
                #print(os.path.splitext(os.path.basename(filename))[:1])
                #print(filename.split(".")[-3])
                #print(et.set_keywords(exiftool.KW_REPLACE,actual_data,'"'+str(os.path.join(root, os.path.basename(filename).split('.')[0])+".")+'"*'))
                #print(et.set_keywords(exiftool.KW_REPLACE,actual_data,str(os.path.join(root, os.path.basename(filename).split('.')[0]))))
                cnt = cnt + len(related_files)
                if len(related_files) > 0 :
                    print(et.set_keywords_batch(exiftool.KW_REPLACE,actual_data, [os.path.join(root, x) for x in related_files] ) )
                    print(et.get_tag_batch("XMP:Subject",[os.path.join(root, x) for x in related_files]))
        if not recursive:
            break
    print('modified > '+str(cnt)+' files')
    

#------------------------------------------------------------------------
#------------------------------------------------------------------------
# This is where the main app is started

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process the xmp files of a given path, using them as base to '+
    'get them keywords metadata to be replicated in the jpg, nef files with same name as xmp file in order to '+
    'syncronice the metadata.')
    
    parser.add_argument('path', metavar='Path', type=str, nargs='+',
                        help='Path to be processed. To process the current path just use . character.')
    parser.add_argument('-r', action = 'store_true',
                    help='recursive processing')
    args = parser.parse_args()
    print(args)
    print(os.getcwd())
    path = args.path[0]
    recursive = False
    main(path, recursive)
    
        
