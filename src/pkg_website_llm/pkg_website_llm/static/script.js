document.documentElement.lang == "de";
console.log("Deutsche Sprache ist aktiviert")
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('send-btn').addEventListener('click', function () {

        var imageElement_Pack = document.getElementById('image_Pack');
        imageElement_Pack.src = "";

        var userInput = document.getElementById('user-input').value;
        var communication_form = document.getElementById('dropdown-menu').value;

        var selected_language = document.documentElement.lang;
        
        response_llm = ""

        if (userInput.trim() !== '') {
            addMessage(userInput, 'user');
            document.getElementById('user-input').value = '';
        } else {
            userInput = "";
        }

        let data_request = { user_input: userInput , communication_form: communication_form, selected_language: selected_language};
        console.log(data_request);
        fetch('/button_click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data_request)

        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);

                let response_llm = {
                    received: JSON.stringify(data.received)
                };

                // Überprüfen, ob response_llm.received definiert und ein Array ist
                if (response_llm.received && Array.isArray(response_llm.received)) {
                    let formattedMessage = response_llm.received.join(', ');
                    addMessage(formattedMessage, 'bot');
                }
                else if (response_llm.received && !Array.isArray(response_llm.received)) {
                    let formattedMessage = response_llm.received.replace(/[\[\]\"',]/g, '')
                    addMessage(formattedMessage, 'bot');

                }
                else {
                    addMessage('Diese Objekte werden gepackt: Keine Objekte', 'bot');
                    console.error('response_llm.received ist kein Array oder nicht definiert:', response_llm.received);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });

        // Simulate bot response
        setTimeout(function () {
            if (document.documentElement.lang == "de"){
                addMessage('Das LLM bearbeitet gerade ihre Anfrage!', 'bot');
            } else {
                addMessage('The LLM is currently processing your request!', 'bot');
            }
        }, 1000);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('approve-btn').addEventListener('click', function () {
        data = "approve"

        fetch('/button_approve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: data
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);

                console.error('Error:', error);
            })
            .catch((error) => {
            });

        // Simulate bot response
        setTimeout(function () {
            if (document.documentElement.lang == "de"){
                addMessage('Auswahl wurde bestätigt und wird bearbeitet!', 'bot');
            }
            else {
                addMessage('Selection has been confirmed and is being processed!', 'bot');
            }
        }, 1000);
    });
});


document.addEventListener('DOMContentLoaded', function () {
document.getElementById("language-toggle").addEventListener("click", function () {
    // Aktuelle Sprache herausfinden
    const currentLanguage = document.documentElement.lang;
    

    const BoxBild = document.getElementById('BoxBild'); 
    const PackBild = document.getElementById('pack_heading');
    const Tabelle_Pack = document.getElementById('myTable').querySelector("thead th:first-child");
    const Tabelle_Pack_Zylinder = document.getElementById('myTable').querySelector("thead th:nth-child(2)");
    const Tabelle_Node = document.getElementById('NodeTable').querySelector("thead th:first-child");

    const user_input = document.getElementById('user-input');

    const AblehnenBtn = document.getElementById('disapprove-btn');
    const Bestätigen = document.getElementById('approve-btn');

    const senden = document.getElementById('send-btn');

    const option1 = document.getElementById('option1');
    const option2 = document.getElementById('option2');
    const option3 = document.getElementById('option3'); 

    const footer_1 = document.getElementById('footer_1');
    const footer_2 = document.getElementById('footer_2');
    const footer_3 = document.getElementById('footer_3');


    // Sprache wechseln
    if (currentLanguage === "en") {
        console.log("Umgestellt auf Deutsche Sprache")
        BoxBild.textContent = "Detektierte Objekte ";
        PackBild.textContent = "Berechneter Packplan ";
        Tabelle_Pack.textContent = "Pack Reihenfolge";
        Tabelle_Pack_Zylinder.textContent = "Zylinder IDs";
        Tabelle_Node.textContent = "Laufende Nodes";
        AblehnenBtn.textContent = "Ablehnen";
        Bestätigen.textContent = "Bestätigen";
        senden.textContent = "Senden";
        user_input.placeholder = "Ihre Nachricht eingeben...";

        option1.textContent = "Chat";
        option2.textContent = "Szenenchat";
        option3.textContent = "Befehl";

        footer_1.textContent = "Forschung & Entwicklungsprojekt 2";
        footer_2.textContent = "Von Raphael Aberle, Andreas Schmitt, Leo Schäfer, Maurice Droll und Eshan Savla";
        footer_3.textContent = "Hochschule Karlsruhe";


        document.getElementById('InitialMessage').innerHTML = 'Hallo, Ich bin das AIP-LLM! <br> Ich kenne die detektierten Objekte sowie deren Gewicht und Abmessungen und ich kann dir Fragen dazu beantworten.<br> Wähle hierzu im Drop-Down die passende Option ("Chat" oder "Szenenchat"). <br> Mit der Option "Szenenchat" nutzt das LLM Kontextinformationen der detektierten Objekte, die Option "Chat" kennt diese nicht. <br> Wenn du direkt Objekte packen möchtest dann nutze "Befehl".';

        document.documentElement.lang = "de";
        this.textContent = "Englisch";
        this.src = "england-flagge.png"

    } else {
        console.log("Umgestellt auf Englische Sprache");

        BoxBild.textContent = "Image of Box Content";
        PackBild.textContent = "Pack Planning";
        Tabelle_Pack.textContent = "Packing Sequence";
        Tabelle_Pack_Zylinder.textContent = "Cylinder IDs";
        Tabelle_Node.textContent = "Running Nodes";
        AblehnenBtn.textContent = "Reject";
        Bestätigen.textContent = "Confirm";
        senden.textContent = "Send";
        user_input.placeholder = "Please type in your request...";

        option1.textContent = "Chat";
        option2.textContent = "Scene chat";
        option3.textContent = "Command";

        footer_1.textContent = "Research & Development Project 2";
        footer_2.textContent = "By Raphael Aberle, Andreas Schmitt, Leo Schäfer, Maurice Droll and Eshan Savla";
        footer_3.textContent = "Karlsruhe University of Applied Sciences";

        document.documentElement.lang = "en";
        this.textContent = "German";
        this.src = "german_flag.png"

        document.getElementById('InitialMessage').innerHTML = 'Hello, I am the LLM-AIP! <br> I have information on the detected objects, their dimensions and their weight and I can answer your questions. <br> Select the appropriate option in the drop-down menu (‘Chat’ or ‘Scene chat’).<br> With the ‘Scene chat’ option, the LLM uses context information of the detected objects; the ‘Chat’ option does not use the context info.<br> If you want to pack objects directly then use ‘Command’.';

    }
});
});


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('disapprove-btn').addEventListener('click', function () {
        data = "disapprove"

        fetch('/button_disapprove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: data
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);

                console.error('Error:', error);
            })
            .catch((error) => {
            });

        // Simulate bot response
        setTimeout(function () {
            if (document.documentElement.lang == "de"){
                addMessage('Auswahl wurde abgelehnt!', 'bot');
            } else{
                addMessage('Selection has been rejected!', 'bot');
            }
        }, 1000);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Funktion, um die Daten vom Flask-Backend abzurufen
    async function fetchData() {
        try {
            const response = await fetch('/get_data');
            const data = await response.json();

            updateNodeList(data);
            updateTable(data);

        } catch (error) {
            console.error('Fehler beim Abrufen der Daten:', error);
        }
    }

    setInterval(fetchData, 10000);
    setInterval(updateImage, 3000); 


    fetchData();
});



function updateNodeList(data) {
    const tbody = document.querySelector('#NodeTable tbody');
    tbody.innerHTML = ''; 

    const nodeList = data.node_list.split(', ');

    for (let i = 0; i < nodeList.length; i += 2) {
        const row = document.createElement('tr');
        tbody.appendChild(row);

        const cellKey = document.createElement('td');
        cellKey.innerText = nodeList[i].replace(/[\['\]]/g, '');
        row.appendChild(cellKey);

        const cellValue = document.createElement('td');
        // Überprüfen Sie, ob ein zweites Element vorhanden ist, um ein leeres Feld zu vermeiden
        if (i + 1 < nodeList.length) {
            cellValue.innerText = nodeList[i + 1].replace(/[\['\]]/g, '');
        }
        row.appendChild(cellValue);
    }
}


function submitFormOnEnter(event) {
    if (event.key === 'Enter') {
        document.getElementById('send-btn').click();
    }
}


function addMessage(text, sender) {
    var message = document.createElement('div');
    message.className = 'message ' + (sender === 'user' ? 'user-message' : 'bot-message');
    message.textContent = text;

    var chatBox = document.getElementById('chat-box');
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Funktion, um die Tabelle mit den abgerufenen Daten zu aktualisieren
function updateTable(data) {
    const tbody = document.querySelector('#myTable tbody');
    tbody.innerHTML = ''; // Lösche vorhandene Tabellenzeilen


    console.log(data.package_content);
    console.log(data.cylinder_ids);

    const itemList = data.package_content;
    const additionalContent = data.cylinder_ids;

    if (Array.isArray(itemList)){

        for (i in itemList) {
            //alert(itemList[i])
            const row = document.createElement('tr');
            tbody.appendChild(row);
            const cellKey = document.createElement('tr');
            cellKey.innerText = itemList[i];
            row.appendChild(cellKey);

            // Zweite Spalte
            const cellValue = document.createElement('td');
            if (additionalContent[i] == undefined) {
                additionalContent[i] = ""
            }
            cellValue.innerText = additionalContent[i];
            row.appendChild(cellValue);

        }
    } 
    else{
        const row = document.createElement('tr');
        tbody.appendChild(row);
        const cellKey = document.createElement('tr');
        cellKey.innerText = "NO DATA";
        row.appendChild(cellKey);
    }
}

// Funktion, um das Bild zu aktualisieren
function updateImage() {

    fetchData()
    async function fetchData() {
    try {

        var imageElement_Pack = document.getElementById('image_Pack');
        let timestamp = new Date().getTime();
        imageElement_Pack.src = `${"PackPlanBild.png"}?t=${timestamp}`;
        //imageElement_Pack.src = "PackPlanBild.png";
        var imageElement_Box = document.getElementById('image');
        imageElement_Box.src = `${"Hintergrund.png"}?t=${timestamp}`;
        //imageElement_Box.src = "Hintergrund.png";

        const response = await fetch('/get_data');
        const data = await response.json();
        var packplanning_name = document.getElementById('pack_heading_text');

        if (data.feedback_string !== 'No String'){
            console.log(data.feedback_string);
            if (packplanning_name.innerText.includes("Alle Pakete werden gepackt")){
                packplanning_name.innerText = packplanning_name.innerText;
            } else{
                packplanning_name.innerText = packplanning_name.innerText + "\n" + data.feedback_string;
            }
    }

    
    } catch (error) {
        console.error('Fehler beim Abrufen der Daten:', error);
    }    }
    }

