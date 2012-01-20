from Globals import InitializeClass

from DataSourceBase import DataSourceBase
from ZenPacks.community.ZopeMonitor.config import MUNIN_MEMORY

class ZopeMemoryDataSource(DataSourceBase):
    """Zope Memory"""

    ZOPE_MONITOR = 'ZopeMemoryDataSourceMonitor'

    sourcetypes = ( ZOPE_MONITOR,)
    sourcetype = ZOPE_MONITOR

    meta_type = 'ZopeMemoryDataSource'

    munin_tags = MUNIN_MEMORY

    uri = 'zopememory'

InitializeClass(ZopeMemoryDataSource)