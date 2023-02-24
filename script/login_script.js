function addTextField(id){
    // Get the element where the inputs will be added to
    var container = document.getElementById(id);
    // Append a node with a random text
    var x = document.createElement("INPUT");
    x.name="text"
    x.placeholder="text"
    x.style.backgroundColor="yellow"
    container.append(x);
}
function addNumberField(id){
    // Get the element where the inputs will be added to
    var container = document.getElementById(id);
    // Append a node with a random text
    var x = document.createElement("INPUT");
    x.name="number"
    x.placeholder="number"
    x.style.backgroundColor="blue"
    container.append(x);
}

function addFuncField(id){
    // Get the element where the inputs will be added to
    var container = document.getElementById(id);
    // Append a node with a random text
    var x = document.createElement("INPUT");
    x.name="function"
    x.placeholder="function"
    x.style.backgroundColor="orange"
    container.append(x);
}
function removeField(id){
    // Get the element where the inputs will be added to
    var container = document.getElementById(id);
    // Append a node with a random text
    container.removeChild(container.lastChild)
}
function clearInput(id){
    removeAll(id)
    document.getElementById(id).innerText="input: "
}
function removeAll(id){
    var container = document.getElementById(id);
    while (container.lastChild!=null)
        container.removeChild(container.lastChild)
}

function show_result(message,result_id){
    //clear all
    result=document.getElementById(result_id)
    removeAll(result_id)
    result.innerText="result: "
    //display result
    for (let i=0;i<message.length;i++){
        text=message[i]
        if (text[0]=="#"){
            let e=document.createElement("img")
            e.src="temp/"+text.substring(1)
            e.width="200"
            e.height="200"
            result.append(e)
        }
        else{
            let e=document.createElement("p")
            e.innerHTML="text: "+text
            result.append(e)
        }
    }
}


function send(){
    const json=[]
    var prompt=document.getElementById("prompt_un")
    //clear text
    prompt.innerText=""
    var container = document.getElementById("container_un");
    for (node of container.childNodes){
        if(node.name=="text"){
            if(node.value==""){
                prompt.innerText="Some Field is empty"
                return
            }
            json.push(node.value+"::str");
        }
        else if (node.name=="function"){
            if(node.value==""){
                prompt.innerText="Some Field is empty"
                return
            }
            json.push(node.value+"::fun");
        }
        else if (node.name=="number"){
            if(node.value==""){
                prompt.innerText="Some Field is empty"
                return
            }
            json.push(node.value+"::number");
        }
    }
    makeRequest('POST','/UniApp',JSON.stringify(json))
    .then(function(result){
        show_result(JSON.parse(result),"result_un")
    })
    .catch(function(result){
        console.log("error")
    })
}

function makeRequest (method,url,text) {
    return new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open(method,url,true)
      xhr.setRequestHeader("Content-Type", "application/json")
      xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(xhr.responseText);
        } else {
          reject({
            status: xhr.status,
            statusText: xhr.statusText
          });
        }
      };
      xhr.onerror = function () {
        reject({
          status: xhr.status,
          statusText: xhr.statusText
        });
      };
      xhr.send(text);
    });
}

function ongoing(){
    const json=[]
    var prompt=document.getElementById("prompt_on")
    //clear text
    prompt.innerText=""
    var container = document.getElementById("container_on");
    for (node of container.childNodes){
        if(node.name=="text")
        {
            if(node.value==""){
                prompt.innerText="Some Field is empty"
                return
            }
            json.push(node.value+"::str");
        }
        else if (node.name=="function")
        {
            if(node.value==""){
                prompt.innerText="Some Field is empty"
                return
            }
            json.push(node.value+"::fun");
        }
        else if (node.name=="number")
        {
            if(node.value==""){
                prompt.innerText="Some Field is empty"
                return
            }
            json.push(node.value+"::number");
        }
    }
    console.log(json)
    console.log(JSON.stringify(json))
    makeRequest('POST','/ongoing',JSON.stringify(json))
    .then(function(result){
        return makeRequest('GET','/ongoing',"")
    })
    .then(function(result){
        console.log(JSON.parse(result))
        show_result(JSON.parse(result),"result_on")
    })
    .catch(function(result){
        console.log("error")
    })
}