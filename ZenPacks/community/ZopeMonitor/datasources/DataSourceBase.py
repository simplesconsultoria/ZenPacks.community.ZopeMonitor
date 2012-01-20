import Products.ZenModel.RRDDataSource as RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.Utils import binPath

class DataSourceBase(ZenPackPersistence, RRDDataSource.RRDDataSource):
    """
    This base class needs instantiations with munin_plugins, and uri
    attributes
    """

    ZENPACKID = 'ZenPacks.community.ZopeMonitor'

    eventClass = '/Status/Zope'

    hostname = '${dev/id}'
    ipAddress = '${dev/manageIp}'
    port = 8080
    useSsl= False
    basicAuthUser = ''
    basicAuthPass = ''
    timeout = 60

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id': 'hostname', 'type': 'string', 'mode': 'w'},
        {'id': 'ipAddress', 'type': 'string', 'mode': 'w'},
        {'id': 'port', 'type': 'int', 'mode': 'w'},
        {'id': 'useSsl', 'type': 'boolean', 'mode': 'w'},
        {'id': 'basicAuthUser', 'type': 'string', 'mode': 'w'},
        {'id': 'basicAuthPass', 'type': 'string', 'mode': 'w'},
        {'id': 'timeout', 'type': 'int', 'mode': 'w'},
        )

    _relations = RRDDataSource.RRDDataSource._relations + (
    )

    factory_type_information = (
            {'immediate_view' : 'editZopeMonitorDataSource',
             'actions'        :
                (
                    { 'id'            : 'edit',
                      'name'          : 'Data Source',
                      'action'        : 'editZopeMonitorDataSource',
                      'permissions'   : ( Permissions.view, ),
                    },
                )
            },
        )

    security = ClassSecurityInfo()

    def __init__(self, id, title=None, buildRelations=True):
        RRDDataSource.RRDDataSource.__init__(self, id, title, buildRelations)

    def getDescription(self):
        if self.sourcetype == self.ZOPE_MONITOR:
            return self.hostname
        return RRDDataSource.RRDDataSource.getDescription(self)

    def useZenCommand(self):
        return True

    def getCommand(self, context):
        parts = [binPath('check_munin.py')]
        parts.append('-U %s' % self.uri)
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.ipAddress:
            parts.append('-I %s' % self.ipAddress)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.timeout:
            parts.append('-t %s' % self.timeout)
        if self.useSsl:
            parts.append('-S')
        if self.basicAuthUser or self.basicAuthPass:
            parts.append('-a %s:%s' % (self.basicAuthUser, self.basicAuthPass))
        cmd = ' '.join(parts)
        cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        for tag in self.munin_tags:
            if not hasattr(self.datapoints, tag):
                self.manage_addRRDDataPoint(tag)

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return RRDDataSource.RRDDataSource.zmanage_editProperties(self,
                REQUEST)
