""" 
    Worker works around with Files, and Directory

 - setting the cofiguration file, ui, and directory
 - creating or preparing the temporary files needed
 - managing the filenames, extension and other details
 - zipping the complete output of create
 
"""

import winreg
from all_val import *
from shutil import copytree, copy, move, rmtree
from uuid import uuid4 as generate_random_uuid 
from tkinter import filedialog, Toplevel, Label, StringVar, messagebox, _tkinter
from PIL import Image, ImageTk

class GetImageDetails:
  def __init__(self, imgpath):
    self.imgpath = imgpath
    
  def getimagename(self):
    imgext = GetImageDetails.getimgext(self)
    rmpackex = self.imgpath.replace('jpg', 'jpeg').replace(imgext, "")
    # Remove The dirname to get the filename
    default_index = 1
    getimgpath = rmpackex
    imgpathfori = getimgpath+" "
    while getimgpath[:-default_index].startswith('/') == False:
      cl= default_index+1
      default_index = cl
      rmdirtxt = (imgpathfori[:-default_index])
      if rmdirtxt.endswith('/') == True:
        thefilename = imgpathfori.replace(rmdirtxt, "")
        imagefilename = (thefilename[:-1])
        image_details.append(imagefilename)
        break
  
  def getimgext(self):
    image_details.append(self.imgpath)
    imgext = Image.open(self.imgpath).format
    theimgext = "."+imgext.lower()
    image_details.append(theimgext)
    print("Image Path: "+image_details[0])
    print("Image Format: "+theimgext)
    return theimgext

class ToDoDuringStartup:
  config_folder = config_dir.replace("\\settings.json", "")

  def makethetempdir(self):
    if path.exists(tempdir): pass
    else: mkdir(tempdir)
    if path.exists(self.config_folder): pass
    else: mkdir(self.config_folder)
    return self
          
  # Set The Default Output Folder Path
  def setdefaults(self):
    if path.exists(config_dir):pass
    else:
      with winreg.OpenKey(winreg.HKEY_CURRENT_USER, dsktp_regkey) as key:
        userdesktop = path.expandvars( winreg.QueryValueEx(key, "Desktop")[0] ).replace("\\", "/")
        with open(config_dir, 'w') as writeconfig:
          configuration = { "Image_Size": "256", "Convert_To_Zip": False, 
                "Convert_To_Mcpack": False, "Outputfolder_Path": userdesktop }
          readusingjson = dump(configuration, writeconfig, indent=4)
    return self
  
  def installfonts(self):
    font_dir = "C:\\windows\\Fonts\\NotoSans-Regular.ttf"
    if path.exists(font_dir): pass
    else: passcopy('res\\NotoSans-Regular.ttf', font_dir)
    return self

class ConfigManagement: 
  # Get the config value then update to a dict{}
  ImgResConfigValue = lambda self, imgresvalue : config_dict.update({'image_res': imgresvalue})
  CnvrtToMcpackValue = lambda self, chmcpackval: config_dict.update({'mc_convert': chmcpackval}) 
  CnvrtToJavZipValue = lambda self, chjvzipval: config_dict.update({'jv_convert': chjvzipval})
  OutPathConfigValue = lambda self, outpathvalue: config_dict.update({'output_path': outpathvalue})
  CustomImgResConfigValue = lambda self, imgresvalue: config_dict.update({'image_custom_res': imgresvalue})
    
  def writesettingsconfig(self): 
    try:
      if config_dict['output_path'] == "": 
        userpath = readconfig()[1]
      else: userpath = config_dict['output_path']
    except KeyError: userpath = readconfig()[1]
    if config_dict.get('image_custom_res') == None:
      try: chosen_res = config_dict['image_res']
      except KeyError: chosen_res = readconfig()[0]
    else: chosen_res = config_dict['image_custom_res']

    getchconmcpack = config_dict.get('mc_convert')
    getchconjavzip = config_dict.get('jv_convert')
    if getchconjavzip == None: getchconjavzip = readconfig()[2]
    if getchconmcpack == None: getchconmcpack = readconfig()[3]

    with open(config_dir, 'w') as writeconfig:
      configuration = { "Image_Size": chosen_res, "Convert_To_Zip": getchconjavzip,
                        "Convert_To_Mcpack": getchconmcpack, "Outputfolder_Path": userpath }
      readusingjson = dump(configuration, writeconfig, indent=4)
      config_dict.clear()
  
class SettingsMultiOptions:
    def __init__(self, imgresolution, packzipval, packmcpackval ):
      self.packzipval = packzipval
      self.imgresolution = imgresolution
      self.packmcpackval = packmcpackval
     
    def outputres(self):
      chosen_res = self.imgresolution.get()
      if chosen_res == int(0): chosen_res = 256
      elif chosen_res == int(10): chosen_res = 512
      elif chosen_res == int(20): chosen_res = 1024
      elif chosen_res == int(30): chosen_res = 2048
      ConfigManagement().ImgResConfigValue(chosen_res)
        
    def checkzipconvert(self):
      thepackzipvalue = self.packzipval.get()
      if thepackzipvalue == False: thepackzipvalue = False
      elif thepackzipvalue == True: thepackzipvalue = True
      ConfigManagement().CnvrtToJavZipValue(thepackzipvalue)
      
    def checkmcpackconvert(self):
      thepackmcpackchvalue = self.packmcpackval.get()
      if thepackmcpackchvalue == False: thepackmcpackchvalue = False
      elif thepackmcpackchvalue == True: thepackmcpackchvalue = True
      ConfigManagement().CnvrtToMcpackValue(thepackmcpackchvalue)
    
class MkJsonPackDetailsFile:
  #GetImageDetails.getimagename(self)
  pack_des = "This SkyOverlay Was Made By The Help Of §cAkqir's (§bMC §fSky Builder) Software..." 
  def makethemanifest():
    uuid1 = generate_random_uuid()
    uuid2 = generate_random_uuid()
    # For Bedrock Write The Manifest File 
    with open(tempdir+'manifest.json', 'w') as writejson:
      manifestfile =  { "format_version": 1, "header": { 
                        "description": MkJsonPackDetailsFile.pack_des,
                        "name": image_details[2]+" (Sky Overlay)", "uuid": str(uuid1), 
                        "version": [1, 0, 0], "min_engine_version": [1, 12, 0]}, "modules": [ { 
                        "description": "", "type": "resources", "uuid": str(uuid2), "version": [1, 0, 0] } ] }
      dump(manifestfile, writejson, sort_keys=True, skipkeys=1, indent=3)
    
  def makethepackmeta():
    with open(tempdir+'pack.json', 'w') as writepckmeta:
      pack_des = FileManagement.pack_des.replace("§c", "").replace("§b", "").replace("§f", "")
      packmeta = { "pack": { "pack_format": 1, "description": pack_des } }
      dump(packmeta, writepckmeta, sort_keys=True, skipkeys=1, indent=3)
    os.rename('pack.json', 'pack.mcmeta')
     
  def makepackicon():
    pass

class PackingPack:
  def MoveToOut(self):
    print("Moving Sky To Pack Folder...")
    old_names = ["Back.png", "Bottom.png", "Front.png", "Left.png", "Top.png", "Right.png"]
    new_names = ["cubemap_0.png", "cubemap_5.png", "cubemap_2.png","cubemap_1.png","cubemap_4.png", "cubemap_3.png"]
    MkJsonPackDetailsFile.packrenamer(old_names, new_names)
    return self

  def ZipMcpackOrBoth(self):
    if readconfig()[2] == True: 
      path = image_details[2]+"\\textures\\environment\\overworld_cubemap"
      copy(tempdir+"\\"+sky_names, tempdir+path)
      print("Converting to Zip (Java Option!!)...")
      MkJsonPackDetailsFile.makethepackmeta()

    if readconfig()[3] == True: 
      path = image_details[2]+"\\assets\\minecraft\\mcpatcher\\sky\\world0"
      print("Converting to Mcpack (Bedrock Option!!)...")
      MkJsonPackDetailsFile.makethemanifest()
      
    def CheckPackFolder():
      for move_no in range (0, 6): 
        sky_names = old_names[move_no]
        sky_path = tempdir+"\\sky_output\\"+sky_names
        if path.exists(sky_path): rm(sky_path)
    return self
