const themeToggleBtn = document.getElementById('theme-toggle');
const body = document.body;

themeToggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-theme');

    const icon = themeToggleBtn.querySelector('.material-symbols-outlined');
    if (body.classList.contains('dark-theme')) {
        icon.textContent = 'brightness_5'; // Ícone de "sol" para tema claro
    } else {
        icon.textContent = 'contrast'; // Ícone de "lua" para tema escuro
    }
});

document.addEventListener("DOMContentLoaded", () => {
    loadNotices(); // Carrega os avisos ao carregar a página
});

function loadNotices() {
    const apiUrl = "/muralaviso/"; // URL da view muralaviso
    const noticeMessageContainer = document.querySelector(".notice-list");

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            noticeMessageContainer.innerHTML = ""; // Limpa a lista antes de adicionar novos avisos
            if (data.avisos && data.avisos.length > 0) {
                // Processa os avisos e os exibe
                data.avisos.forEach(aviso => {
                    const noticeItem = document.createElement("div");
                    noticeItem.className = "notice-item";
                    noticeItem.innerHTML = `
                        <p class="notice-message">${aviso.mensagem}</p>
                        <small>${new Date(aviso.data_criacao).toLocaleString()}</small>
                        <div class="notice-actions">
                            <a href="/editar-aviso/${aviso.id}/" class="btn btn-edit">Editar</a>
                            <button class="btn btn-delete" data-id="${aviso.id}">Excluir</button>
                        </div>
                    `;
                    noticeMessageContainer.appendChild(noticeItem);
                });
            } else {
                // "Else" para quando não há avisos disponíveis
                noticeMessageContainer.innerHTML = "<p class='notice-message'>Nenhum aviso disponível.</p>";
            }
        })
};


const modal = document.getElementById("modal");
const openModalBtn = document.getElementById("openModalBtn");
const closeModalBtn = document.getElementById("closeModalBtn");
const form = modal.querySelector("form");

openModalBtn.addEventListener("click", () => {
    modal.style.display = "block"; // Abre a modal
});

closeModalBtn.addEventListener("click", () => {
    modal.style.display = "none"; // Fecha a modal
});

// Fecha a modal ao clicar fora do conteúdo da modal
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

// Envia o aviso via AJAX ao submeter o formulário
form.addEventListener("submit", (event) => {
    event.preventDefault();  // Evita o envio padrão do formulário

    const formData = new FormData(form);  // Obtém os dados do formulário

    fetch("/criar-aviso/", {  // URL do endpoint para criar aviso
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "sucesso") {
                loadNotices();  // Recarrega os avisos após criar um novo
                form.reset();   // Limpa o formulário
                modal.style.display = "none";
                window.location.reload() // Fecha a modal
            } else {
                alert("Erro ao criar aviso: " + data.mensagem);
            }
        })
        .catch(error => {
            console.error("Erro:", error);
            alert("Erro ao enviar o aviso.");
        });
});

// Adiciona evento de exclusão aos botões de excluir
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('btn-delete')) {
        const avisoId = event.target.getAttribute('data-id');
        if (confirm('Você tem certeza que deseja excluir este aviso?')) {
            deleteNotice(avisoId);
        }
    }
});

// Função para excluir um aviso
function deleteNotice(avisoId) {
    fetch(`/excluir-aviso/${avisoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'sucesso') {
                loadNotices();  // Recarrega os avisos após exclusão
            } else {
                alert("Erro ao excluir aviso: " + data.mensagem);
            }
        })
        .catch(error => console.error('Erro:', error));
}

// Função para obter o CSRF token dos cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Seleciona os elementos da modal de exclusão
const deleteModal = document.getElementById("deleteModal");
const deleteMessage = document.getElementById("deleteMessage");
const avisoIdInput = document.getElementById("avisoIdInput");
const closeDeleteModal = document.getElementById("closeDeleteModal");
const cancelDelete = document.getElementById("cancelDelete");
const deleteButtons = document.querySelectorAll(".btn-delete");

// Adiciona evento aos botões de exclusão para abrir a modal
deleteButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
        const avisoId = button.getAttribute("data-id");
        const avisoMensagem = button.getAttribute("data-mensagem");

        // Preenche os dados na modal
        avisoIdInput.value = avisoId;
        deleteMessage.textContent = `Você tem certeza que deseja excluir este aviso? "${avisoMensagem}"`;

        // Exibe a modal
        deleteModal.style.display = "block";
    });
});

// Fecha a modal ao clicar no botão de fechar
closeDeleteModal.addEventListener("click", () => {
    deleteModal.style.display = "none";
});

// Fecha a modal ao clicar no botão de cancelar
cancelDelete.addEventListener("click", () => {
    deleteModal.style.display = "none";
});

// Fecha a modal ao clicar fora dela
window.addEventListener("click", (event) => {
    if (event.target === deleteModal) {
        deleteModal.style.display = "none";
    }
});

// Seleciona os elementos da modal de edição
const editModal = document.getElementById("editModal");
const editAvisoId = document.getElementById("editAvisoId");
const editMensagem = document.getElementById("editMensagem");
const closeEditModal = document.getElementById("closeEditModal");
const cancelEdit = document.getElementById("cancelEdit");
const editButtons = document.querySelectorAll(".btn-edit");

// Adiciona evento aos botões de edição para abrir a modal
editButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const avisoId = button.getAttribute("data-id");
        const avisoMensagem = button.getAttribute("data-mensagem");

        // Preenche os dados na modal
        editAvisoId.value = avisoId;
        editMensagem.value = avisoMensagem;

        // Exibe a modal
        editModal.style.display = "block";
    });
});

// Fecha a modal de edição ao clicar no botão de fechar
closeEditModal.addEventListener("click", () => {
    editModal.style.display = "none";
});

// Fecha a modal de edição ao clicar no botão de cancelar
cancelEdit.addEventListener("click", () => {
    editModal.style.display = "none";
});

// Fecha a modal de edição ao clicar fora dela
window.addEventListener("click", (event) => {
    if (event.target === editModal) {
        editModal.style.display = "none";
    }
});