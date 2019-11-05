# -*- coding: utf-8 -*-

import os
import pytest
import warnings

# the import of dir_util introduces a deprecation warning
# we can't do much about it
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from distutils import dir_util

from tocrify import Mets

@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir

def test_constructor():
    '''
    Test the creation of an empty Mets instance
    '''
    mets = Mets()
    assert(mets.tree is None)

def test_reading_local_file(datadir):
    '''
    Test reading a local mets file
    '''
    f = open(datadir.join('test_mets.xml'))
    mets = Mets.read(f)
    assert(mets.mets is not None)

def test_loading_local_file(datadir):
    '''
    Test loading a local mets file
    '''
    f = open(datadir.join('test_mets.xml'))
    mets = Mets.fromfile(f)
    assert(mets.mets is not None)

def test_data_assignment(subtests, datadir):
    '''
    Test the correct assignment of meta data
    '''
    f = open(datadir.join('test_mets.xml'))
    mets = Mets.read(f)

    with subtests.test("Check main title"):
        assert(mets.get_main_title() == "Geschichte der Mission der evangelischen Brüder unter den Indianern in Nordamerika")
