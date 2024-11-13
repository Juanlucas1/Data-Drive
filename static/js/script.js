document.getElementById('file-form').addEventListener('submit', function(event) {
    event.preventDefault();

    document.getElementById('loading-icon').style.display = 'block';

    let fileInput = document.getElementById('file-input');
    let fileName = fileInput.files[0].name;
    document.getElementById('file-name').innerText = `Arquivo selecionado: ${fileName}`;

    let formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        const chartsContainer = document.getElementById('charts-container');
        chartsContainer.innerHTML = '';

        for (let [key, value] of Object.entries(data.graphs)) {
            const div = document.createElement('div');
            div.id = key;
            div.innerHTML = value;
            chartsContainer.appendChild(div);
        }

        const scripts = chartsContainer.getElementsByTagName('script');
        for (let script of scripts) {
            eval(script.innerHTML);
        }

        document.getElementById('data-container').innerHTML = data.data_html;
        document.getElementById('loading-icon').style.display = 'none';
    })
    .catch(error => {
        console.error("Erro ao enviar o arquivo:", error);
        document.getElementById('loading-icon').style.display = 'none';
    });
});

document.getElementById('file-input').addEventListener('change', function(event) {
    let fileName = event.target.files[0].name;
    document.getElementById('file-name').innerText = `Arquivo selecionado: ${fileName}`;
});

















