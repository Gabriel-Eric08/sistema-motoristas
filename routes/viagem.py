from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from services.viagem_service import ViagemService
from services.motorista_service import MotoristaService
from services.atribuicao_service import AtribuicaoService # Importamos o serviço de atribuição aqui

viagem_service = ViagemService()
motorista_service = MotoristaService()
atribuicao_service = AtribuicaoService()

# 1. Mudamos o prefixo para '/viagem' (singular) para bater com o fetch do HTML
viagem_bp = Blueprint('Viagem', __name__, url_prefix='/viagem') 

@viagem_bp.route('/')
def viagem_page():
    motoristas = motorista_service.get_all()
    todas_viagens = viagem_service.get_all()
    
    # Separação das listas
    viagens_pendentes = [v for v in todas_viagens if v.status == 'Pendente'] 
    viagens_atribuidas = [v for v in todas_viagens if v.status == 'Atribuída' or v.status == 'Concluída']
    
    # Montamos um objeto auxiliar para exibir o nome do motorista na tabela de atribuídas
    # (Pois o objeto 'v' tem a lista v.atribuicoes, mas queremos o nome direto para facilitar o HTML)
    lista_atribuidas_view = []
    for v in viagens_atribuidas:
        nome_motorista = "Desconhecido"
        if v.atribuicoes:
            nome_motorista = v.atribuicoes[0].motorista.nome
        
        # Adicionamos dinamicamente o atributo para o template
        v.motorista_nome = nome_motorista
        lista_atribuidas_view.append(v)

    # Renderiza o template que criamos anteriormente (cadastro_viagem.html)
    return render_template('cadastro_viagem.html', 
                           viagens_pendentes=viagens_pendentes, 
                           viagens_atribuidas=lista_atribuidas_view, 
                           motoristas=motoristas)

@viagem_bp.route('/', methods=['POST'])
def create_viagem():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Nenhum dado recebido."}), 400
    
    # --- CAPTURA DOS DADOS (Incluindo Distância e Tempo) ---
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    local_partida = data.get('local_partida')
    local_destino = data.get('local_destino')
    distancia_km = data.get('distancia_km')       # <--- NOVO
    tempo_estimado = data.get('tempo_estimado')   # <--- NOVO
    h_partida = data.get('horario_estimado_partida')
    h_volta = data.get('horario_estimado_volta')
    data_viagem_str = data.get('data_viagem') 
    
    if not titulo or not data_viagem_str or not h_partida:
        return jsonify({
            "success": False, 
            "message": "Campos obrigatórios: Título, Data e Hora de Saída."
        }), 400
    
    try:
        # Passando os novos argumentos para o service
        create = viagem_service.create(
            titulo=titulo, 
            descricao=descricao, 
            local_partida=local_partida, 
            local_destino=local_destino,
            distancia_km=distancia_km,      # <--- Passando
            tempo_estimado=tempo_estimado,  # <--- Passando
            h_partida_str=h_partida, 
            h_volta_str=h_volta,
            data_viagem_str=data_viagem_str
        )
        
        if create:
            return jsonify({"success": True, "message": "Viagem cadastrada com sucesso!"}), 201
        else:
            return jsonify({"success": False, "message": "Erro ao validar dados."}), 400

    except Exception as e:
        print(f"Erro na rota create_viagem: {e}")
        return jsonify({"success": False, "message": "Erro interno no servidor."}), 500

# --- ROTA DE ATRIBUIÇÃO (Trazida para cá para facilitar o frontend) ---
@viagem_bp.route('/atribuir', methods=['POST'])
def atribuir_motorista():
    data = request.get_json()
    id_viagem = data.get('id_viagem')
    id_motorista = data.get('id_motorista')
    
    # Admin fixo por enquanto (simulação de sessão)
    id_admin_criador = 1 

    if not id_viagem or not id_motorista:
        return jsonify({"success": False, "message": "Dados incompletos."}), 400

    sucesso = atribuicao_service.create(id_motorista, id_viagem, id_admin_criador)
    
    if sucesso:
        return jsonify({"success": True, "message": "Motorista atribuído e notificado!"}), 200
    else:
        return jsonify({"success": False, "message": "Erro ao atribuir (possível duplicação ou ID inválido)."}), 500


# --- ROTA DE VERIFICAÇÃO DE CONFLITO ---
@viagem_bp.route('/check-conflict', methods=['POST'])
def check_conflict():
    data = request.get_json()
    id_motorista = data.get('id_motorista')
    data_viagem_nova_str = data.get('data_viagem') # Chega como string "YYYY-MM-DD"

    if not id_motorista or not data_viagem_nova_str:
        return jsonify({"has_conflict": False})

    # Busca todas as viagens desse motorista
    viagens_motorista = viagem_service.get_by_motorista(id_motorista)
    
    conflito = False
    detalhes = ""
    
    for v in viagens_motorista:
        # Verifica apenas viagens ativas (Atribuída)
        if v.status == 'Atribuída':
            # Converte a data do banco (Date object) para string para comparar
            v_data_str = v.data_viagem.strftime('%Y-%m-%d')
            
            if v_data_str == data_viagem_nova_str:
                conflito = True
                hora = v.horario_estimado_partida.strftime('%H:%M') if v.horario_estimado_partida else "??"
                detalhes = f"{v.titulo} ({hora})"
                break
            
    if conflito:
         return jsonify({
            "has_conflict": True,
            "message": f"Motorista já possui viagem dia {data_viagem_nova_str}: {detalhes}"
        })
    else:
        return jsonify({"has_conflict": False})

@viagem_bp.route('/historico', methods=['GET'])
def historico_page():
    status_filter = request.args.get('status')
    motorista_filter = request.args.get('motorista')
    data_ini_filter = request.args.get('data_inicio')
    data_fim_filter = request.args.get('data_fim')

    viagens = viagem_service.search(
        status=status_filter,
        id_motorista=motorista_filter,
        data_inicio_str=data_ini_filter,
        data_fim_str=data_fim_filter
    )
    motoristas = motorista_service.get_all()

    # Como não temos o template 'historico_viagens.html' separado no código anterior,
    # sugerimos usar o mesmo ou um novo. Aqui mantive o nome que você usou.
    return render_template(
        'historico_viagens.html',
        viagens=viagens,
        motoristas=motoristas,
        filters={
            'status': status_filter, 
            'motorista': motorista_filter,
            'data_inicio': data_ini_filter,
            'data_fim': data_fim_filter
        }
    )

@viagem_bp.route('/detalhes/<int:id_viagem>', methods=['GET'])
def detalhes_viagem(id_viagem):
    # Busca a viagem pelo ID
    viagem = viagem_service.get_by_id(id_viagem)
    
    if not viagem:
        # Retorna um 404 simples ou renderiza uma página de erro se tiver
        return "<h1>Viagem não encontrada</h1>", 404
        
    # Verifica se há motorista atribuído para passar ao template
    motorista = None
    if viagem.atribuicoes:
        # Pega o primeiro motorista da lista (assumindo relação 1:N ou N:N tratada como 1)
        motorista = viagem.atribuicoes[0].motorista

    return render_template('detalhes_viagem.html', viagem=viagem, motorista=motorista)