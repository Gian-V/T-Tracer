let lista = [];
(async () => {
    const response = await fetch(
        'https://parseapi.back4app.com/classes/Worldzipcode_IT?limit=1000000000000&keys=adminCode2,placeName,postalCode',
        {
            headers: {
                'X-Parse-Application-Id': 'pX9BoL9aKBRWdqVp0fOmBK5ktvIiVht4lLz1tBEH', // This is your app's application id
                'X-Parse-REST-API-Key': 'wcI3cIhmOdFGPawZ39Ik6j5NlPykVkrwxmqx9ZnS', // This is your app's REST API key
            }
        }
    );
    const data = await response.json();

    data['results'].forEach((elmn) => {
        lista.push(`${elmn["placeName"].toUpperCase()} (${elmn["postalCode"]}) ${elmn["adminCode2"]}`)
    });

    Array.from(document.getElementsByClassName("form-control shadow-none where")).forEach((elmn) => {
        autocomplete(elmn, lista);
    });
})();