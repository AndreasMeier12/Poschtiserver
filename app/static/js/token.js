function getToken(){
            const response = fetch('/api/token')
                .then(response => response.json())
                .then(data => {
                        document.getElementById('token-paragraph').innerText = data['val'];
                        document.getElementById('token-iat').innerText = data['iat'];
                        document.getElementById('token-exp').innerText = data['exp'];
                    }
                );
}