from datetime import datetime
from flask import Flask, jsonify, request
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

X_train = [
    [12, 7, 90000, 3],
    [0, 1, 1200, 14],
    [15, 10, 120000, 2],
    [1, 0, 800, 12],
    [10, 5, 50000, 4],
]
y_train = ["alto", "baixo", "alto", "baixo", "alto"]

modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

X_test = [[12, 7, 90000, 3], [0, 1, 1200, 14], [10, 5, 50000, 4]]
y_test = ["alto", "baixo", "alto"]
y_pred = modelo.predict(X_test)

previsoes_db = []


@app.route("/api/triagem", methods=["POST"])
def triagem():
  dados = request.get_json(silent=True)
  if not dados or "features" not in dados:
    return jsonify({"erro": "corpo inválido ou ausente"}), 400

  features = dados["features"]

  if not isinstance(features, list) or len(features) != 4:
    return jsonify({
        "erro": f"esperadas 4 features, recebidas {len(features) if isinstance(features, list) else 'inválidas'}"
    }), 400

  try:
    features_numericas = [float(f) for f in features]
  except (ValueError, TypeError):
    return jsonify({"erro": "features devem ser numéricas"}), 400

  predicao = modelo.predict([features_numericas])[0]
  proba = max(modelo.predict_proba([features_numericas])[0])

  previsoes_db.append({
      "entrada": features_numericas,
      "saida": predicao,
      "confianca": round(float(proba), 2),
      "timestamp": datetime.now(),
  })

  return jsonify({"risco": predicao, "confianca": round(float(proba), 2)}), 200


@app.route("/api/modelo/metricas", methods=["GET"])
def metricas():
  precisao = precision_score(y_test, y_pred, pos_label="alto", zero_division=0)
  recall = recall_score(y_test, y_pred, pos_label="alto", zero_division=0)
  f1 = f1_score(y_test, y_pred, pos_label="alto", zero_division=0)
  matriz = confusion_matrix(y_test, y_pred).tolist()

  aviso = (
      "A acurácia foi omitida de propósito pois em cenários de segurança com"
      " classes desbalanceadas ela gera uma falsa sensação de segurança."
  )

  return (
      jsonify({
          "precisao": round(float(precisao), 2),
          "recall": round(float(recall), 2),
          "f1": round(float(f1), 2),
          "matriz": matriz,
          "aviso": aviso,
      }),
      200,
  )
