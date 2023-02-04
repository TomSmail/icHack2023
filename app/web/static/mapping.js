// loads map on page load
window.onload = buildMap();

// INSERT BACKEND URL
var backEndUrl = "";


// adds tile layers
function buildMap() {
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',

    }).addTo(map);
    buildDummy(map);
    //getDropOffBoxes(map);
}

// GET requesets
async function getDropOffBoxes(map) {
    const response = await fetch(backEndUrl + '/user/create');
    const listOfDropboxes = await response.json();
    var pointList = [];
    for (let i = 0; i < listOfDropboxes.length; i++) {
        var box = listOfDropboxes[i]
        pointList.push([box.xCoord, box.yCoord, box.destinationBool, 500])
    }
    buildLocations(pointList, [], map);
}

function buildLocations(circleData, pointData, map) {
    for (let i = 0; i < circleData.length; i++) {
        var p = circleData[i];
        //  xCoord, yCoord, is it a destination and circle radius
        addCircle(p[0], p[1], p[2], p[3]).addTo(map);
    }
    for (let i = 0; i < pointData.length; i++) {
        var p = pointData[i];
        //  xCoord, yCoord, is it a destination and popup data
        addDropOffBox(p[0], p[1], p[2]).bindPopup(p[3]).addTo(map);
    }
}

function buildDummy(map) {
    var circleData = [[51.53, -0.092, true, 500], [51.54, -0.091, false, 500]]
    var pointData = [[51.53, -0.092, true, "Post Box"], [51.54, -0.091, false, "Drop Point"]]
    buildLocations(circleData, pointData, map);
}

function addCircle(xCoord, yCoord, destinationBool, radius) {
    var colour;
    var fillColour;
    if (destinationBool) {
        colour = '#1ABC9C';
        fillColour = '#A3E4D7';
    } else {
        colour = '#16A085';
        fillColour = '#45B39D'
    }
    return L.circle([xCoord, yCoord], {
        color: colour,
        fillColor: fillColour,
        fillOpacity: 0.5,
        // in meters
        radius: radius
    });
}

function addDropOffBox(xCoord, yCoord, destinationBool) {
    if (destinationBool) {
        colour = '#1ABC9C';
    } else {
        colour = '#16A085';
    }
    return L.circle([xCoord, yCoord], {
        color: colour,
        fillColor: colour,
        radius: 5
    });
}


flipped = false;

function flip() {

    elem = document.getElementById("secondary");
    if (!flipped) {
        console.log("shrink")

        elem.style.width = "0px";
    } else {
        console.log("expand")
        elem.style.width = "50%";
    }
    flipped = !flipped
    map.invalidateSize();

    document.getElementById("secondary").style.width = "0px";

}
