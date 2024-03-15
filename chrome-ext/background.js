chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: getPageDetails
    });
});

function getPageDetails() {
    const details = { url: window.location.href, body: document.body.innerText };
    fetch('https://yourserver.com/api/data', {
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
