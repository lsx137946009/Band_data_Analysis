#
__docformat__ = 'resreucturedtext'

hard_dependencies = ('numpy', 'pandas')
missing_dependencies = [ ]

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)
        
if missing_dependencies:
    raise ImportError(
    "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from datetime import datetime

# TODO: add import
import sensorpowa.core.base
import sensorpowa.plotting.core
import sensorpowa.filtering.bandpass
import sensorpowa.filtering.outlier
import sensorpowa.filtering.smooth
import sensorpowa.sliding.slicing
import sensorpowa.timeutils.timepoint
from sensorpowa.core.series import SensorSeries
from sensorpowa.core.frame import SensorFrame

#
from ._version import get_versions
v = get_versions()
__version__ = v.get('closest-tag', v['version'])
__git_version__ = v.get('full-revisionid')
del get_versions, v

# TODO: add modele level doc-string
__doc__ = """
sixing liu, yaru chen
"""