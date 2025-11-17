from flask import Blueprint, request, jsonify
from services.atribuicao_service import AtribuicaoService

atribuicao_service=AtribuicaoService()
# 1. (CORREÇÃO) Adicionado o prefixo da URL para bater com o fetch do HTML
atribuicao_bp=Blueprint('Atribuicao',__name__, url_prefix='/atribuicao')

@atribuicao_bp.route('/')
def atribuicao_page():
  return 'Atribuicao'

@atribuicao_bp.route('/', methods=['POST'])
def create_atribuicao():
  data = request.get_json()
  if not data:
    return jsonify({
      "success":False, # 2. (CORREÇÃO) Typo corrigido
      "message":"Nenhum dado recebido na requisição!"
    }),400
  
  id_motorista=data.get('id_motorista')
  id_viagem = data.get('id_viagem')
  id_admin_criador=data.get('id_admin_criador')
  
  # A validação está correta, pois o service espera os 3 argumentos
  if not id_motorista or not id_admin_criador or not id_viagem:
    return jsonify({
      "success":False, # 2. (CORREÇÃO) Typo corrigido
      "message":"Todos os campos são obrigatórios"
    }),400
  
  # A chamada do service está correta
  create = atribuicao_service.create(id_motorista,id_viagem,id_admin_criador)
  
  if create:
    return jsonify({
      "success":True, # 2. (CORREÇÃO) Typo corrigido
      "message":"Atribuição cadastrada com sucesso!"
    }), 200 # 201 (Created) seria mais correto, mas 200 funciona
  
  # 3. (CORREÇÃO) Mensagem de erro mais específica
  return jsonify({
    "success":False, # 2. (CORREÇÃO) Typo corrigido
    "message":"Erro ao salvar. O motorista já pode estar atribuído a esta viagem."
  }), 500