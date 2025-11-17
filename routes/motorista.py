from flask import Blueprint, request, jsonify, render_template
from services.motorista_service import MotoristaService

motorista_service = MotoristaService()
motorista_bp = Blueprint('Motorista', __name__)

@motorista_bp.route('/')
def motorista_page():
    motoristas = motorista_service.get_all()
    # Garanta que o nome do arquivo é 'motoristas.html'
    return render_template('cadastro_motorista.html', motoristas=motoristas)

@motorista_bp.route('/', methods=['POST'])
def create_motorista():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False, # Corrigido
            "message": "Nenhum dado recebido na requisição!"
        }), 400

    # 1. Coleta de todos os 5 campos
    nome = data.get('nome')
    telefone = data.get('telefone')
    email = data.get('email')
    topico_ntfy = data.get('topico_ntfy')
    ativo = data.get('ativo') # Valor booleano (true/false) do checkbox

    # 2. Validação (como você pediu, 4 campos obrigatórios)
    if not nome or not telefone or not email or not topico_ntfy:
        return jsonify({
            "success": False, # Corrigido
            "message": "Todos os campos (Nome, Email, Telefone, Tópico) são obrigatórios."
        }), 400
    
    # 3. Envia os 5 campos para o service
    create = motorista_service.create(
        nome=nome,
        telefone=telefone,
        email=email,
        topico_ntfy=topico_ntfy,
        ativo=ativo 
    )
    
    if create:
        return jsonify({
            "success": True, # Corrigido
            "message": "Motorista cadastrado com sucesso!"
        }), 201
    
    return jsonify({
        "success": False, # Corrigido
        "message": "Erro interno do servidor."
    }), 500