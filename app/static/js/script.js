function searchTable() {
    // Get the input value
    var input = document.getElementById('searchInput').value;

    // Send the search query to the backend
    fetch('/search', {
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
                    li.textContent = item;
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
