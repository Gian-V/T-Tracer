(function () {
    Array.from(document.getElementsByClassName('form-control shadow-none date')).forEach((elmn) => {
        new Pikaday({
            field: elmn,
            format: 'D/M/YYYY',
            minDate: new Date(),
            toString(date) {
                const day = date.getDate();
                const month = date.getMonth() + 1;
                const year = date.getFullYear();
                return `${day}/${month}/${year}`;
            }
        });
    })
})();