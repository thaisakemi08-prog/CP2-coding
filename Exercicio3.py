from datetime import datetime, timedelta
import random
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["soc_db"]
eventos = db["eventos"]

eventos.drop()

eventos.create_index("timestamp", expireAfterSeconds=604800)

agora = datetime.now()
eventos_para_inserir = []
for _ in range(200):
    horas_atras = random.randint(0, 23)
    minutos_atras = random.randint(0, 59)
    timestamp = agora - timedelta(hours=horas_atras, minutes=minutos_atras)
    eventos_para_inserir.append({"timestamp": timestamp, "tipo": "falha_autenticacao"})

eventos.insert_many(eventos_para_inserir)

pipeline = [
    {"$group": {"_id": {"$hour": "$timestamp"}, "total": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]

resultado = list(eventos.aggregate(pipeline))

print("=== Falhas por hora (últimas 24h) ===")
max_total = -1
pico_hora = ""
dados_horas = {item["_id"]: item["total"] for item in resultado}

for h in range(24):
    total = dados_horas.get(h, 0)
    barra = "#" * (total // 2)
    hora_str = f"{h:02d}h"
    if total > max_total:
        max_total = total
        pico_hora = f"{hora_str} ({total} falhas)"
    print(f"{hora_str} | {barra} {total}")

print(f"Hora de pico: {pico_hora}")
print("Índice TTL ativo: eventos com mais de 7 dias serão removidos automaticamente.")
print("Comentário: O TTL é uma decisão de segurança para mitigar riscos de exfiltração de dados sensíveis em caso de comprometimento e cumprir políticas de minimização de dados.")
