window.onload = getprofiledata();


async function getprofiledata() {


    resp = await fetch('api/distributor/user/info')

    console.log(resp)


    fetch('api/distributor/user/info')
        .then(
            response => {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                        response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                    console.log(data);
                    profileButton(data["username"], data["balance"], data["pfpUrl"])

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

    //document.getElementById("profile").insertAdjacentElement('beforeBegin', node);
}