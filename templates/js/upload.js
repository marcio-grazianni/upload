"use strict";

window.onload = function () {
    document.getElementById('btnEnviar').addEventListener('click', btnEnviar_onclick);
}

function btnEnviar_onclick(event) {
    let formulario = document.getElementById("frmEnviar");

    if (formulario.checkValidity()) {
        button_processing("btnEnviar", true);

        formulario.submit();
    } else {
        formulario.reportValidity();
    }
}
