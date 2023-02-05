const api_url ="http://127.0.0.1:2025/";
  
// Defining async function
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


