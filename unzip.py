#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import zipfile
import os
import getopt
import shutil

def usage():
    print """usage: unzip.py [-l] <zipfile> [[-e <encoding>] -p <password>]
    <zipfile> is the source zipfile to extract
    <encoding> is the encoding of zipfile
    <password> is the password of zipfile

    -h: help
    -l: list files only
    long options also work:
    --verbose
    --encoding
    --password
    --list 
    """

def get_filename(fileinfo, encoding):
    """
    Return Values:
    	return filename on success or None otherwise
    """
    if encoding == None:
        return fileinfo.filename
    try:
        filename = unicode(fileinfo.filename, encoding)
    except TypeError:
        filename = fileinfo.filename
    except:
        #print "ERROR: unknown encoding (" + encoding + ")"
        filename = None
    return filename
    
def get_zipinfo_unicode(fileinfo, encoding=None):
    assert fileinfo != None
    filename = get_filename(fileinfo, encoding)
    file_size = fileinfo.file_size
    compress_size = fileinfo.compress_size
    crc_value = fileinfo.CRC
    date_time = fileinfo.date_time
    fileinfo_dict = {"filename": filename, "file_size": file_size, "compress_size": compress_size, "datetime": date_time}
    return fileinfo_dict
    pass

def pretty_datetime(datetime):
    return str(datetime[0]).zfill(2) + "-" + str(datetime[1]).zfill(2) + "-" + str(datetime[2]).zfill(2) + " " + str(datetime[3]).zfill(2) + ":" + str(datetime[4]).zfill(2) + ":" + str(datetime[5]).zfill(2)
    
ZIPINFO_DESC = "{:>10}  {:>10}  {:>10}  FILE_NAME".format("Compressed", "Real", "Datetime")
    
def zipinfo_prettify(fileinfo, encoding=None):
    infos = get_zipinfo_unicode(fileinfo, encoding)
    keys = ['filename', 'compress_size', 'file_size', 'datetime']
    info_str = ''
    for key in keys[1:]:
        if key == 'datetime':
            s = pretty_datetime(infos[key])
        else:
            s = str(infos[key])
        info_str += "{:>10}  ".format(s)
    info_unicode = info_str
    info_unicode = unicode(info_str, "ascii") + unicode("\t", "ascii") + infos['filename']
    return info_unicode

def main():
    shortargs = 'hel:p:'
    longargs = ['help', 'encoding=', 'password=', 'list']

    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    try:
        if sys.argv[1].startswith('-'):
            opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
            zipsource = ''.join(sys.argv[-1:])
        else:
            opts, args = getopt.getopt(sys.argv[2:], shortargs, longargs)
            zipsource = sys.argv[1]
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    encoding = 'cp950'
    password = None
    list_file = False

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-e", "--encoding"):
            encoding = a
        if o in ("-p", "--password"):
            password = a
        if o in ("-l", "--list"):
            list_file = True
    try:
        f = zipfile.ZipFile(zipsource, 'r')
    except zipfile.BadZipfile:
        print "ERROR: File is broken zip or not a zip file"
        sys.exit(2)

    if password != None:
        f.setpassword(password)

    if list_file:
        print ZIPINFO_DESC
    for fileinfo in f.infolist():
        filename = get_filename(fileinfo, encoding)
        if filename == None:
            print "ERROR: unknown encoding (" + encoding + ")"
            sys.exit(2)
        if list_file:
            #print filename
            print zipinfo_prettify(fileinfo, encoding)
        else:
            if filename.endswith('/'):
                if not os.path.isdir(filename):
                    os.mkdir(filename)
                    print "Create : " + filename
                else:
                    outputfile = open(filename, "wb")
                    try:
                        shutil.copyfileobj(f.open(fileinfo.filename), outputfile)
                    except:
                        print "ERROR: File is encrypted, password required for extraction (-p, --password)"
                        sys.exit(2)
                print "Extract: " + filename

if __name__ == '__main__': main()

