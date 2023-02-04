function profileButton(name, balance, profilePicUrl) {
    const userBalance  = document.createTextNode(balance)
    const userName = document.createTextNode(name);
    const node = document.createElement()
    node.append(userBalance)
    document.getElementById("profile").insertAdjacentElement('beforeBegin', node);
}