document.getElementById('file-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Mostrar o ícone de carregamento
    document.getElementById('loading-icon').style.display = 'block';

    // Obter o arquivo enviado
    let fileInput = document.getElementById('file-input');
    let fileName = fileInput.files[0].name; // Obter o nome do arquivo

    // Exibir o nome do arquivo selecionado
    document.getElementById('file-name').innerText = `Arquivo selecionado: ${fileName}`;

    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Enviar o arquivo via AJAX para o backend
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Verifique o conteúdo da resposta no console

        // Limpar qualquer conteúdo anterior no gráfico
        const chartsContainer = document.getElementById('charts-container');
        chartsContainer.innerHTML = '';

        // Verificar se os gráficos estão presentes e inseri-los
        const graphs = [
            { key: 'graph_tipo_acidente', containerId: 'graph_tipo_acidente' },
            { key: 'graph_clima', containerId: 'graph_clima' },
            { key: 'graph_dia_semana', containerId: 'graph_dia_semana' },
            { key: 'graph_classificacao_acidente', containerId: 'graph_classificacao_acidente' },
            { key: 'graph_fase_dia', containerId: 'graph_fase_dia' },
            { key: 'graph_sentido_via', containerId: 'graph_sentido_via' },
            { key: 'graph_causa_acidente', containerId: 'graph_causa_acidente' },
            { key: 'graph_pessoas', containerId: 'graph_pessoas' },
            { key: 'graph_feridos', containerId: 'graph_feridos' },
            { key: 'graph_veiculos', containerId: 'graph_veiculos' }
        ];

        // Adicionar gráficos dinamicamente
        graphs.forEach(graph => {
            if (data[graph.key]) {
                const div = document.createElement('div');
                div.id = graph.containerId; // Define o ID para o div do gráfico
                div.innerHTML = data[graph.key];
                chartsContainer.appendChild(div);
            }
        });

        // Executar os scripts para gerar os gráficos
        const scripts = chartsContainer.getElementsByTagName('script');
        for (let script of scripts) {
            eval(script.innerHTML);  // Executa o código JavaScript dentro da tag <script>
        }

        // Exibir dados processados (tabela HTML)
        document.getElementById('data-container').innerHTML = data.data_html;

        // Esconder o ícone de carregamento após o processamento
        document.getElementById('loading-icon').style.display = 'none';
    })
    .catch(error => {
        console.error("Erro ao enviar o arquivo:", error);
        
        // Esconder o ícone de carregamento em caso de erro
        document.getElementById('loading-icon').style.display = 'none';
    });
});

// Exibir nome do arquivo ao selecionar
document.getElementById('file-input').addEventListener('change', function(event) {
    let fileName = event.target.files[0].name;
    document.getElementById('file-name').innerText = `Arquivo selecionado: ${fileName}`;
});

















