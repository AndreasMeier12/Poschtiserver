function getToken(){
            const response = fetch('/api/token')
                .then(response => response.json())
                .then(data =>
                    document.getElementById('token-paragraph').innerText=data['val']
                );
}