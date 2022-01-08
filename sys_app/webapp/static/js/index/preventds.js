(function () {
    document.querySelector('#method-request').addEventListener('submit', (e) => {
        e.preventDefault();
        Array.from(document.getElementsByClassName('form-control shadow-none where')).forEach((elmn) => {
            if (!(lista.includes(elmn.value))) {
                elmn.value = null;
            }
        });
        document.querySelector('#method-request').submit();
    });
})();