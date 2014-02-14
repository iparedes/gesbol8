__author__ = 'nacho'

import ConfigParser

class ConfigManager():
    def __init__(self,archivo):
        self.config=ConfigParser.ConfigParser()
        self.config.read(archivo)
        self.version=self.ConfigSectionMap("gesbol")['version']
        self.dirxml=self.ConfigSectionMap("gesbol")['dirxml']
        self.plantillaes=self.ConfigSectionMap("gesbol")['plantillaes']
        self.plantillaen=self.ConfigSectionMap("gesbol")['plantillaen']
        self.dirconf=self.ConfigSectionMap("gesbol")['dirconf']
        self.dirhtml=self.ConfigSectionMap("gesbol")['dirhtml']

    def ConfigSectionMap(self,section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
