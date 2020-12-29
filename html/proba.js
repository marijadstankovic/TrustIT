

document.body.onload = function ()
{
    const dugme1 = document.getElementById("dugme");
	data = "kuj ce toj da znaje"
    dugme1.onclick = function ()
    {
		console.log("zovem python")
		
		let fetchData = {
			method: 'POST',
			headers: {"Access-Control-Allow-Origin": "*",
			'Access-Control-Allow-Headers': "*"},
			//mode:'no-cors',
        //body: formData,
			//body: JSON.stringify(data)
		}
		
		
		fetch('http://127.0.0.1:5000/proba', fetchData)
		.then(response => {
			console.log(response);
        if (!response.ok)
            throw Error(response.statusText);
		}).catch(error =>
		{
			console.log(error);
		})
        //zovemo python scriptu
		/*$.post( "proba.py", function( data ) {
		alert( "Data Loaded: " + data );
		});*/
	}
    
}

function callbackFunc(response) {
	console.log("python odgovorio")
	const dvi = document.getElementById("divic")
	console.log(response);
	dvi.innerHTML = response
}