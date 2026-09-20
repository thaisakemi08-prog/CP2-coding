from flask import Flask, jsonify, request

app = Flask(__name__)

analistas = [
    (1, "ana", "key-ana-001", 5),
    (2, "bruno", "key-bruno-002", 2)
]

incidentes = [
    (1, 1, "Brute force SSH", "critica"),
    (2, 2, "Phishing no RH", "media")
]

def autenticar():
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return None, 401
    
    analista = next((a for a in analistas if a[2] == api_key), None)
    if not analista:
        return None, 401
        
    return analista, 200

@app.route("/api/incidentes/<int:inc_id>", methods=["GET"])
def get_incidente(inc_id):
    analista, status = autenticar()
    if status != 200:
        return jsonify({"erro": "não autorizado"}), status
        
    inc = next((i for i in incidentes if i[0] == inc_id), None)
    if not inc:
        return jsonify({"erro": "não encontrado"}), 404
        
    if analista[3] < 5 and inc[1] != analista[0]:
        return jsonify({"erro": "acesso negado"}), 403
        
    return jsonify({"id": inc[0], "dono_id": inc[1], "titulo": inc[2], "severidade": inc[3]}), 200

@app.route("/api/incidentes", methods=["GET"])
def listar_incidentes():
    analista, status = autenticar()
    if status != 200:
        return jsonify({"erro": "não autorizado"}), status
        
    if analista[3] >= 5:
        filtrados = incidentes
    else:
        filtrados = [i for i in incidentes if i[1] == analista[0]]
        
    resultado = [{"id": i[0], "dono_id": i[1], "titulo": i[2], "severidade": i[3]} for i in filtrados]
    return jsonify(resultado), 200

@app.route("/api/incidentes/<int:inc_id>", methods=["DELETE"])
def deletar_incidente(inc_id):
    analista, status = autenticar()
    if status != 200:
        return jsonify({"erro": "não autorizado"}), status
        
    inc = next((i for i in incidentes if i[0] == inc_id), None)
    if not inc:
        return jsonify({"erro": "não encontrado"}), 404
        
    if analista[3] < 5:
        return jsonify({"erro": "acesso negado"}), 403
        
    global incidentes
    incidentes = [i for i in incidentes if i[0] != inc_id]
    return jsonify({"status": "sucesso"}), 200
