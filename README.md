# CAS

Content Addressed Storage using sha256 hashes

## What?

This module creates a data store in the filesystem at a path you
specify, and stores whatever values or files you want in it, using
sha256 hashes to identify them.

## Why?

I need it for another project I want to do.  I have a deduplicating
backup program that uses a file store of the same format, and I am now
rewriting it to make it cleaner.  This module will be used to drive
the filestore rather than implementing in internally.

## How?

### Instantiating the store

    cas = cas.CAS(storepath, create = True, force = False)

storepath is the path to the store on the filesystem.

create (default True) can be set to False if you want the module to
leave the contents of the storepath undisturbed if it's not a valid
store.

force (default False) will erase whatever is at the storepath and
recreate it as an empty store.

### Adding things to the store

    key = cas.putblob(blob)

blob contains any string or binary data you would like to add to the
store.  The return value is the sha256 hash of the data and can be
used to retrieve it later.

    key = cas.putfile('/path/to/file')

This puts an entire file into the store.  Be aware that the file path
and metadata are not preserved.  The return value is the sha256 hash
of the file and can be used to retrieve it later.

### Retrieving things from the store

    blob = cas.getblob(key)

Retrieves the given key and returns the data.  Returns None if the key
isn't found.

    success = cas.getfile(key, 'path/to/file')

Retrieves the given key and writes it to the given file.  Returns True
if it was able to do so, false if not.

### List keys

    for key in cas.listkeys():
    	print key

listkeys is a generator that retrieves a list all of the keys in use.

### Deletion

    success = cas.removekey(key)

Removes the given key from the store.  Returns True if it was there,
False if not.

### Tests

    exists = cas.exists(key)

Returns True if the given key exists in the store, False otherwise.

    valid = cas.isvalidkey(key)

Tests to see if the key matches the content stored under it.

    valid = cas.validstore(key)

Tests to see if the storepath contains a valid store

### Administration

    for key in cas.findinvalidkeys():
    	print key

findinvalidkeys tests all of the keys in the store and returns a list
of those that are not valid.  Warning: this could take a long time.

    for old,new in cas.correctinvalidkeys():
    	print old, "changed to", new

correctinvalidkeys will find all of the invalid keys and move them to
their correct hashes.  Warning, this could take a long time.  Returns
a list of tuples, containing the incorrect key, and the key it was
corrected to.

    for key in cas.removeinvalidkeys():
    	print "Deleted", key

removeinvalidkeys will find all of the invalid keys and delete them.
Warning: this could take a long time, and is destructive.  Returns a
list of deleted keys.

### Things you probably don't need

    cas.clear()

Deletes the store.

    cas.buildstruct()

Creates the structure for a store from a blank space.

    cas.changekey(oldkey, newkey)

Changes the key of an object in the store.  Don't do this.  It's here
because correctinvalidkeys() uses it and so do the unit tests, and
I've listed it here for completenes, but seriously, don't do this.