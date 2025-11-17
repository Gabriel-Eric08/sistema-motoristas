from flask import Flask,Blueprint
from db_config import app
from routes.motorista import motorista_bp
from routes.administrador import admin_bp
from routes.viagem import viagem_bp
from routes.atribuicao import atribuicao_bp
from routes.login import login_bp
from routes.home import home_bp


app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(motorista_bp,url_prefix='/motorista')
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(viagem_bp,url_prefix='/viagem')
app.register_blueprint(atribuicao_bp,url_prefix='/atribuicao')

@app.route('/')
def home():
    return 'Hello'

if __name__=="__main__":
    app.run(port=5008, debug=True)