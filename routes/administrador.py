from flask import Blueprint, request, jsonify
from services.administrador_service import AdministradorService


admin_service=AdministradorService()
admin_bp=Blueprint('Admin',__name__)

@admin_bp.route('')
def admin_page():
    return 'Admin page'

@admin_bp.route('/',methods=['POST'])
def create_admin():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":False,
            "message":"Nenhum dado recebido no corpo da requisição!"
        }),400
    
    nome= data.get('nome')
    senha = data.get('senha')
    email = data.get('email')
    if not nome or not senha or not email:
        return jsonify({
            "sucess":False,
            "message":"Todos os campos são obrigatórios!"
        }), 400
    create=admin_service.create(nome,email,senha)
    if create:
        return jsonify({
            "sucess":True,
            "message":"Admin cadastrado com sucesso!"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Erro interno do servidor!"
    }), 500