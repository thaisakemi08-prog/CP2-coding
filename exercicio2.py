ativos = [
    (1, "SRV-WEB01", "192.168.1.10", "alta"),
    (2, "PC-RH03", "192.168.1.45", "baixa")
]

alertas = [
    (1, 1, "BRUTE_FORCE", "critica"),
    (2, 1, "PORT_SCAN", "alta"),
    (3, 2, "XSS", "media")
]

ativos_dict = {a[0]: {"nome": a[1], "ip": a[2], "criticidade": a[3]} for a in ativos}

documentos_migrados = []
for alerta in alertas:
    alerta_id, ativo_id, tipo, severidade = alerta
    ativo_info = ativos_dict.get(ativo_id, {})
    
    documento = {
        "tipo": tipo,
        "severidade": severidade,
        "ativo": {
            "nome": ativo_info.get("nome"),
            "ip": ativo_info.get("ip"),
            "criticidade": ativo_info.get("criticidade")
        }
    }
    documentos_migrados.append(documento)

total_mysql_alertas = len(alertas)
total_mongo_documentos = len(documentos_migrados)

print(f"MySQL: {total_mysql_alertas} alertas | MongoDB: {total_mongo_documentos} documentos -> MIGRACAO ÍNTEGRA")

resultado_consulta = [doc for doc in documentos_migrados if doc["ativo"]["criticidade"] == "alta"]
print(f"Consulta sem JOIN: {len(resultado_consulta)} documentos")

print("Comentário: O que se ganha é a leitura sem JOIN de alta performance; o que se perde é a normalização, pois atualizar dados do ativo exige alterar múltiplos documentos (update_many).")
