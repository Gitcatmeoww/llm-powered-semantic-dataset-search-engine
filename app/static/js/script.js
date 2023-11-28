document.getElementById('searchButton').addEventListener('click', function () {
    searchTable();
});

document.getElementById('resetButton').addEventListener('click', function () {
    resetTable();
});

document.getElementById('keywordSearchButton').addEventListener('click', function () {
    keywordSearchTable();
});


function searchTable() {
    // Get the input value
    var input = document.getElementById('searchInput').value;

    // Send the search query to the backend
    fetch('/semantic_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Stringify the input value to send as JSON body
        body: JSON.stringify({ query: input })
    })
        .then(response => response.json())
        .then(data => {
            // Clear the previous list
            var list = document.getElementById('tablesList');
            list.innerHTML = '';

            // Check if there are results
            if (data.results && data.results.length) {
                // Populate the list with new results
                data.results.forEach(function (item) {
                    var li = document.createElement('li');
                    // Assuming the property that contains the table name is 'tableName'
                    li.textContent = item.tableName;
                    list.appendChild(li);
                });
            } else {
                // Show a message if no results were found
                var li = document.createElement('li');
                li.textContent = 'No results found';
                list.appendChild(li);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function resetTable() {
    // Clear the search input
    document.getElementById('searchInput').value = '';

    // Fetch and display the full table list as it was on initial load
    fetch('/')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            var list = document.getElementById('tablesList');
            list.innerHTML = doc.getElementById('tablesList').innerHTML;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function keywordSearchTable() {
    var input = document.getElementById('searchInput').value;

    // Send the keyword search query to the backend
    fetch('/keyword_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: input })
    })
        .then(response => response.json())
        .then(data => {
            var list = document.getElementById('tablesList');
            list.innerHTML = '';

            if (data.results && data.results.length) {
                data.results.forEach(function (item) {
                    var li = document.createElement('li');
                    li.textContent = item.tableName;
                    list.appendChild(li);
                });
            } else {
                var li = document.createElement('li');
                li.textContent = 'No results found';
                list.appendChild(li);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

