// main.js (ubicado en static/js)
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("flash-modal");
    const closeModalButtons = modal.querySelectorAll(".delete, .button.is-success");

    // Abre automáticamente el modal si hay mensajes flash
    const messages = modal.querySelectorAll(".message");
    if (messages.length > 0) {
        modal.classList.add("is-active");
    }

    // Cierra el modal al hacer clic en los botones de cierre
    closeModalButtons.forEach(button => {
        button.addEventListener("click", () => {
            modal.classList.remove("is-active");
        });
    });
});