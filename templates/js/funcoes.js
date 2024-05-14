"use strict";

function button_processing(botao, exibir) {
    let element = document.getElementById(botao);
    if (exibir) {
        // Exibe processando e desabilita
        element.innerHTML = "<i class='fas fa-spinner fa-spin'></i> " + element.textContent;
        element.disabled = true;
    }
    else {
        // Remove processando e habilita
        element.innerHTML = element.textContent;
        element.disabled = false;
    }
}
