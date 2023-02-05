window.onload = loadcode();

var map = L.map('map')

map.setView([51.505, -0.09], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);


async function loadcode() {
    fetch('api/distributor/user/info')
        .then(
            response => {
                if (response.status !== 200) {
                    console.log('ERRNO: ' + response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                    console.log(data);
                    profileButton(data["username"], data["balance"], data["pfpUrl"])

                });
            })
        .catch(err => console.log('Fetch Error :-S', err));

    fetch('api/distributor/user/get_routes')
        .then(
            response => {
                if (response.status !== 200) {
                    console.log('ERRNO: ' + response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                    displayUserRoutes(data["routes"])
                });
            })
        .catch(err => console.log('Fetch Error :-S', err));

    displayUserRoutes()
}

function displayUserRoutes(routes) {
    routes = [12, 43, 432, 321]
    for (var i = 0; i < routes.length; i++) {
        const elem = document.createElement('div');

        elem.setAttribute("id", routes[i]);
        elem.setAttribute("class", "route");
        elem.setAttribute("onclick", "selectRoute(this)");
        elem.innerHTML = "<h3>Route num: " + (i + 1) + "</h3>"
        document.getElementById('routes').appendChild(elem);
    }
}

collection = []

function selectRoute(elem) {

    for (i = 0; i < collection.length; i += 1) {
        map.removeLayer(collection[i])
    }

    routeid = elem.id;
    startpos = { "lat": 51.51726867924614, "lon": -0.17006825107707066 }
    endpos = { "lat": 51.49908881784374, "lon": -0.17634169907999675 }
    startlockerpos = { "lat": 51.51576514449153, "lon": -0.17545614963098652 }
    endlockerpos = { "lat": 51.50075273293234, "lon": -0.18367794301514892 }

    map.setView([(startpos["lat"] + endpos["lat"]) / 2, (startpos["lon"] + endpos["lon"]) / 2], 13);


    var startmarker = L.marker([startpos.lat, startpos.lon]);
    var endmarker = L.marker([endpos.lat, endpos.lon]);

    var startlocker = L.marker([startlockerpos.lat, startlockerpos.lon]);
    var endlocker = L.marker([endlockerpos.lat, endlockerpos.lon]);

    var polyroute = L.polyline([[startpos.lat, startpos.lon],
    [startlockerpos.lat, startlockerpos.lon],
    [endlockerpos.lat, endlockerpos.lon],
    [endpos.lat, endpos.lon]],
        {
            color: 'red',
            weight: 3,
            opacity: 0.5
        });

    collection = [startlocker, endlocker, startmarker, endmarker, polyroute]

    for (i = 0; i < collection.length; i += 1) {
        collection[i].addTo(map);
    }


}

function profileButton(name, balance, profilePicUrl) {

    var elem = document.getElementById('name');
    elem.innerHTML = name;

    var elem2 = document.getElementById('balance');
    elem2.innerHTML = balance;

    var img = document.getElementById('imgcontainer');
    img.src = profilePicUrl;
}







// flip

flipped = false;

function flip() {

    elem = document.getElementById("secondary");
    if (!flipped) {
        console.log("shrink")

        elem.style.width = "0%";
        elem.style.padding = "0%";

    } else {
        console.log("expand")
        elem.style.width = "50%";

        elem.style.padding = "5%";
    }
    flipped = !flipped;
    map.invalidateSize();


    document.getElementById("secondary").style.width = "0px";

}   