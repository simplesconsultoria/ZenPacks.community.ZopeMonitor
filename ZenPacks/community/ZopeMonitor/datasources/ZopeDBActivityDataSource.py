from Globals import InitializeClass

from DataSourceBase import DataSourceBase
from ZenPacks.community.ZopeMonitor.config import MUNIN_ZODB

class ZopeDBActivityDataSource(DataSourceBase):
    """Zope Memory"""

    ZOPE_MONITOR = 'ZopeDBActivityDataSourceMonitor'

    sourcetypes = ( ZOPE_MONITOR,)
    sourcetype = ZOPE_MONITOR

    meta_type = 'ZopeDBActivityDataSource'

    munin_tags = MUNIN_ZODB

    uri = 'zodbactivity'

InitializeClass(ZopeDBActivityDataSource)