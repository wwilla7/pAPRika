"""
Tests the restraints utilities.
"""

import unittest
import warnings
import numpy as np
import logging as log
import subprocess as sp
import parmed as pmd
import pytest
import paprika
from paprika.restraints import *

def test_DAT_restraint():
    rest1 = DAT_restraint()
    rest1.continuous_apr = True
    rest1.structure_file = './cb6-but/cb6-but-notcentered.pdb'
    rest1.mask1 = ':CB6@O,O2,O4,O6,O8,O10'
    rest1.mask2 = ':BUT@C*'
    rest1.attach['target'] = 3.0
    rest1.attach['fraction_list'] = [0.00, 0.04, 0.181, 0.496, 1.000]
    rest1.attach['fc_final'] = 5.0
    rest1.pull['fc'] = rest1.attach['fc_final']
    rest1.pull['target_initial'] = rest1.attach['target']
    rest1.pull['target_final'] = 10.0
    rest1.pull['num_windows'] = 11
    rest1.release['target'] = rest1.pull['target_final']
    rest1.release['num_windows'] = len(rest1.attach['fraction_list'])
    rest1.release['fc_initial'] = rest1.attach['fc_final']
    rest1.release['fc_final'] = rest1.attach['fc_final']
    rest1.initialize()

    assert rest1.index1 == [13, 31, 49, 67, 85, 103]
    assert rest1.index2 == [109, 113, 115, 119]
    assert rest1.index3 == None
    assert rest1.index4 == None
    assert rest1.phase['attach']['force_constants'] == [0.0, 0.2, 0.905, 2.48, 5.0]
    assert rest1.phase['attach']['targets'] == [3.0, 3.0, 3.0, 3.0, 3.0]
    assert rest1.phase['pull']['force_constants'] == [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    ### Note, the following two come out as numpy arrays ... not sure if that is bad
    assert np.allclose(rest1.phase['pull']['targets'], np.asarray([3.0, 3.7, 4.4, 5.1, 5.8, 6.5, 7.2, 7.9, 8.6, 9.3, 10.0]))
    assert np.allclose(rest1.phase['release']['force_constants'], np.asarray([5.0, 5.0, 5.0, 5.0, 5.0]))
    assert rest1.phase['release']['targets'] == [10.0, 10.0, 10.0, 10.0, 10.0]
    window_list = create_window_list([rest1])
    assert window_list == ['a000', 'a001', 'a002', 'a003', 'p000', 'p001', 'p002', 'p003', 'p004', 'p005', 'p006', 'p007', 'p008', 'p009', 'p010', 'r000', 'r001', 'r002', 'r003']


    rest2 = DAT_restraint()
    rest2.continuous_apr = False
    rest2.structure_file = './cb6-but/cb6-but-notcentered.pdb'
    rest2.mask1 = ':CB6@O,O2,O4,O6,O8,O10'
    rest2.mask2 = ':BUT@C*'
    rest2.attach['num_windows'] = 5
    rest2.attach['fc_initial'] = 0.0
    rest2.attach['fc_final'] = 5.0
    rest2.attach['target'] = 3.0
    rest2.pull['fc'] = rest1.attach['fc_final']
    rest2.pull['target_final'] = 10.0
    rest2.pull['num_windows'] = 11
    rest2.release['fc_increment'] = 1.0
    rest2.release['fc_initial'] = 0.0
    rest2.release['fc_final'] = 5.0
    rest2.initialize()

    assert rest2.index1 == [13, 31, 49, 67, 85, 103]
    assert rest2.index2 == [109, 113, 115, 119]
    assert rest2.index3 == None
    assert rest2.index4 == None
    assert np.allclose(rest2.phase['attach']['force_constants'], np.asarray([0.,1.25,2.5,3.75,5.]))
    assert rest2.phase['attach']['targets'] == [3.0, 3.0, 3.0, 3.0, 3.0]
    assert rest2.phase['pull']['force_constants'] == [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    assert np.allclose(rest2.phase['pull']['targets'], np.asarray([3.0, 3.7, 4.4, 5.1, 5.8, 6.5, 7.2, 7.9, 8.6, 9.3, 10.0]))
    assert np.allclose(rest2.phase['release']['force_constants'], np.asarray([0.,1.25,2.5,3.75,5.]))
    assert rest2.phase['release']['targets'] == [10.0, 10.0, 10.0, 10.0, 10.0]
    window_list = create_window_list([rest2])
    assert window_list == ['a000', 'a001', 'a002', 'a003', 'a004', 'p000', 'p001', 'p002', 'p003', 'p004', 'p005', 'p006', 'p007', 'p008', 'p009', 'p010', 'r000', 'r001', 'r002', 'r003', 'r004']


