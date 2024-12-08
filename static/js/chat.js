const djangoData = document.getElementById('django-data');


const themeToggleBtn = document.getElementById('theme-toggle');
const sunIcon = document.getElementById('sun-icon');
const moonIcon = document.getElementById('moon-icon');
const body = document.body;

themeToggleBtn.addEventListener('click', () => {
	// Toggle between light and dark theme
	body.classList.toggle('dark');
	
	// Toggle visibility of the sun and moon icons
	sunIcon.classList.toggle('hidden');
	moonIcon.classList.toggle('hidden');
});

// New Chat Button Logic
const newChatBtn = document.getElementById('new-chat-btn');
const chatInput = document.getElementById('chat-input');
const chatOutput = document.getElementById('chat-output');

newChatBtn.addEventListener('click', () => {
	// Clear chat output and input
	// chatOutput.innerHTML = '';
	// chatInput.value = '';

	// // Optionally toggle theme when New Chat is clicked as well
	// body.classList.toggle('dark');
	// sunIcon.classList.toggle('hidden');
	// moonIcon.classList.toggle('hidden');
	const token = getCookie('csrftoken');
	alert(token)

	fetch("/chat/new", {
		method: 'POST',
		headers: {
			'X-CSRFToken': token
		},
		body : new FormData()
	})
	.then(res => res.json())
	.then(async (data) => {
		console.log(data)
		if(data.status){
			console.log(data)
			alert(data)
			location.href = "/chat/session/" + data.session_id;
		}
		else{
			alert("error occured!");
		}
	})
	.catch(error => {
		alert('hhh' + error);
	});
});

// Chat Input and Output Logic
const sendBtn = document.getElementById('send-btn');

function answerDiv(){
	const answerDiv = document.createElement('div');
	answerDiv.classList.add('bg-gray-100', 'dark:bg-gray-800', 'text-gray-800', 'dark:text-white', 'p-2', 'rounded-lg', 'my-2');
	answerDiv.textContent = '🤖 : ';
	return answerDiv;
}
sendBtn.addEventListener('click', () => {
	const page = djangoData.getAttribute('data-page');
	const query = chatInput.value.trim();

	if(page == 'home'){
		const formData = new FormData();
		formData.append('query', query);
		try{
			fetch("/chat/new", {
				method: 'POST',
				body: formData
			})
			.then(res => res.json())
			.then((res) => {
				if (res.status) {
					const session_id = res.session_id;
					location.href = "/chat/session/" + session_id;
				}				
			})
			.catch(error => {
				alert(str(error));
			});
		}catch(err){
			alert(str(err))
		}
	}
	if(page == 'chat'){
		const session_id = djangoData.getAttribute('data-session');
		ask_query(query, session_id);
	}

	
});

const ask_query = (query, session_id) => {
	const queryDiv = document.createElement('div');
	queryDiv.classList.add('bg-gray-200', 'dark:bg-gray-700', 'text-gray-800', 'dark:text-white', 'p-2', 'rounded-lg', 'my-2');
	queryDiv.textContent = '😎 : ' + query;
	chatOutput.appendChild(queryDiv);

	const formData = new FormData();
	formData.append('query', query);
	formData.append('session_id', session_id);
	const answer = answerDiv();
	try{
		fetch("/ask", {
			method: 'POST',
			body: formData,
		})
		.then(async (res) => {
			if (!res.ok) {
				answer.textContent +='Server Backend Error';
				return;
			}
		
			const reader = res.body.getReader();  // Get the reader from the stream
			const decoder = new TextDecoder('utf-8');  // Decoder to convert bytes to text
			
			console.log('werwerwer')
			let done = false;
		
			// Process the stream in chunks
			while (!done) {
				const { value, done: streamDone } = await reader.read();
				done = streamDone;
		
				// Decode the current chunk of data and append it to the text
				let piece = decoder.decode(value, { stream: true });
				if(piece == 'None' || piece == '') continue;
				answer.textContent += piece;
		
			}
			
		})
		.catch(error => {
			console.log(error)
			answer.textContent +="I am sorry, there is some problem with server host!";
		});
	}catch(err){
		answer.textContent +="I am sorry, there is some problem with network, Plz try again after confirming network state!";
	}
	chatOutput.appendChild(answer);
	chatInput.value = '';
}


function deleteSession(deleteBt){
	const formData = new FormData();
	formData.append('session_id', deleteBt.parentElement.getAttribute('data-session_id'));
	try{
		fetch("/delete-session", {
			method: 'POST',
			body: formData,
		})
		.then(res => res.json())
		.then(async (res) => {
			if(res.status){
				deleteBt.parentElement.remove();
			}		
		})
		.catch(error => {
			
		});
	}catch(err){
		;
	}
}