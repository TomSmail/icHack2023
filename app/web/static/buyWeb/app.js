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
}
// Calling that async function
getapi(api_url);