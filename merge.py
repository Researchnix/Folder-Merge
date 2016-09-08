#!/usr/bin/python
import os
import sys
import time
import re



def findElements(a):
    paths = [a]
    elements = []
    while len(paths) != 0:
        curPath = paths.pop()
        newPaths = findSubPaths(curPath)
        newFiles = findFiles(curPath)
        paths += newPaths
        elements += newPaths + newFiles
    return elements


def findSubPaths(path):
    return [path + x + '/' for x in os.listdir(path) if os.path.isdir(path + x)]

def findFiles(path):
    return [path + x for x in os.listdir(path) if os.path.isfile(path + x)]


def listElements(a):
    for e in findElements(a):
        print e


def compare(a, b, verbose=False):
    elemA = [stringMinus(e, a) for e in findElements(a)]
    elemB = [stringMinus(e, b) for e in findElements(b)]
    both = set([])
    onlyA = []
    onlyB = []
    for e in elemA:
        if e in elemB:
            both.add(e)
        else:
            onlyA.append(e)
    for e in elemB:
        if e in elemA:
            both.add(e)
        else:
            onlyB.append(e)
    both = list(both)
    # Find conflicting files with the same name but different file sizes
    conf = []
    for c  in both:
        if os.stat(a + c)[6] != os.stat(b + c)[6] and os.path.isfile(a + c) and os.path.isfile(b + c):
            conf.append(c)
    for c in conf:
        both.remove(c)
    if verbose:
        print "both      " + str(len(both))
        print "only A    " + str(len(onlyA))
        print "only B    " + str(len(onlyB))
        print "conflicts  " + str(len(conf))
    return [both, onlyA, onlyB, conf]

    
def stringMinus(a, b):
    return a[len(b):]


# Merges A and B into B
def merge(a, b, verbose=False):
    comp = compare(a, b)
    toBeCopied = comp[1]
    conflicts = comp[3]

    toBeCopied.sort()
    for e in toBeCopied:
        if os.path.isdir(a + e):
            preCommand = b + e
            preCommand = preCommand.replace(" ", "\ ")
            command = 'mkdir ' + preCommand
        else:
            command1 = a + e
            command2 = b + e
            command1 = command1.replace(" ", "\ ")
            command2 = command2.replace(" ", "\ ")
            command = 'cp ' + command1 + ' ' + command2
        if verbose:
            print command
        os.system(command)

    for e in conflicts:
        eCopy = copyOf(e)
        command1 = a + e
        command2 = b + eCopy
        command1 = command1.replace(" ", "\ ")
        command2 = command2.replace(" ", "\ ")
        command = 'cp ' + command1 + ' ' + command2
        if verbose:
            print command
        os.system(command)

    comp = compare(a, b, verbose=False)
    if len(comp[1]) == 0 and len(comp[3]) == 0:
        print "Merging was successful!"
    else:
        print "There seems to be some kind of issue"


# We need to assume that this method is only 
# applied to strings not ending with '/', i.e.
# files and not directories.
def copyOf(a):
    pieces = a.split('/')
    last = pieces[-1]
    name = last.split('.')
    if len(name) == 1:
        name[0] = name[0] + '_Copy'
    else:
        name[-2] = name[-2] + '_Copy'
    newLast = '.'.join(name)
    pieces[-1] = newLast
    return '/'.join(pieces)
    


if __name__ == "__main__":
    #t = time.time()

    if not len(sys.argv) == 3:
        sys.exit("Invalid number of arguments")

    a = sys.argv[1]
    b = sys.argv[2]
    comp = compare(a, b, verbose=True)
    if len(comp[1]) == 0 and len(comp[3]) == 0:
        sys.exit("There is nothing to copy")

    while True:
        decision = raw_input("Do you want to merge " + a + " into " + b + " ? (yes/no/conf/onlyA/onlyB): ")
        if not type(decision) == str:
            sys.exit("Not a valid answer")
        elif decision == "conf":
            print comp[3]
        elif decision == "onlyA":
            print comp[1]
        elif decision == "onlyB":
            print comp[2]
        elif decision == "yes":
            merge(a, b)
        elif decision == "no":
            sys.exit("Aborted")
        else:
            sys.exit("Not a valid answer")


    #a = '/Users/lennart/test/'
    #b = '/Users/lennart/testCopy/'

    

    #print "\n\nDone in " + str(time.time() - t) + " s"
