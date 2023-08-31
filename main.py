from qgis.PyQt.QtGui import QIcon, QCursor
from qgis.PyQt.QtWidgets import QAction
from PyQt5.QtCore import Qt

from .processing import ClickMapTool as cl
import os.path
import os
import inspect

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class IdentifyFeaturesPLUS:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

    # Créer une instance de la classe ClickMapTool
    self.click_tool = cl(self.iface.mapCanvas(), self.iface)
  
  def map_tool_changed(self, tool):
    """ Réinitialise le bouton et le curseur si l'utilisateur change d'outil """
    if tool != self.click_tool:
        self.action.setChecked(False)  # Désenfoncer le bouton lorsque l'outil change
        self.iface.mapCanvas().unsetCursor()  # Rétablir le pointeur par défaut

        

  def initGui(self):
    # create action that will start plugin configuration
    icon = os.path.join(os.path.join(cmd_folder, 'icon_identifyFeaturesPlus.png'))
    self.action = QAction(QIcon(icon),
                          "Identify Features PLUS Tool",
                          self.iface.mainWindow())
    self.action.setObjectName("testAction") # Definie le nom de l'objet QAction pour l'utiliser
    self.action.setStatusTip("Ouvrir le formulaire de l'entité sélectionnée de la couche active.")
    self.action.setCheckable(True)  # Rend le bouton enfonçable
    self.action.triggered.connect(self.run)

    # add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)

  def unload(self):
    # remove the plugin menu item and icon
    self.iface.removeToolBarIcon(self.action)

  def run(self):
    # Activer l'outil de clic sur la carte
    self.iface.mapCanvas().setMapTool(self.click_tool)
    self.iface.mapCanvas().setCursor(QCursor(Qt.WhatsThisCursor)) # Changer le pointeur
    # Détecter l'outil ne sera plus actif
    self.iface.mapCanvas().mapToolSet.connect(self.map_tool_changed)