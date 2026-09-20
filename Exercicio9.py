from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

acessos = []
ips_bloqueados = {}

@app.before_request
def before_request_func():
    ip = request.remote_addr
    if ip in ips_bloqueados:
        if datetime.now() < ips_bloqueados[ip]:
            return jsonify({"erro": "muitas requisições"}), 429, {"Retry-After": "60"}
        else:
            del ips_bloqueados[ip]
            
    request._start_time = datetime.now()
    acessos.append({
        "ip": ip,
        "rota": request.path,
        "metodo": request.method,
        "timestamp": request._start_time,
        "status": None
    })

@app.after_request
def after_request_func(response):
    if acessos and acessos[-1]["status"] is None:
        acessos[-1]["status"] = response.status_code
        
    ip = request.remote_addr
    agora = datetime.now()
    janela = agora - timedelta(minutes=1)
    
    ips_unicos = list(set(a["ip"] for a in acessos))
    dados_ips = []
    
    for u_ip in ips_unicos:
        reqs = [a for a in acessos if a["ip"] == u_ip and a["timestamp"] >= janela]
        req_por_minuto = len(reqs)
        erros_4xx = sum(1 for a in reqs if a["status"] and 400 <= a["status"] < 500)
        taxa_4xx = erros_4xx / req_por_minuto if req_por_minuto > 0 else 0
        rotas_distintas = len(set(a["rota"] for a in reqs))
        dados_ips.append([req_por_minuto, taxa_4xx, rotas_distintas])
        
    if len(dados_ips) >= 2:
        clf = IsolationForest(contamination=0.2, random_state=42)
        previsoes = clf.fit_predict(dados_ips)
        for idx, u_ip in enumerate(ips_unicos):
            if previsoes[idx] == -1:
                ips_bloqueados[u_ip] = datetime.now() + timedelta(seconds=60)
                
    return response

@app.route("/api/dados", methods=["GET"])
def dados():
    return jsonify({"status": "ok"}), 200
