window.onload = loadcode();
flipped = false;

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
                    profileButton(data["username"], "£" + data["balance"], data["pfpUrl"])

                });
            })
        .catch(err => console.log('Fetch Error :-S', err));

    fetch('api/distributor/user/get_route_parts')
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
                    displayUserRoutes(data["routes"])
                });
            })
        .catch(err => console.log('Fetch Error :-S', err));

}

function displayUserRoutes(routes) {
    //routes = [12, 43, 432, 321]
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


                    var startmarker = L.marker([data.startPos.lat, data.startPos.lon]);
                    var endmarker = L.marker([data.endPos.lat, data.endPos.lon]);

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
                console.log(data);
                for (let i = 0; i < data["lockers"].length, i++;) {
                    var xCoord = data["lockers"][i].lattitude;
                    var yCoord = data["lockers"][i].longitude;
                    L.marker([xCoord, yCoord]).addTo(map);
                }
            });
        })
    .catch(err => console.log('Fetch Error :-S', err));
    
}



// loead sw

window.addEventListener('load', () => {
    if (!('serviceWorker' in navigator)) {
        // service workers not supported 😣
        return
    }

    navigator.serviceWorker.register('/sw.js').then(
        () => {
            console.log("reg")
        },
        err => {
            console.error('reg fail', err)
        }
    )
})
