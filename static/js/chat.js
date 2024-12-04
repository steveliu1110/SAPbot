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
	chatOutput.innerHTML = '';
	chatInput.value = '';

	// Optionally toggle theme when New Chat is clicked as well
	body.classList.toggle('dark');
	sunIcon.classList.toggle('hidden');
	moonIcon.classList.toggle('hidden');
});

// Chat Input and Output Logic
const sendBtn = document.getElementById('send-btn');

function createGptBox(){
	const answerDiv = document.createElement('div');
	answerDiv.classList.add('bg-gray-100', 'dark:bg-gray-800', 'text-gray-800', 'dark:text-white', 'p-2', 'rounded-lg', 'my-2');
	answerDiv.textContent = '🤖 : ';
	return answerDiv;
	// chatOutput.appendChild(answerDiv);
	// chatInput.value = '';
}
sendBtn.addEventListener('click', () => {
	const query = chatInput.value.trim();
	if (query) {
		const queryDiv = document.createElement('div');
		queryDiv.classList.add('bg-gray-200', 'dark:bg-gray-700', 'text-gray-800', 'dark:text-white', 'p-2', 'rounded-lg', 'my-2');
		queryDiv.textContent = '😎 : ' + query;
		chatOutput.appendChild(queryDiv);

		const formData = new FormData();
		formData.append('query', query);
		const gptBox = createGptBox();
		try{
			fetch("/ask", {
				method: 'POST',
				body: formData,
			})
			.then(async (res) => {
				// if (data.status) {
				//     appendAnswer(data.answer)
				//     chatInput.value = '';  // Clear input field after sending    
	
				// } else {
				//     appendAnswer("I am sorry, there is some problem with api, Plz try again later!");
				// }
				if (!res.ok) {
					console.error('Request failed with status', res.status);
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
					gptBox.textContent += piece;
			
				}
				
			})
			.catch(error => {
				console.log(error)
				gptBox.textContent +="I am sorry, there is some problem with server host!";
			});
		}catch(err){
			gptBox.textContent +="I am sorry, there is some problem with network, Plz try again after confirming network state!";
		}
		chatOutput.appendChild(gptBox);
		chatInput.value = '';
	}
});