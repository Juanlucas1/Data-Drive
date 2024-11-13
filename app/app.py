import os
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static', static_folder=os.path.join(os.getcwd(), 'static'))

UPLOAD_FOLDER = 'uploads'

def save_file(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def process_file(filepath, filetype):
    try:
        if filetype == 'csv':
            df = pd.read_csv(filepath, encoding='ISO-8859-1', delimiter=';', on_bad_lines='skip')
        elif filetype == 'excel':
            df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None

def generate_graphs_for_columns(df):
    graphs = {}
    
    # Ignorar a coluna 'id' se ela existir
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    
    for column_name in df.columns:
        data_type = df[column_name].dtype
        title = f"Distribuição de {column_name}"

        # Ignorar longitude e latitude para gráficos de pizza e barras
        if 'longitude' in column_name.lower() or 'latitude' in column_name.lower():
            # Aqui podemos gerar gráficos específicos como mapas ou simplesmente ignorá-los para gráficos
            continue

        # Verificar se a coluna é categórica
        if pd.api.types.is_categorical_dtype(data_type) or pd.api.types.is_object_dtype(data_type):
            # Contagem das ocorrências das categorias
            counts = df[column_name].value_counts(normalize=True).reset_index()
            counts.columns = [column_name, 'percent']

            # Agrupar as categorias com menos de 2% em "Outros"
            counts['category'] = counts.apply(lambda row: row[column_name] if row['percent'] >= 0.02 else 'Outros', axis=1)
            counts_aggregated = counts.groupby('category')['percent'].sum().reset_index()

            # Evitar gerar gráficos de pizza para muitas categorias
            if len(counts_aggregated) > 5:
                # Se houver mais de 5 categorias, gerar um gráfico de barras em vez de pizza
                fig = px.bar(counts_aggregated, x='category', y='percent', title=title)
            else:
                # Se houver poucas categorias, gerar um gráfico de pizza
                fig = px.pie(counts_aggregated, names='category', values='percent', title=title)

            graphs[column_name] = fig.to_html(full_html=False)

        # Verificar se a coluna é numérica
        elif pd.api.types.is_numeric_dtype(data_type):
            # Se houver mais de uma coluna numérica, utilizar gráfico de linha ou área
            if len(df.columns) > 1:
                fig = px.line(df, x=df.index, y=column_name, title=title)  # Gráfico de linha
                graphs[column_name] = fig.to_html(full_html=False)
            else:
                # Se a coluna for única, podemos utilizar gráfico de histograma
                fig = px.histogram(df, x=column_name, title=title)  # Histograma para dados numéricos
                graphs[column_name] = fig.to_html(full_html=False)

        # Gráfico de Colunas ou Barras para comparação entre múltiplas categorias ou múltiplos valores numéricos
        if len(df.columns) > 1 and pd.api.types.is_numeric_dtype(df[column_name].dtype):
            fig = px.bar(df, x=df.columns[0], y=column_name, title=title)
            graphs[column_name] = fig.to_html(full_html=False)

            # Gráfico de Área para comparação entre diferentes colunas numéricas
            fig_area = px.area(df, x=df.columns[0], y=column_name, title=title)
            graphs[column_name] = fig_area.to_html(full_html=False)

    return graphs



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filepath = save_file(file)
        filetype = 'csv' if file.filename.endswith('.csv') else 'excel'
        df = process_file(filepath, filetype)

        if df is None:
            return jsonify({"error": "Erro ao processar o arquivo"}), 500

        try:
            graphs = generate_graphs_for_columns(df)
        except Exception as e:
            return jsonify({"error": f"Erro ao gerar os gráficos: {str(e)}"}), 500

        data_html = df.to_html(classes='data')

        return jsonify({
            'graphs': graphs,
            'data_html': data_html
        })

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)





















