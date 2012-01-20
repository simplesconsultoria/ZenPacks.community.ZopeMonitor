from Globals import InitializeClass

from DataSourceBase import DataSourceBase
from ZenPacks.community.ZopeMonitor.config import MUNIN_THREADS

class ZopeThreadsDataSource(DataSourceBase):
    """Zope Threads"""

    ZOPE_MONITOR = 'ZopeThreadsDataSourceMonitor'

    sourcetypes = ( ZOPE_MONITOR,)
    sourcetype = ZOPE_MONITOR

    meta_type = 'ZopeThreadsDataSource'

    munin_tags = MUNIN_THREADS

    uri = 'zopethreads'

InitializeClass(ZopeThreadsDataSource)