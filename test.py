#!/usr/bin/python

import cas

def checkstorevalid(cas):
    if (cas.isvalidstore()):
        print "The store is valid."
    else:
        print "The store is not valid."


print "Starting up."
cas = cas.CAS('/extraspace/workspace/castest')
checkstorevalid(cas)
print

print "Clearing the store."
cas.clear()
checkstorevalid(cas)
print

print "Building the structures."
cas.buildstruct()
checkstorevalid(cas)
print

print "Instilling a blob."
key1 = cas.putblob("This is a blob.")
print "The key is", key1
print

print "Retrieving the blob."
print "Retrieved blob is:", cas.getblob(key1)
print

print "Instilling a file."
key2 = cas.putfile('test.py')
print "The key is", key2

print "Retrieving the file."
cas.getfile(key2, 'retrievedfile')

print "Checking keys."
if (cas.exists(key1)):
    print "Key 1 exists."
else:
    print "Key 1 does NOT exist."

if (cas.exists(key2)):
    print "Key 2 exists."
else:
    print "Key 2 does NOT exist."

if (cas.isvalidkey(key1)):
    print "Key 1 is valid."
else:
    print "Key 1 is NOT valid."

if (cas.isvalidkey(key2)):
    print "Key 2 is valid."
else:
    print "Key 2 is NOT valid."
print

print "Here are all the keys in the store:"
for key in cas.listkeys():
    print key
print

print "Key sizes:"
print '   ', cas.getkeysize(key1)
print '   ', cas.getkeysize(key2)
print

print "Remove key 1."
cas.removekey(key1)

if (cas.isvalidkey(key1)):
    print "Key 1 is valid."
else:
    print "Key 1 is NOT valid."

if (cas.exists(key1)):
    print "Key 1 exists."
else:
    print "Key 1 does NOT exist."
print

print "Instilling a blob."
key1 = cas.putblob("This is a blob.")
print "The key is", key1
print

print "Moving keys to invalid values"
cas.changekey(key1, '0000000000000000000000000000000000000000000000000000000000000000')
cas.changekey(key2, 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
print "Here are all the keys in the store:"
for key in cas.listkeys():
    print key

if (cas.isvalidkey(key1)):
    print "Key 1 is valid."
else:
    print "Key 1 is NOT valid."
print

print "These keys are invalid:"
for key in cas.findinvalidkeys():
    print key

print
print "Correcting keys."
for (old,new) in cas.correctinvalidkeys():
    print "Moving", old, "to", new



print "Here are all the keys in the store:"
for key in cas.listkeys():
    print key

print "Moving keys to invalid values"
cas.changekey(key1, '0000000000000000000000000000000000000000000000000000000000000000')
cas.changekey(key2, 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
print "Here are all the keys in the store:"
for key in cas.listkeys():
    print key

print
print "Deleting invalid keys"
print cas.removeinvalidkeys()

print "Here are all the keys in the store:"
for key in cas.listkeys():
    print key



