const djangoData = document.getElementById('django-data');
const about = document.getElementById('about');
const botTitle = document.getElementById('bot-title');

const newChatBtn = document.getElementById('new-chat-btn');
const chatInput = document.getElementById('chat-input');
const chatOutput = document.getElementById('chat-output');

newChatBtn.onclick = () => {
	location.href = '/home';
}

if(djangoData.getAttribute('data-page') == 'chat'){
	const assistantMsgs = document.querySelectorAll('[role="assistant"]');
	assistantMsgs.forEach(span => {
		span.innerHTML = marked.parse(span.innerHTML);
	});

}


const sendBtn = document.getElementById('send-btn');

function answerDiv(){
	const div = document.createElement('div');
	div.classList.add('text-white', 'p-2', 'my-2', 'flex-1', 'flex');

	const img = document.createElement('img');
	img.src = '/static/png/bot.png';
	img.classList.add('rounded-full', 'w-10', 'h-10', 'mr-2');

	const span = document.createElement('span');
	span.classList.add('mr-0');
	span.innerHTML = 'Bot <br>'

	div.appendChild(img);
	div.appendChild(span);

	return div;
}
function appendQuery(query, parent){
	const htmlString = `
		<div class="text-white p-2 my-2 flex-1 flex">
			<img src="/static/png/you.jpg" class="rounded-full w-10 h-10 mr-2" />
			<span class="mr-0">You<br>
				${query}
			</span>
		</div>
	`;

	parent.insertAdjacentHTML('beforeend', htmlString);
}

sendBtn.addEventListener('click', async() => {
	const page = djangoData.getAttribute('data-page');
	const query = chatInput.value.trim();
	appendQuery(query, chatOutput);
	const answer = answerDiv();
	let answerMarkdown = '';
	const answerSpan = answer.children[1];
	chatOutput.append(answer);

	if(page == 'home'){
		if (botTitle.classList.contains('hidden')) {
			botTitle.classList.remove('hidden');
		}

		about.hidden = 'true';
		const formData = new FormData();
		formData.append('query', query);
		try{
			fetch("/chat/new", {
				method: 'POST',
				body: formData,
			})
			.then(async (res) => {
				if (!res.ok) {
					answerSpan.innerHTML +='Server Backend Error';
					return;
				}
			
				const reader = res.body.getReader();
				const decoder = new TextDecoder('utf-8');
				
				console.log('werwerwer')
				let done = false;
			
				// Process the stream in chunks
				while (!done) {
					const { value, done: streamDone } = await reader.read();
					done = streamDone;
			
					// Decode the current chunk of data and append it to the text
					let piece = decoder.decode(value, { stream: true });
					if(piece == 'None' || piece == '') continue;
					answerMarkdown += piece;
					answerSpan.innerHTML = marked.parse(answerMarkdown);
			
				}
				fetch('/getnewsession', {
					method: 'GET'
				})
				.then(res => res.json())
				.then((res) => {
					if(res.status){
						location.href = '/chat/session/' + res.session_id;
						return;
					}
				})
				
			})
			.catch(error => {
				console.log(error)
				answerSpan.innerHTML +="I am sorry, there is some problem with server host!";
			});
		}catch(err){
			alert(str(err))
		}
	}
	if(page == 'chat'){
		const session_id = djangoData.getAttribute('data-session');
		ask_query(query, session_id, answerSpan);
	}
});

const ask_query = (query, session_id, answerSpan) => {
	const formData = new FormData();
	formData.append('query', query);
	formData.append('session_id', session_id);
	try{
		let answerMarkdown = '';
		fetch("/ask", {
			method: 'POST',
			body: formData,
		})
		.then(async (res) => {
			if (!res.ok) {
				answerSpan.innerHTML +='Server Backend Error';
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
				answerMarkdown += piece;
				answerSpan.innerHTML = marked.parse(answerMarkdown);
		
			}
			
		})
		.catch(error => {
			console.log(error)
			answerSpan.innerHTML +="I am sorry, there is some problem with server host!";
		});
	}catch(err){
		answerSpan.innerHTML +="I am sorry, there is some problem with network, Plz try again after confirming network state!";
	}
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