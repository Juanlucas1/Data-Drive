import os
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static', static_folder=os.path.join(os.getcwd(), 'static'))

# Caminho para salvar os arquivos
UPLOAD_FOLDER = 'uploads'

# Função para salvar o arquivo
def save_file(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Cria o diretório se ele não existir
    
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Salva o arquivo no diretório
    file.save(filepath)
    
    return filepath

# Função para processar arquivos CSV e Excel
def process_file(filepath, filetype):
    try:
        if filetype == 'csv':
            df = pd.read_csv(filepath, encoding='ISO-8859-1', delimiter=';', on_bad_lines='skip')
        elif filetype == 'excel':
            df = pd.read_excel(filepath)
        
        # Remover espaços extras das colunas
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None

# Função para gerar gráficos de diferentes tipos
def generate_graph(df, column_name, title, graph_type='bar'):
    try:
        if column_name in df.columns:
            counts = df[column_name].value_counts().reset_index()
            counts.columns = [column_name, 'count']
            
            if graph_type == 'bar':
                fig = px.bar(counts, x=column_name, y='count', title=title,
                             labels={column_name: column_name, 'count': 'Número de Ocorrências'})
            elif graph_type == 'pie':
                fig = px.pie(counts, names=column_name, values='count', title=title)
            elif graph_type == 'line':
                fig = px.line(counts, x=column_name, y='count', title=title,
                             labels={column_name: column_name, 'count': 'Número de Ocorrências'})
            elif graph_type == 'barh':
                fig = px.bar(counts, y=column_name, x='count', title=title,
                             labels={column_name: column_name, 'count': 'Número de Ocorrências'})
            
            return fig.to_html(full_html=False)
        else:
            print(f"Coluna {column_name} não encontrada.")
            return f"<p>Coluna {column_name} não encontrada no arquivo.</p>"
    except Exception as e:
        print(f"Erro ao gerar gráfico para a coluna {column_name}: {e}")
        return f"<p>Erro ao gerar gráfico para a coluna {column_name}</p>"

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para upload de arquivo
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filepath = save_file(file)
        
        # Verifica a extensão do arquivo e escolhe o método correto de leitura
        filetype = 'csv' if file.filename.endswith('.csv') else 'excel'
        df = process_file(filepath, filetype)
        
        if df is None:
            return jsonify({"error": "Erro ao processar o arquivo"}), 500

        # Gerar gráficos para as colunas mais importantes
        try:
            graph_tipo_acidente = generate_graph(df, 'tipo_acidente', 'Tipos de Acidente', graph_type='bar')
            graph_clima = generate_graph(df, 'condicao_metereologica', 'Condição Meteorológica', graph_type='pie')
            graph_dia_semana = generate_graph(df, 'dia_semana', 'Dia da Semana', graph_type='barh')
            graph_classificacao_acidente = generate_graph(df, 'classificacao_acidente', 'Classificação do Acidente', graph_type='bar')
            graph_fase_dia = generate_graph(df, 'fase_dia', 'Fase do Dia', graph_type='pie')
            graph_sentido_via = generate_graph(df, 'sentido_via', 'Sentido da Via', graph_type='bar')
            graph_causa_acidente = generate_graph(df, 'causa_acidente', 'Causa do Acidente', graph_type='bar')
            graph_pessoas = generate_graph(df, 'pessoas', 'Número de Pessoas Envolvidas', graph_type='line')
            graph_feridos = generate_graph(df, 'feridos', 'Número de Feridos', graph_type='line')
            graph_veiculos = generate_graph(df, 'veiculos', 'Número de Veículos', graph_type='bar')
        except Exception as e:
            return jsonify({"error": f"Erro ao gerar os gráficos: {str(e)}"}), 500

        # Converte os dados para HTML para visualização no frontend
        data_html = df.to_html(classes='data')  # Adiciona a classe 'data' para estilização da tabela
        
        return jsonify({
            'graph_tipo_acidente': graph_tipo_acidente,
            'graph_clima': graph_clima,
            'graph_dia_semana': graph_dia_semana,
            'graph_classificacao_acidente': graph_classificacao_acidente,
            'graph_fase_dia': graph_fase_dia,
            'graph_sentido_via': graph_sentido_via,
            'graph_causa_acidente': graph_causa_acidente,
            'graph_pessoas': graph_pessoas,
            'graph_feridos': graph_feridos,
            'graph_veiculos': graph_veiculos,
            'data_html': data_html
        })

# Função para validar o tipo de arquivo
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)





















