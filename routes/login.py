# /routes/login_bp.py (ou onde sua rota /auth está)

from flask import Blueprint, render_template, request, jsonify, Response, make_response
from services.administrador_service import AdministradorService

administrador_service = AdministradorService()
login_bp = Blueprint('Login', __name__) # Cuidado com o nome do blueprint se tiver outro

@login_bp.route('/')
def login_page():
    return render_template('login.html')

@login_bp.route('/auth', methods=['POST'])
def validate_login():
    data = request.get_json()
    if not data:
        # Use "success" (com 2 's')
        return jsonify({"success": False, "message": "Nenhum dado recebido!"}), 400
        
    nome = data.get('nome')
    senha = data.get('senha')
    
    if not nome or not senha:
        # Use "success" (com 2 's')
        return jsonify({"success": False, "message": "Os campos nome e senha são obrigatórios!"}), 400
        
    validate = administrador_service.validate(nome, senha)
    
    if validate:
        # Use "success" (com 2 's')
        response_data = {"success": True, "message": "Login autenticado com sucesso!"}
        
        response = make_response(jsonify(response_data), 200)
        
        # Define os cookies
        response.set_cookie('username', nome)
        response.set_cookie('senha', senha) # (Lembre-se do aviso de segurança sobre isso)
        
        return response
    
    # Se 'validate' for False
    # Use "success" (com 2 's')
    return jsonify({"success": False, "message": "Nome de usuário ou senha inválidos!"}), 401