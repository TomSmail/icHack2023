window.onload = buildDummy();

function buildDummy() {
    profileButton("Bob Ross", "420.69", "./bobross.jpeg")
}

function profileButton(name, balance, profilePicUrl) {

    var elem = document.createElement('div');
    var container = document.getElementById('name');
    container.appendChild(elem);
    elem.innerHTML = name;

    var elem2 = document.createElement('div');
    var container2 = document.getElementById('balance');
    container2.appendChild(elem2);
    elem2.innerHTML = balance;

    var elem3 = document.createElement('div');
    var container3 = document.getElementById('imgcontainer');
    const img = document.createElement('img');
    img.src = profilePicUrl;
    elem3.appendChild(img);
    container3.appendChild(elem3);
    
    //document.getElementById("profile").insertAdjacentElement('beforeBegin', node);
}