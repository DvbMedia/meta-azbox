from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.ServiceScan import ServiceScan
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.TuneTest import Tuner
from Components.ConfigList import ConfigListScreen
from Components.ProgressBar import ProgressBar
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.ActionMap import NumberActionMap, ActionMap
from Components.NimManager import nimmanager, getConfigSatlist
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigYesNo, ConfigInteger, getConfigListEntry, ConfigSlider, ConfigEnableDisable
from Tools.HardwareInfo import HardwareInfo
from Tools.Directories import resolveFilename
from enigma import eTimer, eDVBFrontendParametersSatellite, eDVBFrontendParameters, eComponentScan, eDVBSatelliteEquipmentControl, eDVBFrontendParametersTerrestrial, eDVBFrontendParametersCable, eConsoleAppContainer, eDVBResourceManager, getDesktop
import time
from Components.FileList import FileList
import re
import os
import sys
from os import system, listdir, statvfs, popen, makedirs, stat, major, minor, path, access
from Components.AVSwitch import AVSwitch
from Components.SystemInfo import SystemInfo
from Components.Console import Console
import datetime
import os.path
from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List
from enigma import *
from Components.config import configfile, getConfigListEntry, ConfigEnableDisable, ConfigYesNo, ConfigText, ConfigDateTime, ConfigClock, ConfigNumber, ConfigSelectionNumber, ConfigSelection, config, ConfigSubsection, ConfigSubList, ConfigSubDict, ConfigIP, ConfigSlider, ConfigDirectory, ConfigInteger
from os.path import isdir as os_path_isdir
from Components.MenuList import MenuList
from Components.VolumeControl import VolumeControl
config.AZPlay = ConfigSubsection()
config.AZPlay.lastDir = ConfigText(default='/')
config.AZPlay.lastFile = ConfigText(default='None')
config.AZPlay.lastPosition = ConfigText(default='0')
config.AZPlay.ExtSub_Enable = ConfigSelection(choices={'0': _('ON'),
 '1': _('OFF')}, default='0')
config.AZPlay.ExtSub_Size = ConfigSelection(default=50, choices=['30',
 '35',
 '40',
 '45',
 '50',
 '55',
 '60',
 '65',
 '70',
 '75',
 '80',
 '85',
 '90'])
config.AZPlay.ExtSub_Position = ConfigSelection(default='0', choices=['0',
 '10',
 '20',
 '30',
 '40',
 '50',
 '60',
 '70',
 '80',
 '90'])
config.AZPlay.ExtSub_Color = ConfigSelection(choices={'1': _('White'),
 '2': _('Yellow'),
 '3': _('Blue'),
 '4': _('Red'),
 '5': _('Green'),
 '6': _('Orange'),
 '7': _('Blue2'),
 '8': _('Blue3'),
 '9': _('Pink'),
 '0': _('Black')}, default='1')
config.AZPlay.ExtSub_OutColor = ConfigSelection(choices={'1': _('White'),
 '2': _('Yellow'),
 '3': _('Blue'),
 '4': _('Red'),
 '5': _('Green'),
 '6': _('Orange'),
 '7': _('Blue2'),
 '8': _('Blue3'),
 '9': _('Pink'),
 '0': _('Black')}, default='0')
config.AZPlay.ExtSub_Encoding = ConfigSelection(choices={'none': _('None'),
 'windows-1256': _('Arabic'),
 'windows-1257': _('Baltic'),
 'csbig5': _('Chinese'),
 'windows-1251': _('Cyrlic'),
 'windows-1250': _('EastEurope'),
 'windows-1253': _('Greek'),
 'windows-1255': _('Hebrew'),
 'windows-1254': _('Turkish'),
 'windows-1258': _('Vietnamese'),
 'windows-1252': _('WestEurope'),
 'iso-8859-1': _('Spanish (es)')}, default='none')
config.AZPlay.Scaling = ConfigSelection(default='Just Scale', choices=['Just Scale', 'Pan&Scan', 'Pillarbox'])
config.AZPlay.UPnP_Enable = ConfigSelection(choices={'0': _('OFF'),
 '1': _('ON')}, default='0')
path = '/usr/share/fonts/'
cache = {}
try:
    cached_mtime, list = cache[path]
    del cache[path]
except KeyError:
    cached_mtime, list = (-1, [])

mtime = os.stat(path).st_mtime
if mtime != cached_mtime:
    list = os.listdir(path)
    list.sort()
cache[path] = (mtime, list)
n = 0
for fontchk in list:
    if fontchk[len(fontchk) - 3:] != 'ttf':
        del list[n]
    n += 1

scriptliste = list
config.AZPlay.ExtSub_FontSel = ConfigSelection(choices=scriptliste, default='nmsbd.ttf')
AZPlay_SKIN1 = '\n\t<screen position="center,570" size="1220,60" title="" flags="wfNoBorder" backgroundColor="transparent" >\n\t\t<widget name="infoA" position="10,10" zPosition="2" size="1200,45" font="Regular;46" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t<widget name="infoB" position="10,70" zPosition="2" size="1200,45" font="Regular;46" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t<widget name="infoC" position="10,130" zPosition="2" size="1200,45" font="Regular;46" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t<widget name="infoD" position="10,5" zPosition="2" size="700,15" font="Regular;15" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t</screen>'
AZPlay_SKIN2 = '\n\t<screen position="center,390" size="760,200" title="" flags="wfNoBorder" zPosition="-1" >\n\t\t<widget name="pozadina" position="0,0" size="760,200" zPosition="1" />\n\t\t<widget name="media_progress" position="45,150" size="670,15" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/progress_big3.png" backgroundColor="#333333" />\n\t\t<widget name="infoA" position="45,175" zPosition="2" size="150,15" font="Regular;14" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t<widget name="infoB" position="643,175" zPosition="2" size="72,15" font="Regular;14" foregroundColor="#ffffff" transparent="1" halign="right" valign="center" />\n\t\t<widget name="infoC" position="45,42" zPosition="2" size="670,30" font="Regular;26" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t<widget name="infoD" position="45,85" zPosition="2" size="335,25" font="Regular;18" foregroundColor="#aaaaaa" transparent="1" halign="left" valign="center" />\n\t\t<widget name="infoE" position="380,85" zPosition="2" size="335,25" font="Regular;18" foregroundColor="#aaaaaa" transparent="1" halign="right" valign="center" />\n\t\t<widget name="infoF" position="45,118" zPosition="2" size="335,25" font="Regular;18" foregroundColor="#aaaaaa" transparent="1" halign="left" valign="center" />\n\t\t<widget name="infoG" position="380,118" zPosition="2" size="335,25" font="Regular;18" foregroundColor="#aaaaaa" transparent="1" halign="right" valign="center" />\n\t</screen>'
AZPlay_SKIN3 = '\n\t<screen position="center,510" size="1220,180" title="" flags="wfNoBorder" >\n\t\t<widget name="infoA" position="10,10" zPosition="2" size="1200,45" font="Regular;46" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t<widget name="infoB" position="10,70" zPosition="2" size="1200,45" font="Regular;46" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t<widget name="infoC" position="10,130" zPosition="2" size="1200,45" font="Regular;46" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t<widget name="infoD" position="10,5" zPosition="2" size="700,15" font="Regular;15" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t</screen>'

class AZPlayScreen(Screen):
    skin = '\n\t\t<screen position="center,center" size="710,420" title="AZPlay">\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="10,380" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="193,380" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="376,380" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="559,380" size="140,40" alphatest="on" />\n\n\t\t\t<widget source="key_red" render="Label" position="10,380" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" foregroundColor="#ffffff" transparent="1"/>\n\t\t\t<widget source="key_green" render="Label" position="193,380" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" foregroundColor="#ffffff" transparent="1"/>\n\t\t\t<widget source="key_yellow" render="Label" position="376,380" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" foregroundColor="#ffffff" transparent="1"/>\n\t\t\t<widget source="key_blue" render="Label" position="559,380" zPosition="1" size="140,40" font="Regular;14" halign="center" valign="center" backgroundColor="#1f771f" foregroundColor="#ffffff" transparent="1"/>\n\n\t\t\t<widget name="text"\t\tposition="0,5"\tfont="Regular;20" size="710,24"\t halign="center" />\n\t\t\t<widget name="text1"\t\tposition="0,345"\tfont="Regular;16" size="710,24"\t halign="center" />\n\t\t\t<widget name="text2"\t\tposition="0,175"\tfont="Regular;24" size="710,60"\t halign="center" />\n\t\t\t<widget name="start_progress" position="45,150" size="620,15" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/progress_big3.png" backgroundColor="#333333" />\n\t\t\t<widget name="list_left" position="5,35" size="700,295" scrollbarMode="showOnDemand" />\n\t\t</screen>\n\t\t'

    def __init__(self, session):
        if os_path_isdir(config.AZPlay.lastDir.value):
            path_left = config.AZPlay.lastDir.value
        else:
            path_left = '/'
        Screen.__init__(self, session)
        self.Console = Console()
        self.current_service = self.session.nav.getCurrentlyPlayingServiceReference()
        selectable_nims = []
        for nim in nimmanager.nim_slots:
            if nim.config_mode == 'nothing':
                continue
            if nim.config_mode == 'advanced' and len(nimmanager.getSatListForNim(nim.slot)) < 1:
                continue
            if nim.config_mode in ('loopthrough', 'satposdepends'):
                root_id = nimmanager.sec.getRoot(nim.slot_id, int(nim.config.connectedTo.value))
                if nim.type == nimmanager.nim_slots[root_id].type:
                    continue
            if nim.isCompatible('DVB-S'):
                selectable_nims.append((str(nim.slot), nim.friendly_full_description))

        self.select_nim = ConfigSelection(choices=selectable_nims)
        self.feid = 0
        if self.select_nim.value != '':
            self.feid = int(self.select_nim.value)
        self.frontend = self.OpenFrontend()
        if self.frontend is None:
            self.oldref = self.session.nav.getCurrentlyPlayingServiceReference()
            self.session.nav.stopService()
            if not self.frontend:
                if session.pipshown:
                    session.pipshown = False
                    del session.pip
                    if not self.openFrontend():
                        self.frontend = None
        self.session.nav.playService(None)
        try:
            os.system('/etc/init.d/djmount stop &')
            print ' >> STOP UPnP'
        except IOError:
            print 'Error STOP_UPnP'

        os.popen('killall djmount')
        time.sleep(0.1)
        if config.AZPlay.UPnP_Enable.value == '1':
            try:
                os.system('/etc/init.d/djmount start &')
                print ' >> START UPnP'
            except IOError:
                print 'Error START_UPnP'

        self['actions'] = ActionMap(['OkCancelActions',
         'ShortcutActions',
         'ColorActions',
         'MenuActions',
         'DirectionActions'], {'red': self.quit,
         'green': self.keyGo,
         'yellow': self.Konfig,
         'blue': self.keyBlue,
         'up': self.keyUp,
         'down': self.keyDown,
         'ok': self.keyGo,
         'cancel': self.quit,
         'menu': self.Konfig}, -2)
        self['key_red'] = StaticText(_('Exit'))
        self['key_green'] = StaticText(_('Start'))
        self['key_yellow'] = StaticText(_('Menu'))
        self['key_blue'] = StaticText(_('GoTo MediaFolder'))
        self['text'] = Label(_('Select Device :'))
        self['text1'] = Label(_('To SetUp AZPlay - Press the Menu button'))
        self['text2'] = Label(_('Loading...\nPlease Wait'))
        self['start_progress'] = ProgressBar()
        self.TestCounter = 0
        self.cmdV0 = ''
        self.cmdV1 = ''
        self.cmdV2 = ''
        self.cmdV3 = ''
        self.pf_v = []
        self.pf_a = []
        self.pf_p = []
        self.pf_v = ['ts',
         'vob',
         'mpg',
         'mpeg',
         'avi',
         'mkv',
         'dat',
         'iso',
         'img',
         'mp4',
         'divx',
         'm2ts',
         'wmv',
         'flv',
         'mov',
         'mts']
        self.pf_a = ['mp3',
         'ogg',
         'wav',
         'wave',
         'flac',
         'm4a',
         'm3u',
         'pls',
         'e2pls',
         'ac3']
        self.pf_p = ['jpeg',
         'jpg',
         'jpe',
         'png',
         'bmp',
         'gif']
        self.pf_all = 'ts|vob|mpg|mpeg|avi|mkv|dat|iso|img|mp4|divx|m2ts|wmv|flv|mov|mts' + '|' + 'mp3|ogg|wav|wave|flac|m4a|m3u|pls|e2pls|ac3' + '|' + 'jpeg|jpg|jpe|png|bmp|gif'
        self['list_left'] = FileList(path_left, matchingPattern='(?i)^.*\\.(' + self.pf_all + ')', useServiceRef=True, additionalExtensions='4098:ac3 4098:m3u 4098:e2pls 4098:pls')
        self.SOURCELIST = self['list_left']
        self['list_left'].hide()
        self['text'].hide()
        self['text1'].hide()
        self['text2'].show()
        hw_type = HardwareInfo().get_device_name()
        if hw_type == 'minime' or hw_type == 'me':
            self.cmdA = 'rmfp_player -dram 0 -ve 0 -vd 0 -ae 0 -no_disp -prebuf 256 -resetvcxo '
            self.cmdV = 'rmfp_player -dram 0 -ve 0 -vd 0 -ae 0 -no_disp -resetvcxo -subs_res 1080 -forced_font /usr/share/fonts/' + config.AZPlay.ExtSub_FontSel.value + ' '
            self.cmdV0 = 'rmfp_player -dram 0 -ve 0 -vd 0 -ae 0 -no_disp -resetvcxo -no_close -oscaler spu -subs_res 1080 -yuv_palette_subs '
        if hw_type == 'elite' or hw_type == 'premium' or hw_type == 'premium+' or hw_type == 'ultra':
            self.cmdA = 'rmfp_player -dram 1 -ve 1 -vd 0 -ae 0 -no_disp -prebuf 256 -resetvcxo '
            self.cmdV = 'rmfp_player -dram 1 -ve 1 -vd 0 -ae 0 -no_disp -resetvcxo -subs_res 1080 -forced_font /usr/share/fonts/' + config.AZPlay.ExtSub_FontSel.value + ' '
            self.cmdV0 = 'rmfp_player -dram 1 -ve 1 -vd 0 -ae 0 -no_disp -resetvcxo -no_close -oscaler spu -subs_res 1080 -yuv_palette_subs '
        self.cmdV1 = ''
        self.DVBCATimer = eTimer()
        self.DVBCATimer.callback.append(self.Prepare)
        azplay_vctrl = VolumeControl.instance
        self.azplay_currebtvol = azplay_vctrl.volctrl.getVolume()
        self.azplay_ismute = azplay_vctrl.volctrl.isMuted()
        self.onLayoutFinish.append(self.Prepare)

    def Prepare(self):
        self.TestCounter += 1
        self['start_progress'].setValue(self.TestCounter * 4)
        try:
            tmpfile = open('/proc/player', 'rb')
            line = tmpfile.readline()
            tmpfile.close()
        except IOError:
            print 'Error updateMsg'

        if int(line[:-1]) == 1:
            print 'StopService - DONE ! (', self.TestCounter, ')'
            self['start_progress'].setValue(100)
            self.onLayoutFinish.append(self.keyGo)
            self.DVBCATimer1 = eTimer()
            self.DVBCATimer1.callback.append(self.Prepare1)
            self.DVBCATimer1.start(100, True)
        elif self.TestCounter < 49:
            self.DVBCATimer.start(100, True)
        elif int(line[:-1]) != 1:
            self.close()

    def keyBlue(self):
        self['list_left'].changeDir('/media/')
        self['text'].setText('/media/')

    def Prepare1(self):
        self['list_left'].show()
        self['text'].show()
        self['text1'].show()
        self['text2'].hide()
        self['start_progress'].hide()
        open('/proc/player', 'w').write('2')
        self.keyGo()

    def keyDown(self):
        self['list_left'].down()
        self.updateCurrentInfo()

    def keyUp(self):
        self['list_left'].up()
        self.updateCurrentInfo()

    def updateCurrentInfo(self):
        if not self['list_left'].canDescent():
            tmpname = self['list_left'].getFilename()
            ipos = tmpname.rfind('/')
            if ipos > -1:
                self['text'].setText(tmpname[ipos + 1:])

    def keyGo(self):
        self.cmdV2 = '-forced_font /usr/share/fonts/' + config.AZPlay.ExtSub_FontSel.value + ' '
        azplay_vctrl = VolumeControl.instance
        if self.azplay_ismute == False:
            value = self.azplay_currebtvol
            azplay_vctrl.volctrl.setVolume(value, value)
            azplay_vctrl.volSave()
            azplay_vctrl.volumeDialog.setValue(value)
        if not os.path.exists('/tmp/rmfp.cmd'):
            os.popen('mkfifo /tmp/rmfp.cmd')
        if not os.path.exists('/tmp/rmfp.cmd'):
            os.popen('mkfifo /tmp/rmfp.in')
        if not os.path.exists('/tmp/rmfp.cmd'):
            os.popen('mkfifo /tmp/rmfp.out')
        if not os.path.exists('/tmp/rmfp.cmd'):
            os.popen('mkfifo /tmp/rmfp.event')
        if self.SOURCELIST.canDescent():
            self.SOURCELIST.descent()
            if self.SOURCELIST.getCurrentDirectory():
                aaa = self.SOURCELIST.getCurrentDirectory()
                if len(aaa) > 40:
                    aaa = '...' + aaa[len(aaa) - 40:]
                self['text'].setText(aaa)
            else:
                self['text'].setText('Select Device :')
        else:
            fn = self['list_left'].getFilename()
            self.MediaFileName = fn
            ftype = self.onFileAction(fn)
            playfile = self.SOURCELIST.getCurrentDirectory() + fn
            self.MediaFilePath = playfile
            self.MediaFilePath = self['list_left'].getFilename()
            self.MediaFileName = self.MediaFilePath
            ipos = self.MediaFilePath.rfind('/')
            if ipos > -1:
                self.MediaFileName = self.MediaFilePath[ipos + 1:]
            if ftype == 'video':
                self.CheckSubtitle()
            if ftype == 'audio':
                self.PlayAudio(self.MediaFilePath)

    def onFileAction(self, filename):
        for ext in self.pf_v:
            if os.path.splitext(filename)[1][1:] == ext:
                return 'video'

        for ext in self.pf_a:
            if os.path.splitext(filename)[1][1:] == ext:
                return 'audio'

        for ext in self.pf_p:
            if os.path.splitext(filename)[1][1:] == ext:
                return 'picture'

        return 'unknown'

    def SubtitleEnc(self, filename):
        try:
            f = open(filename, 'r').read()
        except Exception:
            return

        enc = config.AZPlay.ExtSub_Encoding.value
        if enc == 'none':
            data = f
            f = open('/tmp/tmp.srt', 'w')
            try:
                f.write(data)
            except Exception as e:
                print e
            finally:
                f.close()

        else:
            try:
                data = f.decode(enc)
            except Exception:
                print 'nok'

            f = open('/tmp/tmp.srt', 'w')
            try:
                f.write(data.encode('utf-8'))
            except Exception as e:
                print e
            finally:
                f.close()

    def CheckSubtitle(self):
        if os.path.exists('/tmp/tmp.srt'):
            os.popen("echo '' > /tmp/tmp.srt")
        ipos = self.MediaFilePath.rfind('.')
        if ipos > -1:
            filenamesub = self.MediaFilePath[:ipos + 1] + 'srt'
        else:
            filenamesub = self.MediaFilePath[:-3] + 'srt'
        if not os.path.exists(filenamesub) and config.AZPlay.ExtSub_Enable.value == '0':
            self.session.openWithCallback(self.ClBackSub, LoadSub, self.SOURCELIST.getCurrentDirectory())
            return
        if os.path.exists(filenamesub) and config.AZPlay.ExtSub_Enable.value == '0':
            self.SubtitleEnc(filenamesub)
            self.cmdV = self.cmdV + '-text_subs /tmp/tmp.srt utf8 '
            self.cmdV3 = '-text_subs /tmp/tmp.srt utf8 '
        if config.AZPlay.ExtSub_Enable.value == '1':
            self.cmdV = self.cmdV + '-nosubs '
            self.cmdV3 = '-nosubs '
        self.PlayVideo(self.MediaFilePath)

    def ClBackSub(self, subtpath):
        if subtpath != 'empty':
            self.SubtitleEnc(subtpath)
            self.cmdV = self.cmdV + '-text_subs /tmp/tmp.srt utf8 '
            self.cmdV3 = '-text_subs /tmp/tmp.srt utf8 '
        else:
            self.cmdV = self.cmdV
            self.cmdV3 = ''
        self.PlayVideo(self.MediaFilePath)

    def PlayAudio(self, filename):
        self.cmd = self.cmdA + "'" + filename + "' &"
        os.popen('killall rmfp_player')
        time.sleep(0.1)
        os.popen(self.cmd)
        time.sleep(2)
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('102\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        self.session.openWithCallback(self.ClBack, HideScr, self.MediaFileName, self.MediaFilePath, 'audio')

    def PlayVideo(self, filename):
        self.cmd = self.cmdV0 + self.cmdV1 + self.cmdV2 + self.cmdV3 + "'" + filename + "' &"
        os.popen('killall rmfp_player')
        time.sleep(0.1)
        os.popen(self.cmd)
        time.sleep(2)
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('102\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        self.session.openWithCallback(self.ClBack, HideScr, self.MediaFileName, self.MediaFilePath, 'video')

    def SendCMD2(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            os.popen('echo ' + str(k1) + ' > /tmp/rmfp.in2;echo ' + str(k2) + ' > /tmp/rmfp.cmd2')
        else:
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            os.popen('echo ' + str(k2) + ' > /tmp/rmfp.cmd2')

    def SendCMD2_old(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            for n in range(0, 8):
                try:
                    f = open('/tmp/rmfp.in2', 'wb')
                    try:
                        f.write(str(k1) + '\n')
                    finally:
                        f.close()

                except Exception as e:
                    print e

                if os.path.exists('/tmp/rmfp.in2'):
                    break
                time.sleep(0.05)

            time.sleep(0.03)
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write(str(k2) + '\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

    def ClBack(self, komanda):
        if komanda == '*Exit*':
            self.quit()

    def quit(self):
        time.sleep(0.1)
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('100\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        hdparm = os.popen('killall rmfp_player')
        time.sleep(0.1)
        open('/proc/player', 'w').write('1')
        time.sleep(0.1)
        self.frontend = None
        self.session.nav.playService(self.current_service)
        time.sleep(0.9)
        if self['list_left'].getCurrentDirectory():
            config.AZPlay.lastDir.value = self['list_left'].getCurrentDirectory()
            config.AZPlay.lastDir.save()
        config.AZPlay.ExtSub_Enable.save()
        config.AZPlay.ExtSub_Size.save()
        config.AZPlay.ExtSub_Position.save()
        config.AZPlay.ExtSub_Color.save()
        config.AZPlay.ExtSub_Encoding.save()
        config.AZPlay.lastPosition.save()
        config.AZPlay.lastFile.save()
        azplay_vctrl = VolumeControl.instance
        if self.azplay_ismute == False:
            value = self.azplay_currebtvol
            azplay_vctrl.volctrl.setVolume(value, value)
            azplay_vctrl.volSave()
            azplay_vctrl.volumeDialog.setValue(value)
        try:
            os.system('/etc/init.d/djmount stop &')
            print ' >> STOP UPnP'
        except IOError:
            print 'Error STOP_UPnP'

        self.close()

    def OpenFrontend(self):
        frontend = None
        resource_manager = eDVBResourceManager.getInstance()
        if resource_manager is None:
            print 'get resource manager instance failed'
        else:
            self.raw_channel = resource_manager.allocateRawChannel(self.feid)
            if self.raw_channel is None:
                print 'allocateRawChannel failed'
            else:
                frontend = self.raw_channel.getFrontend()
                if frontend is None:
                    print 'getFrontend failed'
        return frontend

    def Konfig(self):
        self.session.openWithCallback(self.ClBackCfg, AZPlayConfig)

    def ClBackCfg(self, komanda = None):
        print '-'
        if komanda == 'ok':
            self['list_left'].changeDir('/media/')
            self['text'].setText('/media/')
            self['list_left'].refresh


class HideScr(Screen):
    skin = '\n\t\t<screen position="0,0" size="0,0" title="AZPlay" flags="wfNoBorder" >\n\t\t</screen>'

    def __init__(self, session, ime, pateka, ftype):
        Screen.__init__(self, session)
        self.session = session
        self.MediaFileName = ime
        self.MediaFilePath = pateka
        self.MediaFType = ftype
        self['actions'] = NumberActionMap(['MediaPlayerActions',
         'MediaPlayerSeekActions',
         'InputActions',
         'OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'StandbyActions',
         'MenuActions',
         'MoviePlayerActions'], {'ok': self.ok,
         'cancel': self.exit1,
         'up': self.ZapUp,
         'down': self.ZapDown,
         'left': self.ZapLeft,
         'right': self.ZapRight,
         'nextBouquet': self.ZapUp,
         'prevBouquet': self.ZapDown,
         'power': self.exit2,
         'play': self.keyPlay,
         'stop': self.exit1,
         'previous': self.keyPrev,
         'next': self.keyNext,
         'seekFwd': self.keyFF,
         'seekBack': self.keyREW,
         'menu': self.Konfig,
         'subtitles': self.SubSel,
         'delete': self.SubSel,
         'AudioSelection': self.ALngSel}, -1)
        self.playpause = 102
        self.VCodec = ''
        self.Resol = ''
        self.Format = ''
        self.ACodec = ''
        self.SRate = '48000'
        self.ChNo = ''
        self.FFval = 0
        self.REWval = 0
        self.info1 = 'Play |>'
        self.ALanguages = []
        self.SubtitlesL = []
        self.onLayoutFinish.append(self.keyGo)

    def keyGo(self):
        self.PlayerState = eTimer()
        self.PlayerState.callback.append(self.PlayerStateCheck)
        self.PlayerState.start(100, True)
        self.PlayerGetInfo = eTimer()
        self.PlayerGetInfo.callback.append(self.GetInfo)
        self.PlayerGetInfo.start(3500, True)

    def PlayerStateCheck(self):
        f = os.popen('ps|grep -v ps| grep -v grep| grep rmfp_player')
        Playtmp = f.readlines()
        f.close()
        self.AZP = len(Playtmp)
        if self.AZP == 0:
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            for n in range(0, 8):
                try:
                    f = open('/tmp/rmfp.cmd2', 'wb')
                    try:
                        f.write('100\n')
                    finally:
                        f.close()

                except Exception as e:
                    print e

                if os.path.exists('/tmp/rmfp.cmd2'):
                    break
                time.sleep(0.05)

            self.close('*Stop*')
        self.PlayerState.start(300, True)

    def updateMsg(self):
        self.close()

    def exit2(self):
        self.close('*StandBy*')

    def exit1(self):
        self.GetSec1()
        config.AZPlay.lastPosition.value = str(self.sec1)
        config.AZPlay.lastFile.value = str(self.MediaFileName)
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('100\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        time.sleep(0.15)
        self.close('*Stop*')

    def exit(self):
        self.close('---')

    def ok(self):
        self.ok1(5)

    def ok1(self, vreme):
        info1 = self.info1
        info2 = self.MediaFileName
        info3 = self.GetFileSize(self.MediaFilePath)
        info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
        info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
        self.session.openWithCallback(self.ClBack2, AZInfoBar, 2, info1, info2, info3, info4, info5, vreme, 0, 0, self.MediaFType)

    def GetInfo(self):
        self.ALanguages = []
        self.SubtitlesL = []
        if os.path.exists('/tmp/rmfp.out2'):
            os.remove('/tmp/rmfp.out2')
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('130\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        time.sleep(0.05)
        for n in range(0, 9):
            try:
                tmpfile = open('/tmp/rmfp.out2', 'r')
                lines = tmpfile.readlines()
                tmpfile.close()
                lno = 0
                for line in lines:
                    ipos = line.find('Video stream ID')
                    if ipos >= 0:
                        ipos1 = lines[lno + 1].find('(')
                        ipos2 = lines[lno + 1].find(')')
                        VCodec = lines[lno + 1][ipos1 + 1:ipos2]
                        self.VCodec = VCodec.replace(' ', '')
                        ipos1 = lines[lno + 2].find('Resolution')
                        Resol = lines[lno + 2][ipos1 + 10:-1]
                        self.Resol = Resol.replace(' ', '')
                        ipos1 = lines[lno + 3].find('Format')
                        Format = lines[lno + 3][ipos1 + 6:-1]
                        self.Format = Format.replace(' ', '')
                    ipos = line.find('Audio stream ID')
                    if ipos >= 0:
                        ipos1 = lines[lno + 1].find('(')
                        ipos2 = lines[lno + 1].find(')')
                        ACodec = lines[lno + 1][ipos1 + 1:ipos2]
                        self.ACodec = ACodec.replace(' ', '')
                        ipos1 = lines[lno + 2].find('SampleRate')
                        SRate = lines[lno + 2][ipos1 + 10:-1]
                        self.SRate = SRate.replace(' ', '')
                        ipos1 = lines[lno + 3].find('ChannelNumber')
                        ChNo = lines[lno + 3][ipos1 + 13:-1]
                        self.ChNo = ChNo.replace(' ', '')
                        if self.ChNo == '5':
                            self.ChNo = '5.1'
                    ipos = line.find('Video Streams count:')
                    if ipos >= 0:
                        ino = int(lines[lno][ipos + 20:-1])
                        print 'broj na Video strimovi:', ino
                        for n in range(0, ino):
                            print lines[lno + n + 1][:-1]

                    ipos = line.find('Audio Streams count:')
                    if ipos >= 0:
                        ino = int(lines[lno][ipos + 20:-1])
                        print 'No Of Audio streams:', ino
                        for n in range(0, ino):
                            print lines[lno + n + 1][:-1]
                            tmpstr = lines[lno + n + 1][:-1]
                            ipos = tmpstr.find('ID')
                            if ipos >= 0:
                                tmpstr = ' - ' + tmpstr[ipos:]
                            self.ALanguages.append(tmpstr)

                    ipos = line.find('Subtitles Streams count:')
                    if ipos >= 0:
                        ino = int(lines[lno][ipos + 24:-1])
                        print 'No Of Subtitles streams:', ino
                        for n in range(0, ino):
                            print lines[lno + n + 1][:-1]
                            tmpstr = lines[lno + n + 1][:-1]
                            ipos = tmpstr.find('ID')
                            if ipos >= 0:
                                tmpstr = ' - ' + tmpstr[ipos:]
                            self.SubtitlesL.append(tmpstr)

                    ipos = line.find('Duration:')
                    if ipos >= 0:
                        ino = int(lines[lno][ipos + 9:-3])
                        self.Duration = ino
                    lno += 1

                break
            except Exception:
                print 'Error GetInfo'

            time.sleep(0.1)

        if self.MediaFType != 'video':
            return
        if os.path.exists('/tmp/rmfp.out2'):
            os.remove('/tmp/rmfp.out2')
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        time.sleep(0.05)
        if config.AZPlay.ExtSub_Enable.value == '0':
            self.SendCMD2(config.AZPlay.ExtSub_Size.value, 212)
            time.sleep(0.05)
            self.SendCMD2(config.AZPlay.ExtSub_Position.value, 214)
            time.sleep(0.05)
            self.SendCMD2(config.AZPlay.ExtSub_Color.value, 216)
            time.sleep(0.05)
        cmd = 0
        if config.AZPlay.Scaling.value == 'Just Scale':
            cmd = 223
        if config.AZPlay.Scaling.value == 'Pan&Scan':
            cmd = 224
        if config.AZPlay.Scaling.value == 'Pillarbox':
            cmd = 225
        if cmd > 0:
            self.SendCMD2(-1, cmd)
        if config.AZPlay.lastFile.value == self.MediaFileName:
            self.session.openWithCallback(self.ResumeConfirmed, MessageBox, _('Last position = ' + str(datetime.timedelta(seconds=long(config.AZPlay.lastPosition.value))) + '\n\nResume ?'), timeout=5)

    def ResumeConfirmed(self, yesno):
        if yesno:
            self.GetSec1()
            sec3 = long(config.AZPlay.lastPosition.value)
            if sec3 > 0 and sec3 < self.sec2:
                time.sleep(0.11)
                self.SendCMD2(sec3, 106)
                time.sleep(0.75)
                self.ok1(2)

    def GetFileSize(self, pateka):
        tmp = os.stat(pateka).st_size
        if tmp // 1073741824 > 0:
            info3 = str(tmp // 107374182.4 / 10) + 'GB'
        elif tmp // 1048576 > 0:
            info3 = str(tmp // 104857.6 / 10) + 'MB'
        elif tmp // 1024 > 0:
            info3 = str(tmp // 102.4 / 10) + 'kB'
        else:
            info3 = str(tmp) + 'B'
        return info3

    def ZapRight(self):
        self.GetSec1()
        if self.MediaFType == 'audio':
            x = 10
        if self.MediaFType == 'video':
            x = 60
        sec3 = self.sec1 + x
        if self.sec2 == 0 or self.sec1 == 0:
            return
        if sec3 < self.sec2:
            info1 = self.info1
            info2 = self.MediaFileName
            info3 = self.GetFileSize(self.MediaFilePath)
            info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
            info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
            self.session.openWithCallback(self.ClBack2, AZInfoBar, 1, info1, info2, info3, info4, info5, 0, sec3, self.sec2, self.MediaFType)
        else:
            sec3 = self.sec2

    def ZapLeft(self):
        self.GetSec1()
        if self.MediaFType == 'audio':
            x = 10
        if self.MediaFType == 'video':
            x = 60
        sec3 = self.sec1 - x
        if self.sec2 == 0 or self.sec1 == 0:
            return
        if sec3 > 0:
            info1 = self.info1
            info2 = self.MediaFileName
            info3 = self.GetFileSize(self.MediaFilePath)
            info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
            info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
            self.session.openWithCallback(self.ClBack2, AZInfoBar, 1, info1, info2, info3, info4, info5, 0, sec3, self.sec2, self.MediaFType)
        else:
            sec3 = 0

    def ZapUp(self):
        self.GetSec1()
        if self.MediaFType == 'audio':
            x = 60
        if self.MediaFType == 'video':
            x = 300
        sec3 = self.sec1 + x
        if self.sec2 == 0 or self.sec1 == 0:
            return
        if sec3 < self.sec2:
            info1 = self.info1
            info2 = self.MediaFileName
            info3 = self.GetFileSize(self.MediaFilePath)
            info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
            info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
            self.session.openWithCallback(self.ClBack2, AZInfoBar, 1, info1, info2, info3, info4, info5, 0, sec3, self.sec2, self.MediaFType)
        else:
            sec3 = self.sec2

    def ZapDown(self):
        self.GetSec1()
        if self.MediaFType == 'audio':
            x = 60
        if self.MediaFType == 'video':
            x = 300
        sec3 = self.sec1 - x
        if self.sec2 == 0 or self.sec1 == 0:
            return
        if sec3 > 0:
            info1 = self.info1
            info2 = self.MediaFileName
            info3 = self.GetFileSize(self.MediaFilePath)
            info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
            info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
            self.session.openWithCallback(self.ClBack2, AZInfoBar, 1, info1, info2, info3, info4, info5, 0, sec3, self.sec2, self.MediaFType)
        else:
            sec3 = 0

    def keyPlay(self):
        vreme = 5
        self.FFval = 0
        self.REWval = 0
        if self.playpause == 103:
            self.playpause = 102
            self.info1 = 'Play |>'
        else:
            self.playpause = 103
            self.info1 = 'Paused ||'
        os.popen('echo ' + str(self.playpause) + ' > /tmp/rmfp.cmd2')
        time.sleep(0.05)
        os.popen('echo ' + str(self.playpause) + ' > /tmp/rmfp.cmd2')
        info1 = self.info1
        info2 = self.MediaFileName
        info3 = self.GetFileSize(self.MediaFilePath)
        info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
        info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
        time.sleep(0.11)
        self.session.openWithCallback(self.ClBack2, AZInfoBar, 2, info1, info2, info3, info4, info5, vreme, 0, 0, self.MediaFType)

    def keyStop(self):
        self.playpause = 103
        os.popen('echo 105 > /tmp/rmfp.cmd2')
        time.sleep(0.05)
        os.popen('echo 105 > /tmp/rmfp.cmd2')

    def keyPrev(self):
        self.info1 = 'Play |>'
        self.FFval = 0
        self.GetSec1()
        if self.MediaFType == 'audio':
            x = 10
        if self.MediaFType == 'video':
            x = 60
        sec3 = self.sec1 - x
        if sec3 > 0:
            self.SendCMD2(sec3, 106)
            time.sleep(0.75)
        self.ok1(2)

    def keyNext(self):
        self.info1 = 'Play |>'
        self.FFval = 0
        self.GetSec1()
        if self.MediaFType == 'audio':
            x = 10
        if self.MediaFType == 'video':
            x = 60
        sec3 = self.sec1 + x
        if sec3 < self.sec2:
            self.SendCMD2(sec3, 106)
            time.sleep(0.75)
        self.ok1(2)

    def GetSec1(self):
        if os.path.exists('/tmp/rmfp.out2'):
            os.remove('/tmp/rmfp.out2')
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        self.sec1 = 0
        self.sec2 = 0
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('222\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        time.sleep(0.03)
        for n in range(0, 8):
            try:
                tmpfile = open('/tmp/rmfp.out2', 'r')
                line = tmpfile.readlines()
                tmpfile.close()
                os.remove('/tmp/rmfp.out2')
                self.sec1 = int(line[1]) // 1000
                self.sec2 = int(line[0]) // 1000
                break
            except Exception:
                sec1 = 0

            time.sleep(0.1)

    def keyFF(self):
        if self.MediaFType != 'video':
            return
        vreme = 5
        FFcmd = '102'
        self.REWval = 0
        self.FFval += 1
        if self.FFval == 1:
            FFcmd = '143'
            self.info1 = 'Speed: x 1.2'
        if self.FFval == 2:
            FFcmd = '150'
            self.info1 = 'Speed: x 2.0'
        if self.FFval == 3:
            FFcmd = '109'
            self.info1 = 'Speed: x 4.0'
        if self.FFval == 4:
            FFcmd = '110'
            self.info1 = 'Speed: x 0.5'
        if self.FFval == 5:
            FFcmd = '144'
            self.info1 = 'Speed: x 0.8'
        if self.FFval > 5:
            self.FFval = 0
            FFcmd = '102'
            self.info1 = 'Play |>'
        self.playpause = 103
        cmd = 'echo ' + FFcmd + ' > /tmp/rmfp.cmd2'
        os.popen(cmd)
        time.sleep(0.05)
        os.popen(cmd)
        info1 = self.info1
        info2 = self.MediaFileName
        info3 = self.GetFileSize(self.MediaFilePath)
        info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
        info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
        time.sleep(0.11)
        self.session.openWithCallback(self.ClBack2, AZInfoBar, 2, info1, info2, info3, info4, info5, vreme, 0, 0, self.MediaFType)

    def keyREW(self):
        if self.MediaFType != 'video':
            return
        vreme = 5
        REWcmd = '102'
        self.FFval = 0
        self.REWval += 1
        if self.REWval == 1:
            REWcmd = '144'
            self.info1 = 'Speed: x -0.5'
        if self.REWval == 2:
            REWcmd = '151'
            self.info1 = 'Speed: x -2.0'
        if self.REWval == 3:
            REWcmd = '112'
            self.info1 = 'Speed: x -4.0'
        if self.REWval > 3:
            REWcmd = '102'
            self.info1 = 'Play |>'
            self.REWval = 0
        self.playpause = 103
        cmd = 'echo ' + REWcmd + ' > /tmp/rmfp.cmd2'
        os.popen(cmd)
        time.sleep(0.05)
        os.popen(cmd)
        info1 = self.info1
        info2 = self.MediaFileName
        info3 = self.GetFileSize(self.MediaFilePath)
        info4 = 'Audio: ' + self.ACodec + ' ' + self.ChNo + 'ch ' + str(int(self.SRate) // 1000) + 'kHz'
        info5 = 'Video: ' + self.VCodec + ' ' + self.Resol + ' ' + self.Format
        time.sleep(0.11)
        self.session.openWithCallback(self.ClBack2, AZInfoBar, 2, info1, info2, info3, info4, info5, vreme, 0, 0, self.MediaFType)

    def ClBack2(self, komanda):
        if komanda == '*REW*':
            self.keyREW()
        if komanda == '*FF*':
            self.keyFF()
        if komanda == '*PLAY*':
            self.keyPlay()
        if komanda == '*PREW*':
            self.keyPrev()
        if komanda == '*NEXT*':
            self.keyNext()

    def ClBack(self, komanda):
        self.close('*DirectCh*' + str(komanda))

    def Konfig(self):
        if self.MediaFType != 'video':
            return
        self.session.openWithCallback(self.ClBackCfg, AZPlayConfig, '1')

    def ALngSel(self):
        ino = len(self.ALanguages)
        if self.MediaFType != 'video' or ino < 2:
            return
        self.session.openWithCallback(self.ClBackCfg, AZPlaySelectLang, self.ALanguages)

    def SubSel(self):
        ino = len(self.SubtitlesL)
        if self.MediaFType != 'video' or ino < 2:
            return
        self.session.openWithCallback(self.ClBackCfg, AZPlaySelectSub, self.SubtitlesL)

    def ClBackCfg(self, komanda = None):
        if komanda == 'ok' and self.MediaFType == 'video':
            print 'ClBackCfg - return'

    def SendCMD2(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            cmd = 'echo ' + str(k1) + ' > /tmp/rmfp.in2;echo ' + str(k2) + ' > /tmp/rmfp.cmd2'
            os.popen(cmd)
        else:
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            os.popen('echo ' + str(k2) + ' > /tmp/rmfp.cmd2')

    def SendCMD2_old(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            for n in range(0, 8):
                try:
                    f = open('/tmp/rmfp.in2', 'wb')
                    try:
                        f.write(str(k1) + '\n')
                    finally:
                        f.close()

                except Exception as e:
                    print e

                if os.path.exists('/tmp/rmfp.in2'):
                    break
                time.sleep(0.05)

            time.sleep(0.03)
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write(str(k2) + '\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)


class AZInfoBar(Screen):

    def __init__(self, session, mod, info1, info2, info3, info4, info5, vremetr, vreme1, vreme2, ftype):
        Screen.__init__(self, session)
        self.session = session
        if mod == 1:
            self.skin = AZPlay_SKIN2
        if mod == 2:
            self.skin = AZPlay_SKIN2
        if mod == 3:
            self.skin = AZPlay_SKIN3
        self.IMod = mod
        self.info1 = info1
        self.info2 = info2
        self.info3 = info3
        self.info4 = info4
        self.info5 = info5
        self.vremeT = vremetr
        self.vreme1 = vreme1
        self.vreme2 = vreme2
        self.MediaFType = ftype
        self['actions'] = ActionMap(['MediaPlayerActions',
         'MediaPlayerSeekActions',
         'ChannelSelectBaseActions',
         'WizardActions',
         'DirectionActions',
         'MenuActions',
         'NumberActions',
         'ColorActions'], {'ok': self.ok,
         'back': self.exit,
         'left': self.ZapLeft,
         'right': self.ZapRight,
         'up': self.ZapUp,
         'down': self.ZapDown,
         'play': self.keyPlay,
         'stop': self.keyStop,
         'seekFwd': self.keyFF,
         'seekBack': self.keyREW,
         'previous': self.keyPrev,
         'next': self.keyNext}, -1)
        self.onLayoutFinish.append(self.StartScroll)
        self['infoA'] = Label()
        self['infoB'] = Label()
        self['infoC'] = Label()
        self['infoD'] = Label()
        self['infoE'] = Label()
        self['infoF'] = Label()
        self['infoG'] = Label()
        self['media_progress'] = ProgressBar()
        self['pozadina'] = Pixmap()
        self.msgno = 0
        self['infoA'].setText('0:00:00 / 0:00:00')
        self['infoB'].setText('0:00:00')
        self['infoC'].setText(self.info2)
        self['infoD'].setText(str(self.info4))
        self['infoE'].setText(self.info1)
        self['infoF'].setText(str(self.info5))
        self['infoG'].setText('Size: ' + self.info3)
        self.start_time = time.time()
        self.last_val = 0

    def exit(self):
        self.close('*EXIT*')

    def keyPlay(self):
        self.close('*PLAY*')

    def keyStop(self):
        self.close('*STOP*')

    def keyFF(self):
        self.close('*FF*')

    def keyREW(self):
        self.close('*REW*')

    def keyPrev(self):
        self.close('*PREW*')

    def keyNext(self):
        self.close('*NEXT*')

    def ok(self):
        if self.skok == 1:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            for n in range(0, 8):
                try:
                    f = open('/tmp/rmfp.in2', 'wb')
                    try:
                        f.write(str(self.vreme1) + '\n')
                    finally:
                        f.close()

                except Exception as e:
                    print e

                if os.path.exists('/tmp/rmfp.in2'):
                    break
                time.sleep(0.05)

            time.sleep(0.03)
            for n in range(0, 8):
                try:
                    f = open('/tmp/rmfp.cmd2', 'wb')
                    try:
                        f.write('106\n')
                    finally:
                        f.close()

                except Exception as e:
                    print e

                if os.path.exists('/tmp/rmfp.cmd2'):
                    break
                time.sleep(0.05)

        else:
            self.close('*EXIT*')

    def StartScroll(self):
        self.ExitTimer = eTimer()
        self.ExitTimer.callback.append(self.exit)
        self.ExitTimer.start(5000, True)
        plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/AZPlay'
        self.slikaon = LoadPixmap(plugin_path + '/img/hd.png')
        self['pozadina'].instance.setPixmap(self.slikaon)
        self.skok = 0
        if self.IMod == 1:
            self.skok = 1
            self.pozic = self.vreme1 * 100 // self.vreme2
            self.position = str(datetime.timedelta(seconds=self.vreme1)) + ' / ' + str(datetime.timedelta(seconds=int(self.vreme2 - self.vremeT)))
            self.length = str(datetime.timedelta(seconds=self.vreme2))
            self['media_progress'].setValue(self.pozic)
            self['infoA'].setText(self.position)
            self['infoB'].setText(self.length)
        if self.IMod == 2:
            self.NoLoop = 0
            self.position = '0:00:00 / 0:00:00'
            self.length = '0:00:00'
            self['media_progress'].setValue(0)
            self['infoA'].setText(self.position)
            self['infoB'].setText(self.length)
            self.sec1 = 0
            self.sec2 = 0
            self.pozic = 0
            self.msgTimer = eTimer()
            self.msgTimer.callback.append(self.updateMsg)
            self.msgTimer.start(10, True)
        if self.IMod == 3:
            self.NoLoop = 0
            self.position = '0:00:00 / 0:00:00'
            self.length = '0:00:00'
            self['media_progress'].setValue(0)
            self['infoA'].setText(self.position)
            self['infoB'].setText(self.length)
            self.sec1 = 0
            self.sec2 = 0
            self.pozic = 0
            self.msgTimer = eTimer()
            self.msgTimer.callback.append(self.updateMsg)
            self.msgTimer.start(3000, True)

    def ZapRight(self):
        self.skok = 1
        self.NoLoop = 0
        if self.MediaFType == 'audio':
            x = 10
        if self.MediaFType == 'video':
            x = 60
        self.vreme1 += x
        if self.vreme1 < self.vreme2:
            self.ZapDoThis()
        else:
            self.vreme1 -= 60

    def ZapLeft(self):
        self.skok = 1
        self.NoLoop = 0
        if self.MediaFType == 'audio':
            x = 10
        if self.MediaFType == 'video':
            x = 60
        self.vreme1 -= x
        if self.vreme1 > 0:
            self.ZapDoThis()
        else:
            self.vreme1 += 60

    def ZapUp(self):
        self.skok = 1
        self.NoLoop = 0
        if self.MediaFType == 'audio':
            x = 60
        if self.MediaFType == 'video':
            x = 300
        self.vreme1 += x
        if self.vreme1 < self.vreme2:
            self.ZapDoThis()
        else:
            self.vreme1 -= 300

    def ZapDown(self):
        self.skok = 1
        self.NoLoop = 0
        if self.MediaFType == 'audio':
            x = 60
        if self.MediaFType == 'video':
            x = 300
        self.vreme1 -= x
        if self.vreme1 > 0:
            self.ZapDoThis()
        else:
            self.vreme1 += 300

    def ZapDoThis(self):
        if self.vreme2 > 0:
            self.pozic = self.vreme1 * 100 // self.vreme2
        else:
            self.pozic = 0
            return
        self.position = str(datetime.timedelta(seconds=self.vreme1)) + ' / ' + str(datetime.timedelta(seconds=int(self.vreme2 - self.vreme1)))
        self.length = str(datetime.timedelta(seconds=self.vreme2))
        self['media_progress'].setValue(self.pozic)
        self['infoA'].setText(self.position)
        self['infoB'].setText(self.length)
        self.ExitTimer = eTimer()
        self.ExitTimer.callback.append(self.exit)
        self.ExitTimer.start(5000, True)

    def updateMsg(self):
        if self.skok == 1:
            return
        if os.path.exists('/tmp/rmfp.out2'):
            os.remove('/tmp/rmfp.out2')
        if os.path.exists('/tmp/rmfp.cmd2'):
            os.remove('/tmp/rmfp.cmd2')
        for n in range(0, 8):
            try:
                f = open('/tmp/rmfp.cmd2', 'wb')
                try:
                    f.write('222\n')
                finally:
                    f.close()

            except Exception as e:
                print e

            if os.path.exists('/tmp/rmfp.cmd2'):
                break
            time.sleep(0.05)

        time.sleep(0.03)
        for n in range(0, 8):
            try:
                tmpfile = open('/tmp/rmfp.out2', 'rb')
                line = tmpfile.readlines()
                tmpfile.close()
                os.remove('/tmp/rmfp.out2')
                self.sec1 = int(line[1]) // 1000
                self.sec2 = int(line[0]) // 1000
                self.position = str(datetime.timedelta(seconds=self.sec1)) + ' / ' + str(datetime.timedelta(seconds=int(self.sec2 - self.sec1)))
                self.length = str(datetime.timedelta(seconds=self.sec2))
                break
            except Exception:
                print 'Error updateMsg'

            time.sleep(0.1)

        if self.sec2 > 0:
            self.pozic = self.sec1 * 100 // self.sec2
        self['media_progress'].setValue(self.pozic)
        self['infoA'].setText(self.position)
        self['infoB'].setText(self.length)
        self.NoLoop += 1
        self.vreme1 = self.sec1
        self.vreme2 = self.sec2
        if self.NoLoop < self.vremeT and self.skok == 0:
            self.msgTimer.start(1000, True)
        else:
            self.close('*EXIT*')


class LoadSub(Screen):
    skin = '\n\t\t<screen position="center,center" size="710,390" title="AZPlay - Load Subtitle">\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="10,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="560,350" size="140,40" alphatest="on" />\n\n\t\t\t<widget source="key_red" render="Label" position="10,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" foregroundColor="#ffffff" transparent="1"/>\n\t\t\t<widget source="key_green" render="Label" position="560,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" foregroundColor="#ffffff" transparent="1"/>\n\n\t\t\t<widget name="text"\t\tposition="0,5"\tfont="Regular;20" size="710,24"\t halign="center" />\n\t\t\t<widget name="list_left" position="5,45" size="700,295" scrollbarMode="showOnDemand" />\n\t\t</screen>\n\t\t'

    def __init__(self, session, pateka):
        Screen.__init__(self, session)
        self.session = session
        self.Pateka = pateka
        self['actions'] = ActionMap(['OkCancelActions', 'ShortcutActions', 'ColorActions'], {'red': self.quit,
         'green': self.keyGo,
         'blue': self.keyBlue,
         'ok': self.keyGo,
         'cancel': self.quit}, -2)
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Start'))
        self['text'] = Label(_('Select Device :'))
        path_left = self.Pateka
        self['list_left'] = FileList(path_left, matchingPattern='(?i)^.*\\.(sub|srt)')
        self.SOURCELIST = self['list_left']
        self.onLayoutFinish.append(self.keyGo)

    def keyGo(self):
        if self.SOURCELIST.canDescent():
            self.SOURCELIST.descent()
            if self.SOURCELIST.getCurrentDirectory():
                aaa = self.SOURCELIST.getCurrentDirectory()
                if len(aaa) > 40:
                    aaa = '...' + aaa[len(aaa) - 40:]
                self['text'].setText(aaa)
            else:
                self['text'].setText('Select Device :')
        else:
            fn = self['list_left'].getFilename()
            self.SubFileName = fn
            playfile = self.SOURCELIST.getCurrentDirectory() + fn
            self.SubFilePath = playfile
            if os.path.splitext(fn)[1][1:] == 'srt':
                self.close(playfile)

    def keyBlue(self):
        print 'OK'

    def quit(self):
        self.close('empty')


class AZPlayConfig(ConfigListScreen, Screen):
    skin = '\n\t\t<screen position="center,center" size="710,275" title="AZPlay - Setup" >\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="10,230" size="140,40" transparent="1" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="560,230" size="140,40" transparent="1" alphatest="on" />\n\t\t<widget source="key_red" render="Label" position="10,230" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget source="key_green" render="Label" position="560,230" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget source="poraka" render="Label" position="150,230" zPosition="1" size="400,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="config" position="10,10" size="690,210" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.ActivePlay = args
        self.list = []
        self['actions'] = ActionMap(['ChannelSelectBaseActions',
         'WizardActions',
         'DirectionActions',
         'MenuActions',
         'NumberActions',
         'ColorActions'], {'save': self.SaveCfg,
         'back': self.Izlaz,
         'ok': self.SaveCfg,
         'green': self.SaveCfg,
         'red': self.Izlaz}, -2)
        self['key_red'] = StaticText(_('Exit'))
        self['key_green'] = StaticText(_('Save Conf'))
        self['poraka'] = StaticText(_('AZPlay - Setup'))
        ConfigListScreen.__init__(self, self.list)
        self.ExtSub_Size_old = config.AZPlay.ExtSub_Size.value
        self.ExtSub_Position_old = config.AZPlay.ExtSub_Position.value
        self.ExtSub_Color_old = config.AZPlay.ExtSub_Color.value
        self.Scaling_old = config.AZPlay.Scaling.value
        self.UPnP_Enable_old = config.AZPlay.UPnP_Enable.value
        self.ExtSub_Size_old1 = config.AZPlay.ExtSub_Size.value
        self.ExtSub_Position_old1 = config.AZPlay.ExtSub_Position.value
        self.ExtSub_Color_old1 = config.AZPlay.ExtSub_Color.value
        self.Scaling_old1 = config.AZPlay.Scaling.value
        self.UPnP_Enable_old1 = config.AZPlay.UPnP_Enable.value
        self.createSetup()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createSetup()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createSetup()

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Subtitle Enable:'), config.AZPlay.ExtSub_Enable))
        self.list.append(getConfigListEntry(_('Encoding (After changing, Player must be restarted):'), config.AZPlay.ExtSub_Encoding))
        self.list.append(getConfigListEntry(_('Font Select (After changing, Player must be restarted):'), config.AZPlay.ExtSub_FontSel))
        self.list.append(getConfigListEntry(_('Subtitle Font Size:'), config.AZPlay.ExtSub_Size))
        self.list.append(getConfigListEntry(_('Subtitle Position:'), config.AZPlay.ExtSub_Position))
        self.list.append(getConfigListEntry(_('Subtitle Color:'), config.AZPlay.ExtSub_Color))
        self.list.append(getConfigListEntry(_('Scaling:'), config.AZPlay.Scaling))
        if self.ActivePlay == None:
            self.list.append(getConfigListEntry(_('UPnP Enable:'), config.AZPlay.UPnP_Enable))
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        if self.ExtSub_Size_old != config.AZPlay.ExtSub_Size.value:
            self.SendCMD2(config.AZPlay.ExtSub_Size.value, 212)
        if self.ExtSub_Position_old != config.AZPlay.ExtSub_Position.value:
            self.SendCMD2(config.AZPlay.ExtSub_Position.value, 214)
        if self.ExtSub_Color_old != config.AZPlay.ExtSub_Color.value:
            self.SendCMD2(config.AZPlay.ExtSub_Color.value, 216)
        if self.Scaling_old != config.AZPlay.Scaling.value:
            cmd = 0
            if config.AZPlay.Scaling.value == 'Just Scale':
                cmd = 223
            if config.AZPlay.Scaling.value == 'Pan&Scan':
                cmd = 224
            if config.AZPlay.Scaling.value == 'Pillarbox':
                cmd = 225
            if cmd > 0:
                self.SendCMD2(-1, cmd)
        if self.UPnP_Enable_old != config.AZPlay.UPnP_Enable.value:
            if config.AZPlay.UPnP_Enable.value == '1':
                try:
                    os.system('/etc/init.d/djmount start &')
                    print ' >> START UPnP'
                except IOError:
                    print 'Error START_UPnP'

            else:
                try:
                    os.system('/etc/init.d/djmount stop &')
                    print ' >> STOP UPnP'
                except IOError:
                    print 'Error STOP_UPnP'

        self.ExtSub_Size_old = config.AZPlay.ExtSub_Size.value
        self.ExtSub_Position_old = config.AZPlay.ExtSub_Position.value
        self.ExtSub_Color_old = config.AZPlay.ExtSub_Color.value
        self.Scaling_old = config.AZPlay.Scaling.value
        self.UPnP_Enable_old = config.AZPlay.UPnP_Enable.value

    def SendCMD2(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            cmd = 'echo ' + str(k1) + ' > /tmp/rmfp.in2;echo ' + str(k2) + ' > /tmp/rmfp.cmd2'
            os.popen(cmd)
        else:
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            os.popen('echo ' + str(k2) + ' > /tmp/rmfp.cmd2')

    def SaveCfg(self):
        config.AZPlay.ExtSub_Enable.save()
        config.AZPlay.ExtSub_Encoding.save()
        config.AZPlay.ExtSub_FontSel.save()
        config.AZPlay.ExtSub_Size.save()
        config.AZPlay.ExtSub_Position.save()
        config.AZPlay.ExtSub_Color.save()
        config.AZPlay.ExtSub_OutColor.save()
        config.AZPlay.Scaling.save()
        config.AZPlay.UPnP_Enable.save()
        self.close('ok')

    def Izlaz(self):
        config.AZPlay.ExtSub_Size.value = self.ExtSub_Size_old1
        config.AZPlay.ExtSub_Position.value = self.ExtSub_Position_old1
        config.AZPlay.ExtSub_Color.value = self.ExtSub_Color_old1
        config.AZPlay.Scaling.value = self.Scaling_old1
        config.AZPlay.UPnP_Enable.value = self.UPnP_Enable_old1
        self.SendCMD2(config.AZPlay.ExtSub_Size.value, 212)
        time.sleep(0.11)
        self.SendCMD2(config.AZPlay.ExtSub_Position.value, 214)
        time.sleep(0.11)
        self.SendCMD2(config.AZPlay.ExtSub_Color.value, 216)
        time.sleep(0.11)
        cmd = 0
        if config.AZPlay.Scaling.value == 'Just Scale':
            cmd = 223
        if config.AZPlay.Scaling.value == 'Pan&Scan':
            cmd = 224
        if config.AZPlay.Scaling.value == 'Pillarbox':
            cmd = 225
        if cmd > 0:
            self.SendCMD2(-1, cmd)
        time.sleep(0.11)
        if self.ActivePlay == None:
            if config.AZPlay.UPnP_Enable.value == '1':
                try:
                    os.system('/etc/init.d/djmount start &')
                    print ' >> START UPnP'
                except IOError:
                    print 'Error START_UPnP'

            else:
                try:
                    os.system('/etc/init.d/djmount stop &')
                    print ' >> STOP UPnP'
                except IOError:
                    print 'Error STOP_UPnP'

        self.close()


class AZPlaySelectLang(ConfigListScreen, Screen):
    skin = '\n\t\t<screen position="center,center" size="710,275" title="AZPlay - Language Select" >\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="10,230" size="140,40" transparent="1" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="560,230" size="140,40" transparent="1" alphatest="on" />\n\t\t<widget source="key_red" render="Label" position="10,230" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget source="key_green" render="Label" position="560,230" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget source="poraka" render="Label" position="150,230" zPosition="1" size="400,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="list" position="10,10" size="690,210" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session, ALanguages):
        Screen.__init__(self, session)
        self.session = session
        self.ALanguages = ALanguages
        self.list = []
        self['actions'] = ActionMap(['ChannelSelectBaseActions',
         'WizardActions',
         'DirectionActions',
         'MenuActions',
         'NumberActions',
         'ColorActions'], {'save': self.SetLang,
         'back': self.Izlaz,
         'ok': self.SetLang,
         'green': self.SetLang,
         'red': self.Izlaz}, -2)
        self['key_red'] = StaticText(_('Exit'))
        self['key_green'] = StaticText(_('Set'))
        self['poraka'] = StaticText(_('AZPlay - Select Audio/Language'))
        list = []
        for subitem in self.ALanguages:
            ipos = subitem.find(':')
            ipos1 = subitem.rfind("'")
            if ipos > -1 and ipos1 > -1:
                subtmp = '   - Audio track :  | ' + subitem[ipos + 3:ipos1 - 1] + ' |'
                list.append(subtmp)

        self['list'] = MenuList(list)

    def SendCMD2(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            cmd = 'echo ' + str(k1) + ' > /tmp/rmfp.in2;echo ' + str(k2) + ' > /tmp/rmfp.cmd2'
            os.popen(cmd)
        else:
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            os.popen('echo ' + str(k2) + ' > /tmp/rmfp.cmd2')

    def SetLang(self):
        ind = self['list'].getSelectionIndex()
        tmpstr = self.ALanguages[ind]
        ipos = tmpstr.find('ID')
        ipos1 = tmpstr.find('(')
        if ipos >= 0 and ipos1 >= 0:
            AudioL = int(tmpstr[ipos + 2:ipos1])
        self.SendCMD2(AudioL, 116)
        time.sleep(0.11)
        self.close()

    def Izlaz(self):
        self.close()


class AZPlaySelectSub(ConfigListScreen, Screen):
    skin = '\n\t\t<screen position="center,center" size="710,275" title="AZPlay - Subtitle Select" >\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="10,230" size="140,40" transparent="1" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="560,230" size="140,40" transparent="1" alphatest="on" />\n\t\t<widget source="key_red" render="Label" position="10,230" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget source="key_green" render="Label" position="560,230" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget source="poraka" render="Label" position="150,230" zPosition="1" size="400,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="list" position="10,10" size="690,210" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session, SubtitlesL):
        Screen.__init__(self, session)
        self.session = session
        self.SubtitlesL = SubtitlesL
        self.list = []
        self['actions'] = ActionMap(['ChannelSelectBaseActions',
         'WizardActions',
         'DirectionActions',
         'MenuActions',
         'NumberActions',
         'ColorActions'], {'save': self.SetLang,
         'back': self.Izlaz,
         'ok': self.SetLang,
         'green': self.SetLang,
         'red': self.Izlaz}, -2)
        self['key_red'] = StaticText(_('Exit'))
        self['key_green'] = StaticText(_('Set'))
        self['poraka'] = StaticText(_('AZPlay - Select Audio/Language'))
        list = []
        for subitem in self.SubtitlesL:
            ipos = subitem.find(':')
            ipos1 = subitem.find('[')
            if ipos > -1 and ipos1 > -1:
                subtrack = subitem[ipos + 3:ipos1 - 2]
                if subtrack == 'tmp.srt':
                    subtrack = 'External'
                subtmp = '   - Subtitle track :  | ' + subtrack + ' |'
                list.append(subtmp)

        self['list'] = MenuList(list)

    def SendCMD2(self, k1, k2):
        if k1 >= 0:
            if os.path.exists('/tmp/rmfp.in2'):
                os.remove('/tmp/rmfp.in2')
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            cmd = 'echo ' + str(k1) + ' > /tmp/rmfp.in2;echo ' + str(k2) + ' > /tmp/rmfp.cmd2'
            os.popen(cmd)
        else:
            if os.path.exists('/tmp/rmfp.cmd2'):
                os.remove('/tmp/rmfp.cmd2')
            os.popen('echo ' + str(k2) + ' > /tmp/rmfp.cmd2')

    def SetLang(self):
        ind = self['list'].getSelectionIndex()
        tmpstr = self.SubtitlesL[ind]
        ipos = tmpstr.find('ID')
        ipos1 = tmpstr.find('(')
        if ipos >= 0 and ipos1 >= 0:
            SubtitleL = int(tmpstr[ipos + 2:ipos1])
        self.SendCMD2(SubtitleL, 118)
        time.sleep(0.11)
        self.close()

    def Izlaz(self):
        self.close()


def main(session, **kwargs):
    session.open(AZPlayScreen)


def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('AZPlay'),
          main,
          'AZPlay',
          44)]
    return []


def Plugins(path, **kwargs):
    hw_type = HardwareInfo().get_device_name()
    if hw_type == 'minime' or hw_type == 'me' or hw_type == 'elite' or hw_type == 'premium' or hw_type == 'premium+' or hw_type == 'ultra':
        plugin_list = [PluginDescriptor(name=_('AZPlay'), description='Play back media files', where=PluginDescriptor.WHERE_PLUGINMENU, needsRestart=False, fnc=main), PluginDescriptor(name=_('AZPlay'), where=PluginDescriptor.WHERE_MENU, fnc=menu)]
    else:
        plugin_list = []
    return plugin_list


global cache
