const api_url = 
      "http://127.0.0.1:2025/";
  
// Defining async function
async function getapi(url) {
    
    // Storing response
    const response = await fetch(url+'api/producer/locker/estimate?' + new URLSearchParams({
        start_locker: 1,
        end_locker: 2,
    }));
    
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    show(data);
    
}
// Calling that async function
getapi(api_url);

function show(data){
    let a = "This product will be delivered by: ";

    for(let r of data.list){
        a += r.deliveryTime;
    }

    document.getElementById("html_delivery_time") = a;

    



}

