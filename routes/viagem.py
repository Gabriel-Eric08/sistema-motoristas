from flask import Blueprint, request, jsonify, render_template
from services.viagem_service import ViagemService
from services.motorista_service import MotoristaService
# Assumindo que você terá o 'get_current_admin_id' em algum lugar (ex: flask_login)

viagem_service = ViagemService()
motorista_service = MotoristaService()
viagem_bp = Blueprint('Viagem', __name__, url_prefix='/viagens') # Boa prática adicionar url_prefix

@viagem_bp.route('/')
def viagem_page():
    motoristas = motorista_service.get_all()
    todas_viagens = viagem_service.get_all()
    
    # SEPARAÇÃO DE LISTAS (Lógica no Backend)
    # Assumindo que sua model 'Viagem' tem um campo status ou motorista_id
    # Ajuste a condição 'v.status' conforme seu banco de dados
    viagens_pendentes = [v for v in todas_viagens if v.status == 'Pendente'] 
    viagens_atribuidas = [v for v in todas_viagens if v.status == 'Atribuída' or v.status == 'Concluída']

    return render_template('cadastro_viagem.html', 
                           viagens_pendentes=viagens_pendentes, 
                           viagens_atribuidas=viagens_atribuidas, 
                           motoristas=motoristas)

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
    
@viagem_bp.route('/concluir/<id_viagem>', methods=['POST'])
def concluir(id_viagem):
    existing = viagem_service.existing(id_viagem)
    if existing==False:
        return jsonify({
            "sucess":False,
            "message":"Viagem não encontrada!"
        }), 400
    concluir = viagem_service.concluir(id_viagem)
    if concluir:
        return jsonify({
            "sucess":True,
            "message":"Viagem concluída com sucesso!"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Erro interno do servidor!"
    }), 500

@viagem_bp.route('/check-conflict', methods=['POST'])
def check_conflict():
    data = request.get_json()
    id_motorista = data.get('id_motorista')
    data_viagem_nova = data.get('data_viagem') # Formato esperado: YYYY-MM-DD

    if not id_motorista or not data_viagem_nova:
        return jsonify({"has_conflict": False})

    # Lógica para verificar se o motorista tem viagens nessa data
    # Você precisará implementar um método no seu service, ex: get_by_motorista_and_date
    # Aqui simularei a lógica:
    
    viagens_motorista = viagem_service.get_by_motorista(id_motorista) # Supondo que retorne lista de viagens
    
    conflito = False
    detalhes = ""
    
    for v in viagens_motorista:
        # Verifica se a data coincide e se o status é Atribuída (não conta cancelada/concluída se não quiser)
        # Atenção à conversão de tipos (string vs date object)
        v_data_str = v.data_viagem.strftime('%Y-%m-%d') if hasattr(v.data_viagem, 'strftime') else str(v.data_viagem)
        
        if v_data_str == data_viagem_nova and v.status == 'Atribuída':
            conflito = True
            detalhes = f"Viagem: {v.titulo} às {v.horario_estimado_partida}"
            break
            
    return jsonify({
        "has_conflict": conflito,
        "message": f"Este motorista já possui uma viagem nesta data ({detalhes}). Deseja prosseguir mesmo assim?"
    })

@viagem_bp.route('/detalhes/<int:id_viagem>', methods=['GET'])
def detalhes_viagem(id_viagem):
    viagem = viagem_service.get_by_id(id_viagem)
    
    if not viagem:
        # Se não achar, retorna erro json ou redireciona. 
        # Aqui vou retornar um HTML de erro simples ou redirecionar para a lista
        return render_template('erro.html', mensagem="Viagem não encontrada"), 404
        
    # Verifica se há motorista atribuído
    motorista = None
    if viagem.atribuicoes:
        # Pega o primeiro motorista da lista de atribuições
        motorista = viagem.atribuicoes[0].motorista

    return render_template('detalhes_viagem.html', viagem=viagem, motorista=motorista)
@viagem_bp.route('/historico', methods=['GET'])
def historico_page():
    # 1. Captura os parâmetros da URL (Query String)
    status_filter = request.args.get('status')
    motorista_filter = request.args.get('motorista')
    data_ini_filter = request.args.get('data_inicio')
    data_fim_filter = request.args.get('data_fim')

    # 2. Busca os dados filtrados
    viagens = viagem_service.search(
        status=status_filter,
        id_motorista=motorista_filter,
        data_inicio_str=data_ini_filter,
        data_fim_str=data_fim_filter
    )

    # 3. Precisa da lista de motoristas para popular o <select> de filtro
    motoristas = motorista_service.get_all()

    return render_template(
        'historico_viagens.html',
        viagens=viagens,
        motoristas=motoristas,
        # Passamos os filtros de volta para manter os campos preenchidos na tela
        filters={
            'status': status_filter, 
            'motorista': motorista_filter,
            'data_inicio': data_ini_filter,
            'data_fim': data_fim_filter
        }
    )