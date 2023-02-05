window.onload = buildDummy();

function buildDummy() {
    profileButton("Bob Ross", "420.69", "./bobross.jpeg")
}

function profileButton(name, balance, profilePicUrl) {

    var elem = document.getElementById('name');
    elem.innerHTML = name;

    var elem2 = document.getElementById('balance');
    elem2.innerHTML = balance;

    var img = document.getElementById('imgcontainer');
    img.src = profilePicUrl;

    //document.getElementById("profile").insertAdjacentElement('beforeBegin', node);
}