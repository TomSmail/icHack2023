window.onload = getprofiledata();


function getprofiledata() {

    const response = fetch('api/distributor/user/info');
    console.log(response)



    profileButton("Bob Ross", "420.69", "./bobross.jpeg")


    if (document.cookie.match(/^(.*;)?\s*userid\s*=\s*[^;]+(.*)?$/)) {
        window.location.href = "/login";

    }

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