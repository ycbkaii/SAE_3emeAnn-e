var TOKEN = {}
var conn_visible = false
function display_conn() {
    console.log(conn_visible)
    if (!conn_visible) {
        form_con.style.display = "block"
        conn_visible = true
    }
    else {
        form_con.style.display = "none"
        conn_visible = false
    }
    
}

let form_con = document.getElementById("form_conn")
async function login(formData) {
    try {
        const response = await fetch('http://127.0.0.1:8000/usr/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Erreur réseau ou serveur');
        }

        const data = await response.json();
        TOKEN = data
        
        alert('Connexion réussie!');
    } catch (error) {
        console.error('Erreur lors de l\'envoi du formulaire:', error);
        alert('Erreur lors de la connexion. Veuillez réessayer.');
    }
}


document.getElementById('oauth-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new URLSearchParams({
        grant_type: 'password',
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        client_id: "",
        client_secret: "",
    });

    await login(formData);
    display_conn()
    id_user = document.getElementById('username').value
    
    fetchAllBooks()
});



function read_token() {
    return TOKEN
}

display_conn()