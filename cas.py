#!/usr/bin/python

"""
Content Addressed Storage using sha256 hashes

This module creates a data store in the filesystem at a path you
specify, and stores whatever values or files you want in it, using
sha256 hashes to identify them.
"""

import os
import shutil
import hashlib

class StoreNotValidException(Exception):
    """Raised when an invalid store is encountered and not fixable"""
    pass

class CAS:

    """
    Implements Content Addressed Storage.
    """

    def __init__(self, storepath, create=True, force=False ):
        """Instantiates a CAS store.

        You must provide a path to the place in the filesystem where the data are to be stored.  

        Optionally, you may specify create (default True) which will
        cause __init__() to create and/or modify the specified
        docstore path to make it usable as a store.

        Optionally, you may specify force (default False), which will
        cause __init__() to delete whatever (if anything) is at the
        existing store path before creating the store.  Note that this
        will delete any data in the store path, regardless of whether
        or not it is part of a valid data store.

        """

        self.storepath = storepath

        #If create is false, the store must already exist at the path.
        #An exception will be thrown if not.
                                                                                        
        #If create is true and force is false, we will create the
        #store if it is not there and an exception will be thrown if
        #there is anything in the way.

        #If both are true, any object located at storepath will be
        #deleted.

        valid = self.isvalidstore()

        if (create and force):
            self.clear()
        if (create and not valid):
            self.buildstruct()
        if (not create and not valid):
            raise StoreNotValidException()
        
    def isvalidstore(self):
        """Confirms that the store path is valid.  Returns True if it is.

        Tests to see that the path exists, is a folder, and contans
        256 folders numbered in hex from 00 through ff.  Returns True
        if all of these conditions are met, False otherwise.

        """

        if (not os.path.exists(self.storepath)):
            return False
        if (not os.path.isdir(self.storepath)):
            return False
        for i in range(0, 256):
            subdir = format(i, "02x")
            if (not os.path.exists(os.path.join(self.storepath, subdir))):
                return False
            if (not os.path.isdir(os.path.join(self.storepath, subdir))):
                return False
        return True
    
    def clear(self):
        """Deletes anything found at the store path."""

        #Simply does a recursive delete of self.storepath if it exists.
        if (os.path.exists(self.storepath)):
            if (os.path.isdir(self.storepath)):
                shutil.rmtree(self.storepath)
            else:
                os.path.unlink(self.storepath)

    def buildstruct (self):
        """Creates all of the structures expected in the data store."""

        for i in range(0, 256):
            subdir = format(i, "02x")
            os.makedirs(os.path.join(self.storepath, subdir))

    def putblob(self, blob):
        """Places a blob in the store and returns its key.

        Given a blob, this will calculate its hash and, if needed,
        copy the object into the store.  It will return the hash.

        """

        digest = hashlib.sha256()
        digest.update(blob)
        key = digest.hexdigest()
        objpath = os.path.join(self.storepath, key[:2], key)

        if (not os.path.exists(objpath)):
            with open(objpath, "w") as fh:
                fh.write(blob)

        return key

    def getblob(self, key):
        """Takes a key and returns the content.  Returns None if the key
        isn't in the store."""
        
        if (self.exists(key)):
            objpath = os.path.join(self.storepath, key[:2], key)
            with open(objpath, "r") as fh:
                result = fh.read()
            return result
        return None

    def putfile(self, filepath, key = None):
        """Takes a filepath and optional key, and puts the file into the
        store.  Returns the hash.

        If there is a matching key in the store already, the copy is not performed.

        If a key is provided, the hashing step is skipped.

        """

        if (key is None):
            key = self.hashfile(filepath)
        
        objpath = os.path.join(self.storepath, key[:2], key)
        shutil.copyfile(filepath, objpath)

        return key

    def getfile(self, key, filepath):
        """Retrieves content to a file.

        Takes a hash and a filepath.  Copies the content from the store to
        the specified filepath.  Returns True if the key was found,
        False if not.

        """
        if (not self.exists(key)):
            return False
        objpath = os.path.join(self.storepath, key[:2], key)
        shutil.copyfile(objpath, filepath)
        return True

    def hashfile(self, filepath):
        """#Takes a filepath and returns the hash.  Returns None if it isn't there.

        This is largely intended as a utility for the other methods in this class.

        """

        blocksize = 1048576
        
        if ((not os.path.exists(filepath)) or (not os.path.isfile(filepath))):
            return None
        
        digest = hashlib.sha256()
        with open(filepath, "rb") as fh:
            block = fh.read(blocksize)
            while (len(block) > 0):
                digest.update(block)
                block = fh.read(blocksize)
        return digest.hexdigest()
        
    def isvalidkey(self, key):
        """Takes a key and confirms that the object stored under that key
        correctly hashes to that key.

        Returns True if it does, False if not, None if the key is not
        in the store.

        """
        
        objpath = os.path.join(self.storepath, key[:2], key)
        testkey = self.hashfile(objpath)
        if (testkey == key):
            return True
        return False
        
    def getkeysize (self, key):
        """Takes a key and returns the size of the stored object.

        Returns None if the key is absent, because this is a distinct
        condition from a zero-length key.

        """
        
        objpath = os.path.join(self.storepath, key[:2], key)
        if (not self.exists(key)):
            return None
        return os.path.getsize(objpath)
    
    def removekey(self, key):
        """Deletes the specified key from the data store.  Returns True
        #if successful, False if not."""
        
        if self.exists(key):
            objpath = os.path.join(self.storepath, key[:2], key)
            os.unlink(objpath)
            return True
        return False    

    def exists(self, key):
        """Returns True if key exists in the store, False if not."""
        
        objpath = os.path.join(self.storepath, key[:2], key)
        if ((not os.path.exists(objpath)) or (not os.path.isfile(objpath))):
            return False
        return True

    def changekey (self, oldkey, newkey):
        """Changes the key of an object.  Don't do this."""
        
        oldobjpath = os.path.join(self.storepath, oldkey[:2], oldkey)
        newobjpath = os.path.join(self.storepath, newkey[:2], newkey)
        shutil.move(oldobjpath, newobjpath)
    
    def listkeys (self):
        """Yields all keys from the store"""
        for i in range(0, 256):
            subdir = format(i, '02x')
            for item in os.listdir(os.path.join(self.storepath, subdir)):
                yield item

    def findinvalidkeys(self):
        """Yields all keys that have mismatched content

        Warning: This could take a long time, depending on the size of
        the store and the size of the individual objects in the store.

        """
        
        for key in self.listkeys():
            if (not self.isvalidkey(key)):
                yield key
    
    def correctinvalidkeys(self):
        """Renames any keys that are not valid.  Returns a list of
        tuples consisting of the old and new key values.

        Warning: This could take a long time, depending on the size of
        the store and the size of the individual objects in the store.

        """

        result = []
        for key in self.findinvalidkeys():
            objpath = os.path.join(self.storepath, key[:2], key)
            newkey = self.hashfile(objpath)
            self.changekey(key, newkey)
            result = result + [ (key, newkey) ]
        return result
    
    def removeinvalidkeys(self):
        """Deletes any keys that are not valid.  Returns a list of
        the deleted keys.

        Warning: This could take a long time, depending on the size of
        the store and the size of the individual objects in the store.

        Warning: This deletes data!  It may be destructive.

        """

        result = []
        for key in self.findinvalidkeys():
            self.removekey(key)
            result = result + [key]
        return result
