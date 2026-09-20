from flask import Flask, jsonify, request

app = Flask(__name__)

COLUNAS = {"data": "criado_em", "sev": "severidade", "ip": "ip_origem"}
ORDENS = {"asc": "ASC", "desc": "DESC"}


@app.route("/api/eventos", methods=["GET"])
def api_eventos():
  ordenar_por = request.args.get("ordenar_por", "data")
  ordem = request.args.get("ordem", "asc")
  tamanho_str = request.args.get("tamanho", "10")

  if ordenar_por not in COLUNAS:
    return jsonify({"erro": "campo de ordenação inválido"}), 400

  if ordem not in ORDENS:
    return jsonify({"erro": "ordem inválida"}), 400

  try:
    tamanho = int(tamanho_str)
  except ValueError:
    return jsonify({"erro": "tamanho deve ser inteiro"}), 400

  if tamanho > 100:
    tamanho = 100

  coluna_sql = COLUNAS[ordenar_por]
  ordem_sql = ORDENS[ordem]

  return jsonify({
      "status": 200,
      "tamanho_aplicado": tamanho,
      "ordenacao": f"{coluna_sql} {ordem_sql}",
  })
