/**
 * Converte um texto Markdown em HTML usando classes do Bootstrap.
 * Suporta títulos, listas, negrito, itálico, links e parágrafos.
 */
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