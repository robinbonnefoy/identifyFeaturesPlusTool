from qgis.core import QgsGeometry, Qgis, QgsMapLayerType, QgsFeatureRequest
from qgis.gui import QgsMapToolEmitPoint


class ClickMapTool(QgsMapToolEmitPoint):
  def __init__(self, canvas, iface):
    super().__init__(canvas)
    self.iface = iface
    
        
  def is_raster(self, layer):
    """ Renvoie si la couche est un raster """
    return layer.type() == QgsMapLayerType.RasterLayer

  def canvasReleaseEvent(self, event):
    """ Gestion du clic et de l'affichage des formulaire"""
    # Récupérer les coordonnées du clic
    point = self.toMapCoordinates(event.pos())
    active_layer = self.iface.activeLayer()

    if self.is_raster(active_layer) : 
      self.iface.messageBar().pushMessage("Identify Tool FREDON ", "La couche active est un raster.", level=Qgis.Warning, duration=5)
        
    else :
      # Créer une géométrie de point à partir des coordonnées GPS
      point_geom = QgsGeometry.fromPointXY(point)
      print(active_layer)
      # Créer une requête spatiale et récupérer les entités intersectant le point
      request = QgsFeatureRequest().setFilterRect(point_geom.boundingBox())
      print(point_geom.boundingBox())
      features = [feature for feature in active_layer.getFeatures(request)]

    if len(features) == 0 :
      self.iface.messageBar().pushMessage("Identify Tool FREDON ", "Aucune entité trouvée dans la couche active.", level=Qgis.Info, duration=5)
    else :
      # Afficher les attributs des entités intersectant le point dans un formulaire
      for feature in features:
        self.iface.openFeatureForm(active_layer, feature)