def recomendar(perfil: dict) -> dict:
    base_conhecimento = {
        "credenciais_do_SOC": {
            "banco": "MySQL",
            "cap": "CP",
            "justificativa": "O erro inaceitável é a dessincronização de credenciais permitindo acessos indevidos, tornando uma falha de autenticação catastrófica pior do que uma indisponibilidade temporária.",
            "risco_owasp": "A07:2021 – Falhas de Identificação e Autenticação"
        },
        "telemetria_de_sensores": {
            "banco": "MongoDB",
            "cap": "AP",
            "justificativa": "O erro inaceitável é o bloqueio total da ingestão de logs de segurança devido a restrições de consistência rígida, o que cegaria o monitoramento de ameaças em tempo real.",
            "risco_owasp": "A09:2021 – Falhas de Logging e Monitoramento"
        },
        "trilha_de_auditoria": {
            "banco": "MongoDB",
            "cap": "CP",
            "justificativa": "O erro inaceitável é a corrupção ou divergência de registos forenses, fazendo com que a trilha perca a validade jurídica necessária para investigações de incidentes.",
            "risco_owasp": "A09:2021 – Falhas de Logging e Monitoramento"
        },
        "carrinho_de_licencas": {
            "banco": "MySQL",
            "cap": "CP",
            "justificativa": "O erro inaceitável é a concorrência de transações permitindo o uso duplicado ou fraudulento de licenças sem validação financeira imediata.",
            "risco_owasp": "A04:2021 – Design Inseguro"
        },
        "cache_de_sessoes": {
            "banco": "MongoDB",
            "cap": "AP",
            "justificativa": "O erro inaceitável é a queda generalizada do portal de autenticação de utilizadores provocada por gargalos de replicação síncrona em falhas de rede.",
            "risco_owasp": "A07:2021 – Falhas de Identificação e Autenticação"
        }
    }
    
    schema_fixo = perfil.get("schema_fixo", False)
    precisa_acid = perfil.get("precisa_acid", False)
    escala_horizontal = perfil.get("escala_horizontal", False)
    tolera_atraso = perfil.get("tolera_atraso_de_consistencia", False)
    dado_sensivel = perfil.get("dado_sensivel", False)

    if precisa_acid and schema_fixo:
        banco = "MySQL"
        cap = "CP"
        justificativa = "O erro inaceitável é a corrupção estrutural e a quebra de atomicidade financeira provocada pela falta de consistência transacional restrita."
        risco_owasp = "A04:2021 – Design Inseguro"
    elif escala_horizontal and tolera_atraso:
        banco = "MongoDB"
        cap = "AP"
        justificativa = "O erro inaceitável é o colapso na recepção de fluxos massivos de dados por dependência de bloqueios globais de consistência."
        risco_owasp = "A05:2021 – Configuração Incorreta de Segurança"
    else:
        banco = "MongoDB" if not schema_fixo else "MySQL"
        cap = "AP" if escala_horizontal else "CP"
        justificativa = "O erro inaceitável é a falha sistémica de concorrência gerada pelo descompasso entre o modelo de dados e a topologia de rede."
        risco_owasp = "A04:2021 – Design Inseguro"

    return {
        "banco": banco,
        "cap": cap,
        "justificativa": justificativa,
        "risco_owasp": risco_owasp
    }
