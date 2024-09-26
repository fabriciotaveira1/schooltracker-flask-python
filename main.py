from flask import Flask, redirect, render_template, request, url_for, session as session_flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from services.api_clima import ApiClima
from sqlalchemy.ext.automap import automap_base
from Model.Usuario import Usuario
from Model.Registro import Registro
from Model.Viagem import Viagem
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
Usuario = Base.classes.Usuario
Registro = Base.classes.Registro
Viagem = Base.classes.Viagem

# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/novo_usuario", methods=["POST"])
def inserir_aluno():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Verifica se o email já existe no banco de dados
    usuario_existente = session.query(Usuario).filter_by(email=email).first()

    if usuario_existente:
        mensagem = "Email já cadastrado no sistema."
        return render_template('index.html', mensagem=mensagem)

    usuario = Usuario(nome=nome, email=email, senha=senha)
    
    try:
        session.add(usuario) 
        session.commit() 
    except:
        session.rollback()
        raise 
    finally:
        session.close()
        
    mensagem = "Cadastro efetuado com sucesso."
    return render_template('index.html', mensagem=mensagem)

@app.route('/logar', methods=['POST'])
def logar_ra():
    try:
        email = request.form['email']
        senha = request.form['senha']

        usuario_existente = session.query(Usuario).filter_by(email=email, senha=senha).first()

        if usuario_existente:
            session_flask['usuario_id'] = usuario_existente.id
            return redirect(url_for('diario_bordo'))
        else:
            mensagem = "Email ou senha inválidos"
            return render_template('index.html', mensagem=mensagem)
    except ValueError:
        mensagem = "Email ou senha inválido. Certifique-se de que está digitando corretamente."
        return render_template('index.html', mensagem=mensagem)

@app.route("/diario_bordo")
def diario_bordo():
    usuario_id = session_flask.get('usuario_id')

    if usuario_id not in session_flask:
        return redirect(url_for('index'))

    recent_entries = session.query(Registro).filter_by(id_usuario=usuario_id).all()

    entries_data = []
    for entry in recent_entries:
        entries_data.append({
            'title': entry.title,
            'cidade': entry.cidade,
            'temperatura': entry.temperatura,
            'velocidade_do_vento': entry.velocidade_do_vento,
            'umidade_do_ar': entry.umidade_do_ar,
            'observacoes': entry.observacoes,
        })

    return render_template("diariobordo.html", recent_entries=entries_data, nome=session_flask.get('usuario_nome'))

@app.route("/adicionar_entrada", methods=["POST"])
def adicionar_entrada():
    id_viagem = request.form['id_viagem']
    data_registro = request.form['data_registro']
    cidade = request.form['cidade']
    observacoes = request.form['observacoes']

    if 'usuario_id' not in session_flask:
        mensagem = "Você precisa estar logado para adicionar uma entrada."
        return render_template('index.html', mensagem=mensagem)

    viagem_existente = session.query(Viagem).filter_by(id_viagem=id_viagem).first()
    if not viagem_existente:
        mensagem = "A viagem especificada não foi encontrada."
        return render_template('diario_bordo.html', mensagem=mensagem)

    nova_entrada = Registro(
        id_viagem=id_viagem,
        data_registro=data_registro,
        cidade=cidade,
        observacoes=observacoes
    )

    api_clima = ApiClima('da7d7856826a4e9daae192630241109')  # Substitua pela sua chave de API
    nova_entrada.registrar_dados_clima(api_clima, cidade)

    try:
        session.add(nova_entrada)
        session.commit()
    except Exception as e:
        session.rollback()
        mensagem = f"Ocorreu um erro ao registrar a entrada: {str(e)}"
        return render_template('diario_bordo.html', mensagem=mensagem)
    finally:
        session.close()

    mensagem = "Entrada adicionada com sucesso."
    return redirect(url_for('diario_bordo', mensagem=mensagem))

@app.route("/viagens", methods=["GET"])
def viagens():
    # Busca todas as viagens do banco de dados
    viagens_existentes = session.query(Viagem).all()
    return render_template("viagens.html", viagens=viagens_existentes)

@app.route("/adicionar_viagem", methods=["POST"])
def adicionar_viagem():
    data_inicio = request.form['data_inicio']
    localizacao = request.form['localizacao']

    # Obtém o ID do usuário logado
    usuario_id = session.get('usuario_id')

    nova_viagem = Viagem(data_inicio=data_inicio, localizacao=localizacao, id_usuario=usuario_id)
    
    try:
        session.add(nova_viagem)
        session.commit()
    except Exception as e:
        session.rollback()
        mensagem = f"Ocorreu um erro ao adicionar a viagem: {str(e)}"
        return render_template('viagens.html', mensagem=mensagem)
    finally:
        session.close()

    return redirect(url_for('viagens'))

@app.route("/editar_viagem/<int:id_viagem>", methods=["GET", "POST"])
def editar_viagem(id_viagem):
    viagem = session.query(Viagem).filter_by(id_viagem=id_viagem).first()

    if request.method == "POST":
        viagem.data_inicio = request.form['data_inicio']
        viagem.localizacao = request.form['localizacao']

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            mensagem = f"Ocorreu um erro ao editar a viagem: {str(e)}"
            return render_template('viagens.html', mensagem=mensagem)
        finally:
            session.close()

        return redirect(url_for('viagens'))

    return render_template("viagens.html", viagem=viagem)

@app.route("/deletar_viagem/<int:id_viagem>", methods=["GET"])
def deletar_viagem(id_viagem):
    viagem = session.query(Viagem).filter_by(id_viagem=id_viagem).first()
    try:
        session.delete(viagem)
        session.commit()
    except Exception as e:
        session.rollback()
        mensagem = f"Ocorreu um erro ao deletar a viagem: {str(e)}"
        return render_template('viagens.html', mensagem=mensagem)
    finally:
        session.close()

    return redirect(url_for('viagens'))


if __name__ == "__main__":
    app.run(debug=True)
