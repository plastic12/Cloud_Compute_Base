function addTextField(){
    // Get the element where the inputs will be added to
    var container = document.getElementById("container");
    // Append a node with a random text
    var x = document.createElement("INPUT");
    x.name="text"
    x.placeholder="text"
    x.style.backgroundColor="yellow"
    container.append(x);
}
function addNumberField(){
    // Get the element where the inputs will be added to
    var container = document.getElementById("container");
    // Append a node with a random text
    var x = document.createElement("INPUT");
    x.name="number"
    x.placeholder="number"
    x.style.backgroundColor="blue"
    container.append(x);
}

function addFuncField(){
    // Get the element where the inputs will be added to
    var container = document.getElementById("container");
    // Append a node with a random text
    var x = document.createElement("INPUT");
    x.name="function"
    x.placeholder="function"
    x.style.backgroundColor="orange"
    container.append(x);
}
function removeField(){
    // Get the element where the inputs will be added to
    var container = document.getElementById("container");
    // Append a node with a random text
    container.removeChild(container.lastChild)
}
function removeAll(){
    var container = document.getElementById("container");
    while (container.lastChild!=null)
        container.removeChild(container.lastChild)
}

function send(){
    const json=[]
    var prompt=document.getElementById("prompt")
    //clear text
    prompt.innerText=""
    var container = document.getElementById("container");
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
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //clear result
            result=document.getElementById("result")
            while (result.lastChild!=null)
                result.removeChild(result.lastChild)
            let json=JSON.parse(xhttp.responseText)
            console.log(json)
            //display result
            label=document.createElement("p")
            label.innerHTML="Result: "
            result.append(label)
            for (let i=0;i<json.length;i++){
                text=json[i]
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
    };
    xhttp.open("POST","",true)
    xhttp.setRequestHeader("Content-Type", "application/json")
    xhttp.send(JSON.stringify(json));
    
}