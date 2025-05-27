/**
 * Converte um texto Markdown em HTML usando classes do Bootstrap.
 * Suporta títulos, listas, negrito, itálico, links e parágrafos.
 */
class SimpleMarkdownEditor {
    constructor({ element }) {
        this.textarea = element;
        this.createEditor();
        this.bindEvents();
    }

    createEditor() {
        // Cria o container do editor
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'simplemde-wrapper mb-3';

        // Cria a barra de ferramentas
        this.toolbar = document.createElement('div');
        this.toolbar.className = 'simplemde-toolbar btn-toolbar mb-2';
        this.toolbar.innerHTML = `
            <button type="button" class="btn btn-light btn-sm" data-action="bold" title="Negrito"><b>B</b></button>
            <button type="button" class="btn btn-light btn-sm" data-action="italic" title="Itálico"><i>I</i></button>
            <button type="button" class="btn btn-light btn-sm" data-action="heading" title="Título">H</button>
            <button type="button" class="btn btn-light btn-sm" data-action="ul" title="Lista não ordenada">&bull; Lista</button>
            <button type="button" class="btn btn-light btn-sm" data-action="ol" title="Lista ordenada">1. Lista</button>
            <button type="button" class="btn btn-light btn-sm" data-action="link" title="Link">&#128279;</button>
            <button type="button" class="btn btn-light btn-sm" data-action="preview" title="Visualizar">&#128065;</button>
        `;

        // Cria a área de preview
        this.preview = document.createElement('div');
        this.preview.className = 'simplemde-preview border rounded p-3 bg-light d-none';
        this.preview.style.minHeight = this.textarea.offsetHeight + 'px';

        // Insere os elementos no DOM
        this.textarea.parentNode.insertBefore(this.wrapper, this.textarea);
        this.wrapper.appendChild(this.toolbar);
        this.wrapper.appendChild(this.textarea);
        this.wrapper.appendChild(this.preview);

        // Ajusta textarea
        this.textarea.classList.add('simplemde-textarea');
        this.textarea.style.resize = 'vertical';
    }

    bindEvents() {
        this.toolbar.addEventListener('click', (e) => {
            if (e.target.closest('button')) {
                const action = e.target.closest('button').dataset.action;
                this.handleToolbarAction(action);
            }
        });

        this.textarea.addEventListener('input', () => {
            if (!this.preview.classList.contains('d-none')) {
                this.updatePreview();
            }
        });
    }

    handleToolbarAction(action) {
        switch (action) {
            case 'bold':
                this.wrapSelection('**', '**');
                break;
            case 'italic':
                this.wrapSelection('*', '*');
                break;
            case 'heading':
                this.insertAtLineStart('# ');
                break;
            case 'ul':
                this.insertAtLineStart('- ');
                break;
            case 'ol':
                this.insertAtLineStart('1. ');
                break;
            case 'link':
                this.insertLink();
                break;
            case 'preview':
                this.togglePreview();
                break;
        }
    }

    wrapSelection(before, after) {
        const { selectionStart, selectionEnd, value } = this.textarea;
        const selected = value.slice(selectionStart, selectionEnd);
        const newValue = value.slice(0, selectionStart) + before + selected + after + value.slice(selectionEnd);
        this.textarea.value = newValue;
        this.textarea.focus();
        this.textarea.setSelectionRange(selectionStart + before.length, selectionEnd + before.length);
        this.textarea.dispatchEvent(new Event('input'));
    }

    insertAtLineStart(prefix) {
        const { selectionStart, value } = this.textarea;
        const start = value.lastIndexOf('\n', selectionStart - 1) + 1;
        const newValue = value.slice(0, start) + prefix + value.slice(start);
        this.textarea.value = newValue;
        this.textarea.focus();
        this.textarea.setSelectionRange(selectionStart + prefix.length, selectionStart + prefix.length);
        this.textarea.dispatchEvent(new Event('input'));
    }

    insertLink() {
        const { selectionStart, selectionEnd, value } = this.textarea;
        const selected = value.slice(selectionStart, selectionEnd) || 'texto';
        const url = prompt('URL do link:', 'https://');
        if (url) {
            const linkMarkdown = `[${selected}](${url})`;
            const newValue = value.slice(0, selectionStart) + linkMarkdown + value.slice(selectionEnd);
            this.textarea.value = newValue;
            this.textarea.focus();
            this.textarea.setSelectionRange(selectionStart + 1, selectionStart + 1 + selected.length);
            this.textarea.dispatchEvent(new Event('input'));
        }
    }

    togglePreview() {
        if (this.preview.classList.contains('d-none')) {
            this.updatePreview();
            this.preview.classList.remove('d-none');
            this.textarea.classList.add('d-none');
        } else {
            this.preview.classList.add('d-none');
            this.textarea.classList.remove('d-none');
        }
    }

    updatePreview() {
        this.preview.innerHTML = markdownToBootstrapHTML(this.textarea.value);
    }

    value() {
        return this.textarea.value;
    }

    setValue(val) {
        this.textarea.value = val;
        this.textarea.dispatchEvent(new Event('input'));
    }
}

// Exemplo de uso:
// var simplemde = new SimpleMarkdownEditor({ element: document.getElementById("content") });
// document.querySelector('form').addEventListener('submit', function() {
//     document.getElementById("content").value = simplemde.value();
// });


function markdownToBootstrapHTML(markdown) {
    // Converte títulos
    let html = markdown
        .replace(/^###### (.*$)/gim, '<h6 class="mt-3 mb-2">$1</h6>')
        .replace(/^##### (.*$)/gim, '<h5 class="mt-3 mb-2">$1</h5>')
        .replace(/^#### (.*$)/gim, '<h4 class="mt-3 mb-2">$1</h4>')
        .replace(/^### (.*$)/gim, '<h3 class="mt-3 mb-2">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 class="mt-3 mb-2">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 class="mt-4 mb-3">$1</h1>');

    // Converte listas ordenadas
    html = html.replace(/^\d+\.\s+(.*)$/gim, '<li class="list-group-item">$1</li>');
    html = html.replace(/(<li class="list-group-item">[\s\S]+<\/li>)/gim, '<ol class="list-group mb-3">$1</ol>');

    // Converte listas não ordenadas
    html = html.replace(/^\s*[-*+]\s+(.*)$/gim, '<li class="list-group-item">$1</li>');
    html = html.replace(/(<li class="list-group-item">[\s\S]+<\/li>)/gim, '<ul class="list-group mb-3">$1</ul>');

    // Negrito e itálico
    html = html.replace(/\*\*\*(.*?)\*\*\*/gim, '<b><i>$1</i></b>');
    html = html.replace(/\*\*(.*?)\*\*/gim, '<b>$1</b>');
    html = html.replace(/\*(.*?)\*/gim, '<i>$1</i>');

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" class="link-primary" target="_blank">$1</a>');

    // Quebra de linha dupla para parágrafo
    html = html.replace(/\n{2,}/g, '</p><p class="mb-2">');
    html = '<p class="mb-2">' + html + '</p>';

    // Remove parágrafos duplicados em listas e títulos
    html = html.replace(/<p class="mb-2">\s*(<(h\d|ul|ol)[^>]*>)/gim, '$1');
    html = html.replace(/(<\/(h\d|ul|ol)>)\s*<\/p>/gim, '$1');

    // Remove parágrafos vazios
    html = html.replace(/<p class="mb-2">\s*<\/p>/gim, '');

    return html.trim();
}

// Exemplo de uso:
// const html = markdownToBootstrapHTML("# Título\n\nTexto **negrito** e *itálico*.\n\n- Item 1\n- Item 2");