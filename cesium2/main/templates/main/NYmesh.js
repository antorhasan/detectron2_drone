
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkZDM1MDQyYi05ZmZmLTQ5YjItOWJiNS0yYjQzZmY3OWM1NDYiLCJpZCI6MTQ2NzcsInNjb3BlcyI6WyJhc3IiLCJnYyJdLCJpYXQiOjE1NjYxNDkwNDh9.zAbDOcZl0STkWZiP8EVtrV5FeWGk5FzJvnRmH_LkZJs';
var viewer = new Cesium.Viewer('cesiumContainer', {
  animation: false,
  timeline: false,
  terrainProvider: Cesium.createWorldTerrain()});

  var tileset = viewer.scene.primitives.add(
  new Cesium.Cesium3DTileset({
      url: Cesium.IonResource.fromAssetId(64324)
  })
);


viewer._cesiumWidget._creditContainer.parentNode.removeChild(
viewer._cesiumWidget._creditContainer); 


viewer.zoomTo(tileset)

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {
    direction: 'left'
    });
});















