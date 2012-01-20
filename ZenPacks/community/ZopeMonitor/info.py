from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.community.ZopeMonitor.interfaces import IZopeMonitorDataSourceInfo


class ZopeMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(IZopeMonitorDataSourceInfo)
    timeout = ProxyProperty('timeout')
    cycletime = ProxyProperty('cycletime')
    hostname = ProxyProperty('hostname')
    ipAddress = ProxyProperty('ipAddress')
    port = ProxyProperty('port')
    useSsl = ProxyProperty('useSsl')
    basicAuthUser = ProxyProperty('basicAuthUser')
    basicAuthPass = ProxyProperty('basicAuthPass')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False

