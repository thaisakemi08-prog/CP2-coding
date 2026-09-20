from datetime import datetime

usuarios = [
    (1, "ana", "ana@x.com", 5),
    (2, "bruno", "bruno@x.com", 2),
    (3, "caio", "caio@x.com", 1)
]

auditoria_logs = []

def alterar_nivel(admin_id, alvo_id, novo_nivel):
    global usuarios
    
    admin = next((u for u in usuarios if u[0] == admin_id), None)
    alvo = next((u for u in usuarios if u[0] == alvo_id), None)
    
    nivel_anterior = alvo[3] if alvo else None
    
    if not admin or admin[3] < 5:
        resultado = "RECUSADO"
        auditoria_logs.append({
            "quem": admin_id,
            "alvo": alvo_id,
            "nivel_anterior": nivel_anterior,
            "nivel_novo": novo_nivel,
            "resultado": resultado,
            "timestamp": datetime.now()
        })
        return "RECUSADO (admin sem privilégio ou inexistente). rollback."
        
    if admin_id == alvo_id:
        resultado = "RECUSADO"
        auditoria_logs.append({
            "quem": admin_id,
            "alvo": alvo_id,
            "nivel_anterior": nivel_anterior,
            "nivel_novo": novo_nivel,
            "resultado": resultado,
            "timestamp": datetime.now()
        })
        return "RECUSADO (auto-promoção). rollback."
        
    if not alvo:
        resultado = "RECUSADO"
        auditoria_logs.append({
            "quem": admin_id,
            "alvo": alvo_id,
            "nivel_anterior": nivel_anterior,
            "nivel_novo": novo_nivel,
            "resultado": resultado,
            "timestamp": datetime.now()
        })
        return "RECUSADO (alvo inexistente). rollback."
        
    usuarios = [
        (u[0], u[1], u[2], novo_nivel) if u[0] == alvo_id else u 
        for u in usuarios
    ]
    
    resultado = "OK"
    auditoria_logs.append({
        "quem": admin_id,
        "alvo": alvo_id,
        "nivel_anterior": nivel_anterior,
        "nivel_novo": novo_nivel,
        "resultado": resultado,
        "timestamp": datetime.now()
    })
    
    return f"OK. commit. {alvo[1].capitalize()}: {nivel_anterior} -> {novo_nivel}"
