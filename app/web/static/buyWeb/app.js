const api_url ="http://127.0.0.1:2025/";
  
// Defining async function

async function buy() {
    const data = {
         "start_locker": 6,
         "end_locker": 7  
    } 
    
    const response = await fetch(api_url + "api/producer/parcel/create", {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
     
    if (response.ok) {
        alert("The item was purchased!")
    }
    else {
        alert("An error occurred in purchasing the item.")
    }

}


async function getapi(url) {
    
    // Storing response
    const response = await fetch(url + 'api/producer/locker/estimate?' + new URLSearchParams({
        start_locker: 6,
        end_locker: 7,
    }));
    
    // Storing data in form of JSON
    var data = await response.json();
    document.getElementById("html_delivery_time").textContent = data.deliveryTime;    
}
// Calling that async function
getapi(api_url);


