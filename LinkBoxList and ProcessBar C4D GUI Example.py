"""
LinkBoxList & ProcessBar GUI Example

Author: Asthon Rolle AKA AP Asthon

Cinema 4D Python Script For C4D
Compatible:
    - Win / Mac
    - R16, R17, R18, R19, R20, R21
"""


#  // Imports for Cinema 4D //
import c4d
import os
import sys 
import webbrowser 
import math 
import random
import urllib 
import glob 
import shutil 
import time
import datetime
from c4d import plugins, gui, bitmaps, documents, storage, utils
from random import randint

# Colors
BG_DARK = c4d.Vector(0.1015625, 0.09765625, 0.10546875)
DARK_BLUE_TEXT_COL = c4d.Vector(0, 0.78125, 0.99609375)
DARK_RED_TEXT_COL = c4d.Vector(0.99609375, 0, 0)



# ---------------------------------------------------------------------
#       Creating GUI Instance Functions UI Elements Operations 
#                          Hepler Methods. 
# ---------------------------------------------------------------------

def AddLinkBoxList_GUI(ui_ins, ui_id, w_size, h_size, enable_state_flags):
    """ 
    This GUI name is really call a c4d.gui.InExcludeCustomGui.
    / InExclude custom GUI (CUSTOMGUI_INEXCLUDE_LIST). 
    """
    #First create a container that will hold the items we will allow to be dropped into the INEXCLUDE_LIST gizmo
    acceptedObjs = c4d.BaseContainer()
    acceptedObjs.InsData(c4d.Obase, "") # -> # Accept all objects / you change as desired 
                                             # Take a look at c4d Objects Types in SDK.
    # Create another base container for the INEXCLUDE_LIST gizmo's settings and add the above container to it
    bc_IEsettings = c4d.BaseContainer()
    bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_SEND_SELCHANGE_MSG, True)
    bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_INIT_STATE, 1)
    """ 
    Its buttons with states for each object in the list container gui of the CUSTOMGUI_INEXCLUDE_LIST.
    feel free to enable this in the ui by seting the  enable_state_flags to True. 
    """
    if enable_state_flags == True:
        bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_NUM_FLAGS, 2)
        # button 1
        bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_IMAGE_01_ON, 1039241) # -> Id Icon or Plugin Id 
        bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_IMAGE_01_OFF, 1039241)
        # button 2
        bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_IMAGE_02_ON, 1039801)
        bc_IEsettings.SetData(c4d.IN_EXCLUDE_FLAG_IMAGE_02_OFF, 1036394)
        
    bc_IEsettings.SetData(c4d.DESC_ACCEPT, acceptedObjs)        
    ui_ins.AddCustomGui(ui_id, c4d.CUSTOMGUI_INEXCLUDE_LIST, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, w_size, h_size, bc_IEsettings)
    return True


def Add_ProgressBar_GUI(ui_ins, progressbar_ui_id, strText_id, w_size, h_size):
    """
    Create ProgressBar GUI
    """
    ui_ins.GroupBegin(0, c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 0, 1)   
    ui_ins.GroupBorderNoTitle(c4d.BORDER_THIN_IN)
    # ProgressBar
    ui_ins.AddCustomGui(progressbar_ui_id, c4d.CUSTOMGUI_PROGRESSBAR, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, w_size, h_size)
    ui_ins.AddSeparatorV(0, c4d.BFV_SCALEFIT)
    # Static UI Text
    ui_ins.AddStaticText(strText_id, c4d.BFH_MASK, 50, h_size, "", c4d.BORDER_WITH_TITLE_BOLD) 
    ui_ins.GroupEnd() # Group End           
    return True

def Run_PrcoessBar(ui_ins, progressbar_ui_id, currentNum, amountOfObjects, col):
    # Prcoess Bar
    percent = float(currentNum)/amountOfObjects*100
    # Set Data to PROGRESSBAR
    progressMsg = c4d.BaseContainer(c4d.BFM_SETSTATUSBAR)
    progressMsg[c4d.BFM_STATUSBAR_PROGRESSON] = True
    progressMsg[c4d.BFM_STATUSBAR_PROGRESS] = percent/100.0 
    # this if you want a custom color
    if col:
        ui_ins.SetDefaultColor(progressbar_ui_id, c4d.COLOR_PROGRESSBAR, col)    
    ui_ins.SendMessage(progressbar_ui_id, progressMsg)
    # Return Percent String Data  
    return str(int(percent))+"%"
  
def Stop_ProgressBar(ui_ins, progressbar_ui_id):
    progressMsg = c4d.BaseContainer(c4d.BFM_SETSTATUSBAR)
    progressMsg.SetBool(c4d.BFM_STATUSBAR_PROGRESSON, False)
    ui_ins.SendMessage(progressbar_ui_id, progressMsg)
    return True

# ------------------------------------------------------------------------------------ #


# ----------------------------------------
#  // UI Main Window //
# ----------------------------------------
class Tool_WindowDialog(c4d.gui.GeDialog):
    
    # GUI Ids
    IDS_VER = 999
    IDS_OverallGrp = 1000
    IDS_StaticText = 1001 
    IDS_BTN_01 = 1002
    IDS_LINKBOXLIST = 1003
    IDS_MULTI_LINE_STRINGBOX = 1004
    IDS_PROCESSBAR_GUI = 1006 
    IDS_PROCESSBAR_TEXT = 1007   

    def Get_ObjectsLinkList(self):
        """ Get Objects """
        LinkList =  self.FindCustomGui(self.IDS_LINKBOXLIST, c4d.CUSTOMGUI_INEXCLUDE_LIST)
        Get_ObjectListData = LinkList.GetData()
        objs = Get_ObjectListData.GetObjectCount()
        if objs:
            currentNum = 1
            amountOfObjects = objs
            for i in xrange(objs):
                
                self.SetString(self.IDS_PROCESSBAR_TEXT, 
                               Run_PrcoessBar(ui_ins=self, 
                                              progressbar_ui_id=self.IDS_PROCESSBAR_GUI, 
                                              currentNum=currentNum, 
                                              amountOfObjects=amountOfObjects,
                                              col=None #DARK_BLUE_TEXT_COL # DARK_RED_TEXT_COL
                                              ) 
                              )
                
                # Get Data From Objects
                objName_data = Get_ObjectListData.ObjectFromIndex(doc, i).GetName()
                objID_data = Get_ObjectListData.ObjectFromIndex(doc, i).GetGUID()
                
                # Print to Your Custom GUI Log
                data = self.GetString(self.IDS_MULTI_LINE_STRINGBOX)
                show_data = data +"\n" +objName_data+" | ID : "+str(objID_data)
                self.SetString(self.IDS_MULTI_LINE_STRINGBOX, show_data)
                print(show_data)
                
                currentNum += 1
                
            Stop_ProgressBar(ui_ins=self, progressbar_ui_id=self.IDS_PROCESSBAR_GUI)      
        return True        
        
    # ====================================== #        
    #  Main GeDialog Class Overrides
    # ====================================== #
    def __init__(self):
        """
        The __init__ is an Constuctor and help get 
        and passes data on from the another class.
        """        
        super(Tool_WindowDialog, self).__init__()

    # UI Layout
    def CreateLayout(self):
        
        
        # Dialog Title
        self.SetTitle("LinkBoxList & ProcessBar GUI")
        
        # Top Menu addinng Tool Version
        self.GroupBeginInMenuLine()
        self.AddStaticText(self.IDS_VER, 0)
        self.SetString(self.IDS_VER, " v1.0  ")
        self.GroupEnd()        
        
        self.GroupBegin(self.IDS_OverallGrp, c4d.BFH_SCALEFIT, 1, 0, "") # Overall Group.
        
        # Static UI Text
        self.AddStaticText(self.IDS_StaticText, c4d.BFH_CENTER, 0, 15, "LinkBoxList & ProcessBar GUI Example", c4d.BORDER_WITH_TITLE_BOLD)
        
        self.AddSeparatorH(0, c4d.BFH_SCALEFIT) # Line Separator / eg: self.AddSeparatorH(0, c4d.BFH_MASK) and AddSeparatorV 

        self.GroupBegin(0, c4d.BFH_SCALEFIT, 3, 0, "") 
        self.GroupBorderSpace(5, 5, 5, 5)
        
        self.GroupBegin(0, c4d.BFH_SCALEFIT, 1, 0, "") 
        self.AddStaticText(self.IDS_StaticText, c4d.BFH_LEFT, 0, 15, " Add Objects :", c4d.BORDER_WITH_TITLE_BOLD)
        AddLinkBoxList_GUI(ui_ins=self, ui_id=self.IDS_LINKBOXLIST, w_size=290, h_size=200, enable_state_flags=False)
        self.GroupEnd()        

        self.AddSeparatorV(0, c4d.BFV_SCALEFIT)
        
        self.GroupBegin(0, c4d.BFH_SCALEFIT, 1, 0, "")
        self.AddStaticText(self.IDS_StaticText, c4d.BFH_LEFT, 0, 15, " Log :", c4d.BORDER_WITH_TITLE_BOLD)
        self.AddMultiLineEditText(self.IDS_MULTI_LINE_STRINGBOX, c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 290, 200, c4d.DR_MULTILINE_MONOSPACED)
        self.GroupEnd()  
        
        self.GroupEnd() 
                      
        self.AddSeparatorH(0, c4d.BFH_SCALEFIT)
        
        Add_ProgressBar_GUI(ui_ins=self, progressbar_ui_id=self.IDS_PROCESSBAR_GUI, strText_id=self.IDS_PROCESSBAR_TEXT, w_size=100, h_size=10)
        
        self.AddSeparatorH(0, c4d.BFH_SCALEFIT)
        
        self.AddButton(self.IDS_BTN_01, c4d.BFH_SCALEFIT, 100, 15, name="Run Process of Objects") 
        
        self.AddSeparatorH(0, c4d.BFH_SCALEFIT)
        
        
        
        self.GroupEnd() 

        self.GroupEnd() # End of the overall group.        
        return True

    def InitValues(self):
        """ 
        Called when the dialog is initialized by the GUI / GUI's startup values basically.
        """
        self.SetDefaultColor(self.IDS_OverallGrp, c4d.COLOR_BG, BG_DARK)
        self.SetDefaultColor(self.IDS_StaticText, c4d.COLOR_TEXT, DARK_BLUE_TEXT_COL) 
        self.SetDefaultColor(self.IDS_VER, c4d.COLOR_TEXT, DARK_RED_TEXT_COL)
        self.SetString(self.IDS_PROCESSBAR_TEXT, "0%")
        #self.Enable(self.IDS_MULTI_LINE_STRINGBOX, False)# --> # Disable or Enable Mode of the user interaction       
        return True 
 
    def Command(self, id, msg):
        """
        This Method is called automatically when the user clicks on a gadget and/or changes its value this function will be called.
        It is also called when a string menu item is selected.
        :param messageId: The ID of the gadget that triggered the event.
        :param bc: The original message container
        :return: False if there was an error, otherwise True.
        """        
        if id:
            print(str(id))
            
        if (id == self.IDS_BTN_01):
            self.Get_ObjectsLinkList()
                    
        return True
    

    def CoreMessage(self, id, msg):
        """
        Override this function if you want to react to Cinema 4D core messages. 
        The original message is stored in msg
        """     
        if id == c4d.EVMSG_CHANGE:
            pass
        return True    
    
    def DestroyWindow(self):
        """
        DestroyWindow Override this method - this function is 
        called when the dialog is about to be closed temporarily, 
        for example for layout switching. 
        """        
        print("Script Tool GUI Dialog Close.")



if __name__=='__main__':
    class_dialog = Tool_WindowDialog()
    class_dialog.Open(c4d.DLG_TYPE_ASYNC, defaultw=200, defaulth=10)
