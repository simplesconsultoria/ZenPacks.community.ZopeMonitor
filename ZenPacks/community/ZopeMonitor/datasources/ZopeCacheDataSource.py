from Globals import InitializeClass

from DataSourceBase import DataSourceBase
from ZenPacks.community.ZopeMonitor.config import MUNIN_CACHE

class ZopeCacheDataSource(DataSourceBase):
    """Zope Cache"""

    ZOPE_MONITOR = 'ZopeCacheDataSourceMonitor'

    sourcetypes = ( ZOPE_MONITOR,)
    sourcetype = ZOPE_MONITOR

    meta_type = 'ZopeCacheDataSource'

    munin_tags = MUNIN_CACHE

    uri = 'zopecache'

InitializeClass(ZopeCacheDataSource)