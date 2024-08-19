from flask import Flask, redirect,render_template,request, url_for

from flask_sqlalchemy import SQLAlchemy

# Importa a função `sessionmaker`, que é usada para criar uma nova sessão para interagir com o banco de dados
from sqlalchemy.orm import sessionmaker

# Importa as funções `create_engine` para estabelecer uma conexão com o banco de dados e `MetaData` para trabalhar com metadados do banco de dados
from sqlalchemy import create_engine, MetaData

# Importa a função `automap_base`, que é usada para refletir um banco de dados existente em classes ORM automaticamente
from sqlalchemy.ext.automap import automap_base
from Model.aluno import Aluno

import urllib.parse

app = Flask(__name__)

user = 'root'
password = urllib.parse.quote_plus('senai@123')

host = 'localhost'
database = 'schooltracker'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Criar a engine e refletir o banco de dados existente
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

# Mapeamento automático das tabelas para classes Python
Base = automap_base(metadata=metadata)
Base.prepare()

# Acessando a tabela 'aluno' mapeada
Aluno = Base.classes.aluno

# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/novoaluno", methods=["POST"])
def inserir_aluno():
    ra = request.form['ra']
    nome = request.form['nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])

    # Verifica se o RA já existe no banco de dados
    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()

    if aluno_existente:
        mensagem = "RA já cadastrado no sistema."
        return render_template('index.html', msgbanco=mensagem)

    aluno = Aluno(ra=ra,nome=nome,tempoestudo=tempoestudo,rendafamiliar=rendafamiliar)
    
    try:
        session.add(aluno) 
        session.commit() 
    except:
        session.rollback()
        raise 
    finally:
        session.close()
    mensagem = "cadastro efetuado com sucesso"
    return render_template('index.html',msgbanco=mensagem)

@app.route('/logar', methods=['POST'])
def logar_ra():
    try:
        # Obtém o valor do campo 'ra' e converte para inteiro
        ra = int(request.form['ra'])
    except ValueError:
        # Caso a conversão falhe, retorna uma mensagem de erro
        mensagem = "RA inválido. Certifique-se de que está digitando apenas números."
        return render_template('index.html', mensagem=mensagem)

    # Consulta o banco de dados para verificar se o aluno existe
    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()
    
    
    if aluno_existente:
        # recupera o nome do aluno
        nome = aluno_existente.nome
        # Se o aluno for encontrado, renderiza o template com o RA
        return render_template('diariobordo.html', nome=nome)
    else:
        # Se o aluno não for encontrado, retorna uma mensagem de erro
        mensagem = "RA inválido"
        return render_template('index.html', mensagem=mensagem)
    
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        alunos = session.query(Aluno).all()
    except ValueError:
        session.rollback()
        mensagem = 'Erro ao tentar buscar alunos'
        return redirect(url_for('listar_alunos'))
    finally:
        session.close()
    
    return render_template('listaralunos.html', alunos=alunos)
    
@app.route('/deletar/<int:aluno_id>', methods=['POST'])
def deletar(aluno_id):
    # Verifica o método simulado
    if request.form.get('_method') == 'DELETE':
        try:
            aluno_existente = session.query(Aluno).filter_by(id=aluno_id).first()
            
            if aluno_existente:
                session.delete(aluno_existente)
                session.commit()
                mensagem = 'Aluno deletado com sucesso'
            else:
                mensagem = 'Aluno não encontrado'
        except Exception as e:
            session.rollback()
            mensagem = f'Erro ao tentar deletar aluno: {str(e)}'
        finally:
            session.close()

        return redirect(url_for('listar_alunos'))
    
    # Se não for DELETE, pode-se retornar um erro ou redirecionar
    return 'Método não permitido', 405

@app.route('/atualizar/<int:aluno_id>', methods=['POST'])
def atualizar(aluno_id):
    # Verifica o método simulado
    if request.form.get('_method') == 'PUT':
        try:
            # Obtém os dados do formulário
            ra = request.form.get('ra')
            nome = request.form.get('nome')
            tempoestudo = request.form.get('tempoestudo')
            rendafamiliar = request.form.get('rendafamiliar')

            # Verifica se todos os dados necessários foram fornecidos
            if not ra or not nome or not tempoestudo or not rendafamiliar:
                return 'Dados insuficientes para atualização', 400

            aluno_existente = session.query(Aluno).filter_by(id=aluno_id).first()
            
            if aluno_existente:
                # Atualiza as informações do aluno
                aluno_existente.ra = ra
                aluno_existente.nome = nome
                aluno_existente.tempoestudo = tempoestudo
                aluno_existente.rendafamiliar = rendafamiliar
                session.commit()
                mensagem = 'Aluno atualizado com sucesso'
            else:
                mensagem = 'Aluno não encontrado'
        except Exception as e:
            session.rollback()
            mensagem = f'Erro ao tentar atualizar aluno: {str(e)}'
        finally:
            session.close()

        return redirect(url_for('listar_alunos'))
    
    # Se não for PUT, pode-se retornar um erro ou redirecionar
    return 'Método não permitido', 405


if __name__ == "__main__":
    app.run(debug=True)