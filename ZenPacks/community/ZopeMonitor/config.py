PROJECTNAME = "ZenPacks.community.ZopeMonitor"
SKINS_DIR = 'skins'
SKINNAME = PROJECTNAME
GLOBALS = globals()

MUNIN_THREADS = ('total_threads', 'free_threads')
MUNIN_CACHE = ('total_objs', 'total_objs_memory', 'target_number')
MUNIN_ZODB = ('total_load_count', 'total_store_count', 'total_connections')
MUNIN_MEMORY = ('VmPeak', 'VmSize', 'VmLck', 'VmHWM', 'VmRSS', 'VmData', 'VmStk', 'VmExe', 'VmLib', 'VmPTE')