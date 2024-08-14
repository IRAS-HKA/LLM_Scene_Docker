document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('send-btn').addEventListener('click', function () {
        var userInput = document.getElementById('user-input').value;
        var communication_form = document.getElementById('dropdown-menu').value;
        
        response_llm = ""

        if (userInput.trim() !== '') {
            addMessage(userInput, 'user');
            document.getElementById('user-input').value = '';
        } else {
            userInput = "";
        }

        let data_request = { user_input: userInput , communication_form: communication_form};
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
                console.error("FUCKKKKKKK")
                console.error('Error:', error);
            });

        // Simulate bot response
        setTimeout(function () {
            addMessage('Das LLM bearbeitet gerade ihre Anfrage!', 'bot');

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
            addMessage('Auswahl wurde bestätigt und wird bearbeitet!', 'bot');

        }, 1000);
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
            addMessage('Auswahl wurde abgelehnt!', 'bot');

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

    // Rufe fetchData alle 10 Sekunden auf
    setInterval(fetchData, 10000);
    // Aktualisiere das Bild alle 10 Sekunden
    setInterval(updateImage, 10000); // 10000 ms = 10 Sekunden

    // Initialer Datenabruf beim Laden der Seite
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
    var imageElement_Pack = document.getElementById('image_Pack');
    var imageElement_Box = document.getElementById('image');
    imageElement_Pack.src = "PackPlanBild.png";
    imageElement_Box.src = "Hintergrund.png";
    // async function fetchData() {
    //     try {
    //         const response = await fetch('/get_data');
    //         const data = await response.json();


    //         var imageElement = document.getElementById('image');
    //         var currentSrc = data.picture;

    //         // Logik, um die neue Bildquelle festzulegen
    //         // Hier ein einfaches Beispiel, das den Query-Parameter ändert, um den Cache zu umgehen
    //         var newSrc = currentSrc.split('?')[0] + '?' + new Date().getTime();
            
    //         imageElement.src = "PackPlanBild.png";
            


    //         //}
    //     } catch (error) {
    //         console.error('Fehler beim Abrufen der Daten:', error);
    //     }


    // }
}

