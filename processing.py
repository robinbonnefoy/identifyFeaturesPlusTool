from qgis.core import QgsGeometry, Qgis, QgsMapLayerType, QgsFeatureRequest, QgsProject, QgsCoordinateTransform, QgsPointXY, QgsRectangle
from qgis.gui import QgsMapToolEmitPoint


class ClickMapTool(QgsMapToolEmitPoint):
  def __init__(self, canvas, iface, status_bar):
    super().__init__(canvas)
    self.iface = iface
    self.status_bar = status_bar
    
        
  def is_raster(self, layer):
    """ Renvoie si la couche est un raster """
    return layer.type() == QgsMapLayerType.RasterLayer
  
  def enlarge_bbox(self, bbox, delta):
    """
    Agrandit une boîte englobante (QgsRectangle) par une valeur delta.
    
    Args:
        bbox (QgsRectangle): La boîte englobante à agrandir.
        delta (int): La valeur par laquelle agrandir la boîte englobante.

    Returns:
        QgsRectangle: La boîte englobante agrandie.
    """
    xmin = bbox.xMinimum() - delta
    ymin = bbox.yMinimum() - delta
    xmax = bbox.xMaximum() + delta
    ymax = bbox.yMaximum() + delta
    
    return QgsRectangle(xmin, ymin, xmax, ymax)

  def canvasReleaseEvent(self, event):
    """ Gestion du clic et de l'affichage des formulaire"""
    # Récupérer les coordonnées du clic
    point = QgsPointXY(event.mapPoint())

    # Récupérer la couche active avec son SCR
    active_layer = self.iface.activeLayer()
    crs = active_layer.crs()

    # Récupérer le SCR de la carte
    canvas_crs = self.iface.mapCanvas().mapSettings().destinationCrs()

    if self.is_raster(active_layer) : 
      self.iface.messageBar().pushMessage("Identify Tool FREDON ", "La couche active est un raster.", level=Qgis.Warning, duration=5)
        
    else :
      # Créer une géométrie de point à partir des coordonnées GPS
      point_geom = QgsGeometry.fromPointXY(point)

      # Créer un objet QgsCoordinateTransform pour la conversion du SCR du canvas vers la couche active
      transform = QgsCoordinateTransform(canvas_crs, crs, QgsProject.instance())

      # Appliquer la transformation 
      point_geom.transform(transform)

      # Agrandir la bounding Box pour identifier plus facilement les entités
      enlarged_bbox = self.enlarge_bbox(point_geom.boundingBox(), 2)

      # Créer une requête spatiale et récupérer les entités intersectant le point
      request = QgsFeatureRequest().setFilterRect(enlarged_bbox)

      # Exécution de la requête
      features = [feature for feature in active_layer.getFeatures(request)]

      if len(features) == 0 :
        self.status_bar.showMessage("Aucune entité trouvée dans la couche active")
      else :
        # Afficher les attributs des entités intersectant le point dans un formulaire
        message = '' + str(len(features)) + ' entité(s) identifiée(s)'
        self.status_bar.showMessage(message)
        for feature in features:
          self.iface.openFeatureForm(active_layer, feature)