// ============================================================================
// FUNÇÕES DE RENDERIZAÇÃO
// ============================================================================

/**
 * Renderiza preview de dados textuais (JSON formatado)
 */
function renderTextPreview(data) {
    return `
        <h5>Preview dos dados (${data.data.length} de ${data.total}):</h5>
        <pre class="bg-light p-3 rounded" style="max-height: 400px; overflow-y: auto;">${JSON.stringify(data.data, null, 2)}</pre>
    `;
}

/**
 * Renderiza preview de dados com imagens (grid de cards)
 */
function renderImagePreview(data, dataType) {
    const items = data.data.map(item => {
        if (dataType === 'pokemon') {
            const placeholder = 'https://via.placeholder.com/150?text=No+Image';
            const imageUrl = (item.imagens && (item.imagens.oficial || item.imagens.frente)) || placeholder;
            return `
                <div class="image-card">
                    <img src="${imageUrl}" alt="${item.nome}" 
                         onerror="this.src='${placeholder}'">
                    <div class="image-card-title">${item.nome}</div>
                    <div class="image-card-subtitle">
                        ${item.tipos ? item.tipos.join(', ') : ''}
                        <br>
                        <small>Gen ${item.geracao}</small>
                    </div>
                </div>
            `;
        } else if (dataType === 'dog') {
            const placeholder = 'https://via.placeholder.com/150?text=No+Image';
            const imageUrl = item.fotos || placeholder;
            return `
                <div class="image-card">
                    <img src="${imageUrl}" alt="${item.raca || 'Dog'}" 
                         onerror="this.src='${placeholder}'">
                    <div class="image-card-title">${item.nome}</div>
                    <div class="image-card-subtitle">
                        ${item.raca}
                        <br>
                        <small>${item.idade} anos • ${item.genero}</small>
                    </div>
                </div>
            `;
        }
        return '';
    }).join('');

    return `
        <h5>Preview dos dados (${data.data.length} de ${data.total}):</h5>
        <div class="image-preview-grid">${items}</div>
        <details class="mt-3">
            <summary class="btn btn-sm btn-outline-secondary">Ver JSON completo</summary>
            <pre class="bg-light p-3 rounded mt-2" style="max-height: 300px; overflow-y: auto;">${JSON.stringify(data.data, null, 2)}</pre>
        </details>
    `;
}

// ============================================================================
// FUNÇÕES DE MANIPULAÇÃO DE FORMULÁRIOS
// ============================================================================

/**
 * Processa o submit de formulários (textual ou com imagens)
 */
async function handleFormSubmit(e, isImageData = false) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const params = new URLSearchParams(formData);
    const exportFormat = formData.get('export_format');
    const dataType = formData.get('data_type');

    const resultDiv = document.getElementById('result');
    const alertContainer = document.getElementById('alertContainer');
    const previewContainer = document.getElementById('previewContainer');

    // Mostra mensagem de carregamento
    resultDiv.style.display = 'none';
    alertContainer.innerHTML = '<div class="alert alert-info">Gerando dados...</div>';
    resultDiv.style.display = 'block';
    previewContainer.innerHTML = '';

    try {
        const response = await fetch(`/gerar/?${params.toString()}`);

        if (exportFormat === 'preview') {
            const data = await response.json();

            if (data.success) {
                alertContainer.innerHTML = `
                    <div class="alert alert-success">
                        ${data.message}
                    </div>
                `;

                // Renderiza preview baseado no tipo de dado
                if (isImageData) {
                    previewContainer.innerHTML = renderImagePreview(data, dataType);
                } else {
                    previewContainer.innerHTML = renderTextPreview(data);
                }

                resultDiv.style.display = 'block';
            } else {
                alertContainer.innerHTML = `
                    <div class="alert alert-danger">
                        Erro: ${data.error}
                    </div>
                `;
                resultDiv.style.display = 'block';
            }
        } else {
            // Download do arquivo (JSON ou CSV)
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;

            const contentDisposition = response.headers.get('content-disposition');
            const filename = contentDisposition.split('filename=')[1].replace(/"/g, '');

            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            alertContainer.innerHTML = `
                <div class="alert alert-success">
                    Download iniciado! ✅
                </div>
            `;
            resultDiv.style.display = 'block';
        }
    } catch (error) {
        alertContainer.innerHTML = `
            <div class="alert alert-danger">
                Erro ao gerar dados: ${error.message}
            </div>
        `;
        resultDiv.style.display = 'block';
    }
}

// ============================================================================
// INICIALIZAÇÃO DOS EVENT LISTENERS
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    // Listener para formulário de dados textuais
    const textForm = document.getElementById('textGeneratorForm');
    if (textForm) {
        textForm.addEventListener('submit', (e) => {
            handleFormSubmit(e, false);
        });
    }

    // Listener para formulário de dados com imagens
    const imageForm = document.getElementById('imageGeneratorForm');
    if (imageForm) {
        imageForm.addEventListener('submit', (e) => {
            handleFormSubmit(e, true);
        });
    }

    // Limpa resultados ao trocar de aba
    document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', () => {
            const resultDiv = document.getElementById('result');
            if (resultDiv) {
                resultDiv.style.display = 'none';
            }
        });
    });

    // Adicione smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Adicione efeito de loading nos botões
    document.querySelectorAll('.btn-generate').forEach(button => {
        button.addEventListener('click', function () {
            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading');
            }, 2000);
        });
    });

});