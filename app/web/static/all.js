window.onload = loadcode();
flipped = false;

var map = L.map('map')

var greenIcon = L.icon({
    iconUrl: 'marker-icon-green.png',
    shadowUrl: 'leaf-shadow.png',

    iconSize: [38, 95], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var redIcon = L.icon({
    iconUrl: 'marker-icon-red.png',
    shadowUrl: 'leaf-shadow.png',

    iconSize: [38, 95], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});


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
                    profileButton(data["username"], "£" + data["balance"], data["pfpUrl"])

                });
            })
        .catch(err => console.log('Fetch Error :-S', err));
    getroute()
}

setInterval(function () {
    getroute()
}, 4000);

function getroute() {
    fetch('api/distributor/user/get_route_parts')
        .then(
            response => {
                if (response.status !== 200) {
                    console.log('ERRNO: ' + response.status);
                    return;
                }
                response.json().then(function (data) {
                    //console.log("refreshing routes")
                    //routes = [12, 43, 432, 321]
                    document.getElementById("routes").innerHTML = "";
                    for (var i = 0; i < data["routes"].length; i++) {
                        const elem = document.createElement('div');

                        elem.setAttribute("id", data["routes"][i]);
                        elem.setAttribute("class", "route");
                        elem.setAttribute("onclick", "selectRoute(this)");
                        elem.innerHTML = "<h3>Route number: " + (i + 1) + "</h3>"
                        document.getElementById('routes').appendChild(elem);
                    }

                });
            })
        .catch(err => console.log('Fetch Error :-S', err));
}

collection = []

function selectRoute(elem) {

    tm = document.getElementById("secondary");
    flipped = true;

    tm.classList.add("hidden");
    map.invalidateSize();

    fetch('api/distributor/route_part/get?route_part_id=' + elem.id)
        .then(
            response => {
                if (response.status !== 200) {
                    console.log('ERRNO: ' + response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {

                    console.log(data)

                    for (i = 0; i < collection.length; i += 1) {
                        map.removeLayer(collection[i])
                    }

                    startpos = { "lat": 51.51726867924614, "lon": -0.17006825107707066 }
                    endpos = { "lat": 51.49908881784374, "lon": -0.17634169907999675 }
                    startlockerpos = { "lat": 51.51576514449153, "lon": -0.17545614963098652 }
                    endlockerpos = { "lat": 51.50075273293234, "lon": -0.18367794301514892 }

                    map.setView([(data.startPos["lat"] + data.endPos["lat"]) / 2, (data.startPos["lon"] + data.endPos["lon"]) / 2], 13);


                    var startmarker = L.marker([data.startPos.lat, data.startPos.lon], { icon: greenIcon });
                    var endmarker = L.marker([data.endPos.lat, data.endPos.lon], { icon: redIcon });

                    var startlocker = L.marker([data.startLocker.lat, data.startLocker.lon]);
                    var endlocker = L.marker([data.endLocker.lat, data.endLocker.lon]);

                    var polyroute = L.polyline([[data.startPos.lat, data.startPos.lon],
                    [data.startLocker.lat, data.startLocker.lon],
                    [data.endLocker.lat, data.endLocker.lon],
                    [data.endPos.lat, data.endPos.lon]],
                        {
                            color: 'red',
                            weight: 3,
                            opacity: 0.5
                        });

                    collection = [startlocker, endlocker, startmarker, endmarker, polyroute]

                    for (i = 0; i < collection.length; i += 1) {
                        collection[i].addTo(map);
                    }




                });
            })
        .catch(err => console.log('Fetch Error :-S', err));





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


function flip() {

    elem = document.getElementById("secondary");
    if (!flipped) {
        console.log("shrink")
        elem.classList.add("hidden");


    } else {
        console.log("expand")
        elem.classList.remove("hidden");
    }
    flipped = !flipped;
    map.invalidateSize();



}

function toggleVis() {
    fetch('api/distributor/locker/getall')
        .then(
            response => {
                if (response.status !== 200) {
                    console.log('ERRNO: ' + response.status);
                    if (response.status == 500) {
                        //document.location.href = "/login"
                    }
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                    console.log(data["lockers"]);
                    for (let i = 0; i < data["lockers"].length, i += 1;) {
                        var xCoord = data["lockers"][i]["latitude"];
                        var yCoord = data["lockers"][i]["longitude"];
                        L.marker([xCoord, yCoord]).addTo(map);
                    }
                });
            })
        .catch(err => console.log('Fetch Error :-S', err));

}



window.addEventListener("load", () => {
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("sw.js");
    }
});