"""
pAPRika
Advanced toolkit for binding free energy calculations
"""

# Make Python 2 and 3 imports work the same
# Safe to remove with Python 3-only code
from __future__ import absolute_import

# Add imports here

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

__all__ = ["setup", "analyze"]

from paprika.setup import Setup
from paprika.analyze import Analyze
setup = Setup
analyze = Analyze
