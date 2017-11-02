#!/usr/bin/python

import os
import shutil
import hashlib

class StoreNotValidException(Exception):
    pass

class CAS:
    def __init__(self, storepath, create=True, force=False ):
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
            self.buildstruct
        if (not create and not valid):
            raise StoreNotValidException
        
    def isvalidstore(self):
        #needs to confirm that the folder is present and contains
        #folders for 00-FF.  Return False if any of these conditions
        #is not met, and return True if we get through all of that
        #with no glitches.
        if (not os.path.exists(self.storepath)):
            return False
        if (not os.path.isdir(self.storepath)):
            return False
        for i in range(0, 255):
            subdir = format(i, "02x")
            if (not os.path.exists(os.path.join(self.storepath, subdir))):
                return False
            if (not os.path.isdir(os.path.join(self.storepath, subdir))):
                return False
        return True
    
    def clear(self):
        #Simply does a recursive delete of self.storepath if it exists.
        if (os.path.exists(self.storepath)):
            if (os.path.isdir(self.storepath)):
                shutil.rmtree(self.storepath)
            else:
                os.path.unlink(self.storepath)

    def buildstruct (self):
        #Creates all folders leading up to and including
        #self.storepath, then creates folders for 00-FF under that.
        for i in range(0, 255):
            subdir = format(i, "02x")
            os.makedirs(os.path.join(self.storepath, subdir))

    def putblob(self, blob):
        #Takes a blob in a variable, computes its hash, and, if there
        #is no object in the store by that hash, writes it to a file
        #in the store.  Returns the hash.
        digest = hashlib.sha256()
        digest.update(blob)
        key = digest.hexdigest()
        objpath = os.path.join(self.storepath, key[:2], key)

        if (not os.path.exists(objpath)):
            with open(objpath, "w") as fh:
                fh.write(blob)

        return key

    def getblob(self, key):
        #Takes a key and loads the content.  Returns None if the key
        #isn't in the store.
        objpath = os.path.join(self.storepath, key[:2], key)
        if (os.path.exists(objpath) and os.path.isfile(objpath)):
            with open(objpath, "r") as fh:
                result = fh.read()

        return result

    def putfile(self, filepath):
        #Takes a filepath, computes the hash of the file there, and,
        #if there is no object in the store by that hash, writes it to
        #the store.  Returns the hash.
        blocksize = 1048576
        
        #Calculate the hash
        key = self.hashfile(filepath)
        
        objpath = os.path.join(self.storepath, key[:2], key)
        shutil.copyfile(filepath, objpath)

        return key

    def getfile(self, key, filepath):
        #Takes a hash and a filepath, and, if the file is found,
        #copies the data from the store into the filepath.  Returns
        #True if the key was found; False if not.
        objpath = os.path.join(self.storepath, key[:2], key)
        if ((not os.path.exists(objpath)) or (not os.path.isfile(objpath))):
            return False

        shutil.copyfile(objpath, filepath)
        return True

    def hashfile(self, filepath):
        #Takes a filepath and returns the hash.  Returns None if it isn't there.
        if ((not os.path.exists(filepath)) or (not os.path.isfile(filepath))):
            return None
        
        digest = hashlib.sha256()
        with open(filepath, "r") as fh:
            block = fh.read(blocksize)
            while (len(block) > 0):
                digest.update(block)
                block = fh.read(blocksize)
        return digest.hexdigest()
        
    def isvalidkey(self, key):
        #Takes a hash and attempts to validate that the data held
        #under that hash actually hashes out to that value.  Returns
        #True if so, False if not, or None if the key is not found in
        #the store.
        objpath = os.path.join(self.storepath, key[:2], key)
        testkey = self.hashfile(objpath)
        if (testkey == key):
            return True
        return False
        
    def getkeysize (self, key):
        #Takes a key and returns the size of the stored object.
        #Returns None if the key is absent, because this is a distinct
        #condition from a zero-length key.
        objpath = os.path.join(self.storepath, key[:2], key)
        if ((not os.path.exists(objpath)) or (not os.path.isfile(objpath))):
            return None
        return os.path.getsize(objpath)
    
    def listkeys (self):
        #Yields all keys from the store 
        pass

    def findinvalidkeys(self):
        #Yields all keys that have mismatched content
        pass
    
    def correctinvalidkeys(self):
        #Renames any keys that are not valid.  Yields tuples
        #consisting of the old and new key values.
        pass
    
    def removeinvalidkeys(self):
        #Deletes any keys that are not valid.  Yields a list of delete
        #keys.
        pass

    def removekey(self, key):
        #Deletes the specified key from the data store.  Returns True
        #if successful, False if not.
        pass

    def exists(self, key):
        #Returns True if key exists in the store, False if not.
        pass

    def changekey (self, oldkey, newkey):
        #Changes the key of an object.
        pass
    
