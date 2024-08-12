document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('send-btn').addEventListener('click', function () {
        var userInput = document.getElementById('user-input').value;
        response_llm = ""

        if (userInput.trim() !== '') {
            addMessage(userInput, 'user');
            document.getElementById('user-input').value = '';
        } else {
            userInput = "";
        }

        let data = { user_input: userInput };

        fetch('/button_click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
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
                console.error(data)
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

        setTimeout(function () {
            addMessage('Auswahl zu Packalgorithmus übermittelt!', 'success');

        }, 5000);
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

            //list_object = [package_content, cylinder_ids, grasp_pose, place_pose]

            //document.getElementById("package_content").innerText = data["package_content"];
            //document.getElementById("cylinder_ids").innerText = data["cylinder_ids"];

            //document.getElementById("grasp_pose").innerText = data["grasp_pose"];
            //document.getElementById("place_pose").innerText = data["place_pose"];

            // Aktualisiere die Tabellenzellen mit den abgerufenen Daten
            //for (const key in data) {
            //if (data.hasOwnProperty(key)) {
            //    document.getElementById(key).innerText = data[key];
            //}

            updateTable(data);



            //}
        } catch (error) {
            console.error('Fehler beim Abrufen der Daten:', error);
        }
    }

    // Rufe fetchData alle 10 Sekunden auf
    setInterval(fetchData, 10000);

    // Initialer Datenabruf beim Laden der Seite
    fetchData();
});


function submitFormOnEnter(event) {
    if (event.key === 'Enter') {
        document.getElementById('send-btn').click();
    }
}


function addMessage(text, sender) {
    var message = document.createElement('div');
    message.className = 'message ' + (sender === 'user' ? 'user-message' : 'bot-message');
    message.className = 'message ' + (sender === 'success' ? 'sucess-message' : 'bot-message');
    message.textContent = text;

    var chatBox = document.getElementById('chat-box');
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Funktion, um die Tabelle mit den abgerufenen Daten zu aktualisieren
function updateTable(data) {
    const tbody = document.querySelector('#myTable tbody');
    tbody.innerHTML = ''; // Lösche vorhandene Tabellenzeilen

    const itemList = data.package_content.split(', ');
    const additionalContent = data.cylinder_ids.split(' ');


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

// Funktion, um das Bild zu aktualisieren
function updateImage() {
    async function fetchData() {
        try {
            const response = await fetch('/get_data');
            const data = await response.json();


            var imageElement = document.getElementById('image');
            var currentSrc = data.picture;

            // Logik, um die neue Bildquelle festzulegen
            // Hier ein einfaches Beispiel, das den Query-Parameter ändert, um den Cache zu umgehen
            var newSrc = currentSrc.split('?')[0] + '?' + new Date().getTime();

            imageElement.src = newSrc;


            //}
        } catch (error) {
            console.error('Fehler beim Abrufen der Daten:', error);
        }


}
}

// Aktualisiere das Bild alle 10 Sekunden
setInterval(updateImage, 10000); // 10000 ms = 10 Sekunden