

/**
 * Adds two SVG markers over the homes of the Chicago Bears and Chicago Cubs
 *
 * @param  {H.Map} map      A HERE Map instance within the application
 */
function addSVGMarkers(map){
  //Create the svg mark-up
  var svgMarkup = '<svg  width="24" height="24" xmlns="http://www.w3.org/2000/svg">' +
  '<rect stroke="black" fill="${FILL}" x="1" y="1" width="22" height="22" />' +
  '<text x="12" y="18" font-size="12pt" font-family="Arial" font-weight="bold" ' +
  'text-anchor="middle" fill="${STROKE}" >C</text></svg>';

  // Add the first marker
  var bearsIcon = new H.map.Icon(
    svgMarkup.replace('${FILL}', 'blue').replace('${STROKE}', 'red')),
    bearsMarker = new H.map.Marker({lat:32.07675654, lng:34.79099751 },
      {icon: bearsIcon});

  map.addObject(bearsMarker);

  // Add the second marker.
  var cubsIcon = new H.map.Icon(
    svgMarkup.replace('${FILL}', 'white').replace('${STROKE}', 'orange')),
    cubsMarker = new H.map.Marker({lat:32.07726563, lng:34.7874784541 },
      {icon: cubsIcon});

  map.addObject(cubsMarker);
}

/**
 * Boilerplate map initialization code starts below:
 */

//Step 1: initialize communication with the platform
// In your own code, replace variable window.apikey with your own apikey

//Step 2: initialize a map - this map is centered over Chicago.

                  
                












/**
 * Adds context menus for the map and the created objects.
 * Context menu items can be different depending on the target.
 * That is why in this context menu on the map shows default items as well as
 * the "Add circle", whereas context menu on the circle itself shows the "Remove circle".
 *
 * @param {H.Map} map Reference to initialized map object
 */
function addContextMenus(map) {
  // First we need to subscribe to the "contextmenu" event on the map
  map.addEventListener('contextmenu', function (e) {
    // As we already handle contextmenu event callback on circle object,
    // we don't do anything if target is different than the map.
    if (e.target !== map) {
      return;
    }

    // "contextmenu" event might be triggered not only by a pointer,
    // but a keyboard button as well. That's why ContextMenuEvent
    // doesn't have a "currentPointer" property.
    // Instead it has "viewportX" and "viewportY" properties
    // for the associates position.

    // Get geo coordinates from the screen coordinates.
    var coord  = map.screenToGeo(e.viewportX, e.viewportY);

    // In order to add menu items, you have to push them to the "items"
    // property of the event object. That has to be done synchronously, otherwise
    // the ui component will not contain them. However you can change the menu entry
    // text asynchronously.
    e.items.push(
      // Create a menu item, that has only a label,
      // which displays the current coordinates.
      new H.util.ContextItem({
        label: [
          Math.abs(coord.lat.toFixed(4)) + ((coord.lat > 0) ? 'N' : 'S'),
          Math.abs(coord.lng.toFixed(4)) + ((coord.lng > 0) ? 'E' : 'W')
        ].join(' ')
      }),
      // Create an item, that will change the map center when clicking on it.
      new H.util.ContextItem({
        label: 'Center map here',
        callback: function() {
          map.setCenter(coord, true);
        }
      }),
      // It is possible to add a seperator between items in order to logically group them.
      H.util.ContextItem.SEPARATOR,
      // This menu item will add a new circle to the map
      new H.util.ContextItem({
        label: 'הוסף דיווח',
        callback: addCircle.bind(map, coord)
      })
    );
  });
}

/**
 * Adds a circle which has a context menu item to remove itself.
 *
 * @this H.Map
 * @param {H.geo.Point} coord Circle center coordinates
 */
function addCircle(coord) {
  // Create a new circle object
  var circle = new H.map.Circle(coord, 100),
      map = this;

  // Subscribe to the "contextmenu" eventas we did for the map.
  circle.addEventListener('contextmenu', function(e) {
    // Add another menu item,
    // that will be visible only when clicking on this object.
    //
    // New item doesn't replace items, which are added by the map.
    // So we may want to add a separator to between them.
    e.items.push(
      new H.util.ContextItem({
        label: 'Remove',
        callback: function() {
          map.removeObject(circle);
        }
      })
    );
  });

  // Make the circle visible, by adding it to the map
  map.addObject(circle);
}

/**
 * Boilerplate map initialization code starts below:
 */







/**
 * Moves the map to display over Berlin
 *
 * @param  {H.Map} map      A HERE Map instance within the application
 */
function moveMapToTelAviv(map){
  map.setCenter({lat:32.07563227682336, lng:34.791035994817925});
  map.setZoom(15);
}

/**
 * Boilerplate map initialization code starts below:
 */

//Step 1: initialize communication with the platform
// In your own code, replace variable window.apikey with your own apikey
var platform = new H.service.Platform({
  apikey: window.apikey
});
var defaultLayers = platform.createDefaultLayers();

//Step 2: initialize a map - this map is centered over Europe
var map = new H.Map(document.getElementById('map'),
  defaultLayers.vector.normal.map,{
  center: {lat:50, lng:5},
  zoom: 4,
  pixelRatio: window.devicePixelRatio || 1
});
// add a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());

//Step 3: make the map interactive
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Create the default UI components
var ui = H.ui.UI.createDefault(map, defaultLayers);

// Now use the map as required...
window.onload = function () {
  moveMapToTelAviv(map);
  // Step 5: main logic
addContextMenus(map);

// Now use the map as required...
addSVGMarkers(map);
}
