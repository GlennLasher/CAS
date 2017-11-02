#!/usr/bin/python

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
        #folders for 00-FF.
        pass
    
    def clear(self):
        #Simply does a recursive delete of self.storepath if it exists.
        pass

    def buildstruct (self):
        #Creates all folders leading up to and including
        #self.storepath, then creates folders for 00-FF under that.
        pass
    
    def putblob(self, blob):
        #Takes a blob in a variable, computes its hash, and, if there
        #is no object in the store by that hash, writes it to a file
        #in the store.  Returns the hash.
        pass

    def getblob(self, key):
        #Takes a key and loads the content.  Returns None if the key
        #isn't in the store.
        pass

    def putfile(self, filepath):
        #Takes a filepath, computes the hash of the file there, and,
        #if there is no object in the store by that hash, writes it to
        #the store.  Returns the hash.
        pass

    def getfile(self, key, filepath):
        #Takes a hash and a filepath, and, if the file is found,
        #copies the data from the store into the filepath.  Returns
        #True if the key was found; False if not.
        pass

    def isvalidkey(self, key):
        #Takes a hash and attempts to validate that the data held
        #under that hash actually hashes out to that value.  Returns
        #True if so, False if not, or None if the key is not found in
        #the store.
        pass

    def getkeysize (self, key):
        #Takes a key and returns the size of the stored object.
        pass
    
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
    
