const resultDiv = document.querySelector('#post_text');

SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;
let recognition = new SpeechRecognition();

recognition.lang = 'ja-JP';
recognition.interimResults = true;
recognition.continuous = true;

let finalTranscript = ''; // 確定した(黒の)認識結果

recognition.onresult = (event) => {
  let interimTranscript = ''; // 暫定(灰色)の認識結果
  let finalTranscript = ''; // 確定した(黒の)認識結果
  for (let i = event.resultIndex; i < event.results.length; i++) {
    let transcript = event.results[i][0].transcript;
    if (event.results[i].isFinal) {
      finalTranscript = transcript;
    } else {
      interimTranscript = transcript;
    }
  }
  post_text.value =interimTranscript + finalTranscript;

  if(finalTranscript.endsWith('な')||finalTranscript.endsWith('ね')){
    //タスクを追加する処理
    console.log(post_text.value)

  }
}
//ページが読み込まれたら音声認識を開始
recognition.start();

// https://developer.mozilla.org/ja/docs/Learn/JavaScript/Client-side_web_APIs/Fetching_data

// CSRF対策
const getCookie = (name) => {
  if (document.cookie && document.cookie !== '') {
    for (const cookie of document.cookie.split(';')) {
      const [key, value] = cookie.trim().split('=')
      if (key === name) {
        return decodeURIComponent(value)
      }
    }
  }
}
const csrftoken = getCookie('csrftoken')

//ここからVue
const App = {
	data() {
	  return {
	    task: {title: ''},
	    task: {indent:''},
	    tasks:['HTMLより'],
	  }
	  },
	compilerOptions: {
	    delimiters: ['[[', ']]'],
	},
	methods: {
		sendRequest(url, method, data){
			const csrftoken = Cookies.get('csrftoken');
			const myHeaders = new Headers({
			    'Content-Type': 'application/json',
			});
			if(method !== 'get'){
			    myHeaders.set('X-CSRFToken', csrftoken)
			};
	    
			fetch(url, {
			    method: method,
			    headers: myHeaders,
			    body: data,
			})
			.then((response) => {
			    return response.json();
			})
			.then((response) => {
			    if (method == 'get') {
				this.tasks = response;
			    };
			    if (method == 'post') {
				this.task.title = ''
				this.getTasks();
			    };
			    if (method == 'put') {
				this.getTasks();
			    };
			    if (method == 'put' || method == 'delete') {
				this.getTasks();
			    };
			})
			.catch(error => {
			    console.error('There has been a problem with your fetch operation:', error);
			});
		},
		getTasks(){
			this.sendRequest(URL, 'get');
		},
		createTask(){
			this.getTasks();
			this.sendRequest(URL, 'post',JSON.stringify(this.task));
		},
		updateTask(task){
			this.getTasks();
			this.sendRequest(URL, 'put',JSON.stringify(task));
		},
		deleteTask(task){
			this.getTasks();
			this.sendRequest(URL, 'delete',JSON.stringify(task));
		},
	created() {
	  	this.getTasks();
	},

	onInput(e, task) {
		item.value = e.target.innerText;
	},
	onTab(task, index) {
		task.indent++;
	}

      },
}
Vue.createApp(App).mount('#app')