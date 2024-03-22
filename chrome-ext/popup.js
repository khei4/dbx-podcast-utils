document.addEventListener('DOMContentLoaded', function () {
    var sendButton = document.getElementById('send');
    sendButton.addEventListener('click', function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            var currentTab = tabs[0];
            chrome.scripting.executeScript({
                target: { tabId: currentTab.id },
                function: getPageDetails
            });
        });
    }, false);
});

function getPageDetails() {
    const details = { url: window.location.href, body: document.body.innerText };
    // FIXME: Update the URL to Text2Speech server
    fetch('http://localhost:8000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(details),
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => console.error('Error:', error));
}
