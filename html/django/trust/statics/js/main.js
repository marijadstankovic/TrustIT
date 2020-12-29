<script>	
	const dateControl = document.querySelector('input[type="date"]');
	console.log(dateControl);
	const txtTitle = document.getElementById("txtTitle");
	const txtText = document.getElementById("txtText");
	const btnNext = document.getElementById("example");
	console.log(txtTitle)
	console.log(txtText)
	console.log(btnNext)
	btnNext.onclick = ev => {
		let url = "/pr";
		let date=dateControl.value;
		let title=txtTitle.value;
		let text=txtText.value;
		if (!date) {
		alert("Date is not defined.");
		}
		else if (!title) {
			alert("Title is not defined.");
		}
		else if (!text) {
			alert("Text is not defined.");
		}
		else
		{
				let formData= new FormData();
				formData.append('date', date);
				formData.append('title', title);
				formData.append('text', text);


			let fetchData = {
				method: 'POST',
				body: formData
			}

			fetch(url, fetchData)
			.then(response => {
				if (!response.ok)
					throw Error(response.statusText);
				return response.json();
			})
			.catch(error =>
			{
				console.log(error);
			})
		}
	}
</script>