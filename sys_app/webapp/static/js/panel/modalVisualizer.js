function loadUser(user) {
    window.onload = () => {
        if (document.getElementById('shipments_list') !== null) {
            new bootstrap.Collapse(document.getElementById('collapse_users'), {
                    toggle: false
                }
            ).show();
            new bootstrap.Modal(document.getElementById(`viewShipments${user}`), {
                    toggle: false
                }
            ).show();
        }
    }
}