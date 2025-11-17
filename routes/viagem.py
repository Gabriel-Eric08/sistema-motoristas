from flask import Blueprint, request, jsonify, render_template
from services.viagem_service import ViagemService
from services.motorista_service import MotoristaService
# Assumindo que você terá o 'get_current_admin_id' em algum lugar (ex: flask_login)

viagem_service = ViagemService()
motorista_service = MotoristaService()
viagem_bp = Blueprint('Viagem', __name__, url_prefix='/viagens') # Boa prática adicionar url_prefix

@viagem_bp.route('/')
def viagem_page():
    motoristas=motorista_service.get_all()
    viagens = viagem_service.get_all()
    # Assumindo que o template se chama 'viagens.html'
    return render_template('cadastro_viagem.html', viagens=viagens, motoristas=motoristas)

@viagem_bp.route('/', methods=['POST'])
def create_viagem():
    """
    Rota corrigida para criar uma VIAGEM (evento).
    Agora usa 'data_viagem' (Date) em vez de 'data_hora_inicio' (DateTime).
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Nenhum dado recebido."}), 400
    
    # Campos básicos da Viagem
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    local_partida = data.get('local_partida')
    local_destino = data.get('local_destino')
    h_partida = data.get('horario_estimado_partida') # ex: "14:30"
    h_volta = data.get('horario_estimado_volta')     # ex: "18:00"

    # --- CAMPO CORRIGIDO ---
    # Espera-se um formato de data "AAAA-MM-DD" (ex: "2024-10-30")
    data_viagem_str = data.get('data_viagem') 
    
    # --- VALIDAÇÃO ATUALIZADA ---
    # Título e data são obrigatórios. O horário de partida também deveria ser.
    if not titulo or not data_viagem_str or not h_partida:
        return jsonify({
            "success": False, 
            "message": "Os campos 'Título', 'Data da Viagem' e 'Horário de Partida' são obrigatórios."
        }), 400
    
    # --- CHAMADA DE SERVICE CORRIGIDA ---
    try:
        create = viagem_service.create(
            titulo=titulo, 
            descricao=descricao, 
            local_partida=local_partida, 
            local_destino=local_destino,
            h_partida_str=h_partida, 
            h_volta_str=h_volta,
            data_viagem_str=data_viagem_str # Passando a string "AAAA-MM-DD"
        )
        
        if create:
            return jsonify({"success": True, "message": "Viagem cadastrada com sucesso!"}), 201
        else:
            # O service retorna False em caso de erro de conversão
            return jsonify({
                "success": False, 
                "message": "Erro ao criar viagem. Verifique os formatos de data (AAAA-MM-DD) e hora (HH:MM)."
            }), 400

    except Exception as e:
        # Captura outros erros inesperados
        print(f"Erro inesperado na rota create_viagem: {e}")
        return jsonify({"success": False, "message": "Erro interno no servidor."}), 500
    
