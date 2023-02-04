window.onload = buildDummy();

function buildDummy() {
    profileButton("Bob Ross", "420.69", "/bobross.jpeg")
}

function profileButton(name, balance, profilePicUrl) {
    const userBalance  = document.createTextNode('balance');
    const userName = document.createElement('name');
    const node = document.createElement('');
    const profilePic = document.createElement('pfp')
    const img = document.createElement("img");
    img.src = profilePicUrl;
    profilePic.document.append(img);
    userName.document.append(name);
    userBalance.document.append(balance);
    document.getElementById("profile").insertAdjacentElement('beforeBegin', node);
}