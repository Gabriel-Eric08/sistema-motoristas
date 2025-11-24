from flask import Blueprint, render_template
from datetime import date, datetime, time # Importante importar datetime também
from services.viagem_service import ViagemService
from services.motorista_service import MotoristaService

# Instância dos serviços
viagem_service = ViagemService()
motorista_service = MotoristaService()

home_bp = Blueprint('Home', __name__)

@home_bp.route('/home')
def home_page():
    print("--- INÍCIO DA ROTA HOME ---") # Log no terminal
    try:
        # 1. Busca dados
        todos_motoristas = motorista_service.get_all()
        todas_viagens = viagem_service.get_all()
        
        print(f"Passo 1 OK: {len(todos_motoristas)} motoristas, {len(todas_viagens)} viagens.")

        hoje = date.today()

        # 2. Cálculos básicos
        total_motoristas = len(todos_motoristas)
        total_viagens = len(todas_viagens)

        # Filtros de contagem
        # O erro pode estar aqui se o banco tiver datas nulas ou formatos errados
        viagens_hoje = []
        for v in todas_viagens:
            # Proteção caso v.data_viagem seja None
            if v.data_viagem and v.data_viagem == hoje:
                viagens_hoje.append(v)
        
        viagens_pendentes = [v for v in todas_viagens if v.status == 'Pendente']
        
        qtd_hoje = len(viagens_hoje)
        qtd_pendentes = len(viagens_pendentes)
        
        print("Passo 2 (Cálculos) OK")

        # 3. Lógica Próximas Viagens
        # Filtra apenas viagens válidas (com data) e futuras
        viagens_futuras = [v for v in todas_viagens if v.data_viagem and v.data_viagem >= hoje]
        
        # Ordenação segura
        # Se horario for None, usa time.min (00:00:00) para não dar erro de comparação
        viagens_futuras.sort(key=lambda x: (x.data_viagem, x.horario_estimado_partida or time.min))
        
        proximas_5_viagens = viagens_futuras[:5]
        
        print("Passo 3 (Ordenação) OK")

        stats = {
            'motoristas': total_motoristas,
            'hoje': qtd_hoje,
            'pendentes': qtd_pendentes,
            'total': total_viagens
        }

        return render_template('home.html', stats=stats, proximas_viagens=proximas_5_viagens)

    except Exception as e:
        # ISSO VAI MOSTRAR O ERRO REAL NO SEU TERMINAL
        import traceback
        traceback.print_exc()
        print(f"ERRO FATAL: {e}")
        return f"<h1>Ocorreu um erro no servidor:</h1><p>{e}</p>", 500