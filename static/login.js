async function login(formData) {
    try {
        const response = await fetch('URL_DE_VOTRE_BACKEND', {
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
        console.log('Réponse du serveur:', data);
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

});
