from flask import Flask, render_template_string

app = Flask(__name__)

p1 = "<script>alert('xss1')</script>"
p2 = "' x onerror='alert(\"xss2\")'"

incidentes = [
    {"ativo": p1, "severidade": "alta"},
    {"ativo": p2, "severidade": "critica"}
]

@app.after_request
def adicionar_csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.route("/dashboard-inseguro", methods=["GET"])
def dashboard_inseguro():
    html = """
    <h1>Dashboard Inseguro</h1>
    <table>
    {% for inc in incidentes %}
    <tr>
        <td><img src="/icone.png" alt="{{ inc.ativo|safe }}"></td>
        <td>{{ inc.severidade }}</td>
    </tr>
    {% endfor %}
    </table>
    """
    return render_template_string(html, incidentes=incidentes)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    html = """
    <h1>Dashboard Seguro</h1>
    <table>
    {% for inc in incidentes %}
    <tr>
        <td><img src="/icone.png" alt="{{ inc.ativo }}"></td>
        <td>{{ inc.severidade }}</td>
    </tr>
    {% endfor %}
    </table>
    """
    return render_template_string(html, incidentes=incidentes)
