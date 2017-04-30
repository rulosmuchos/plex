#*********************************************************************
# content   = menu Nuke
# version   = 0.0.1
# date      = 2017-01-01
#
# license   = MIT
# copyright = Copyright 2017 Filmakademie Baden-Wuerttemberg, Animationsinstitut
# author    = Alexander Richter <pipeline@richteralexander.com>
#*********************************************************************
# This source file has been developed within the scope of the
# Technical Director course at Filmakademie Baden-Wuerttemberg.
# http://td.animationsinstitut.de
#*********************************************************************

import os
import nuke
import webbrowser

import libLog
import libData
import software

TITLE = os.path.splitext(os.path.basename(__file__))[0]
LOG   = libLog.init(script=TITLE)

#************************
# FUNC
def add_gizmo_menu(menu):
    for paths in os.getenv('SOFTWARE_PATH').split(';'):
        for file in os.listdir(paths):
            if file.endswith('.gizmo'):
                gizmo = file.replace('.gizmo', '')
                menu.addCommand('Gizmos/' + gizmo, 'nuke.tcl({})'.format(gizmo))

def add_write_node():
    from scripts import writeNode
    write = nuke.allNodes("arWrite")
    for currentNode in write:
        writeNode.nodeCreate(currentNode)

def add_all_img():
    for img in os.getenv('IMG_PATH').split(';'):
        nuke.pluginAddPath('{}/software/nuke'.format(img))
        nuke.pluginAddPath('{}/software/nuke/menu'.format(img))


#*******************
# TOOLBAR
add_all_img()

project_data = libData.get_data()
menu_data = project_data['software']['NUKE']['MENU']
menuNode  = nuke.menu('Nodes').addMenu(project_data['project']['name'], icon = 'nuke.ico')

for menu_item in menu_data:
    software.Software.add_menu(menuNode, menu_item)

add_gizmo_menu(menuNode)
nuke.addOnScriptSave(add_write_node)

