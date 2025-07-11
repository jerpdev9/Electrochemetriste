from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use("Agg")  # Usamos backend sin GUI para servidores
import matplotlib.pyplot as plt
import pyCHNOSZ as pyc
import io

app = Flask(__name__)

# Lista maestra de especies (puedes ampliar o cargar dinámicamente)
ALL_SPECIES = [
    "H2O", "O2", "H+", "H2", "CO2", "CO3--", "CH4",
    "Fe++", "Fe+++", "SO4--", "HS-", "H2S"
]

@app.route("/")
def index():
    """Renderiza la página principal con la lista de especies."""
    return render_template("index.html", species=ALL_SPECIES)

@app.route("/diagram", methods=["POST"])
def diagram():
    """Genera el diagrama de Pourbaix y devuelve un PNG."""
    selected = request.form.getlist("species")
    if not selected:
        return "No species selected", 400

    try:
        # Reiniciar configuración de CHNOSZ
        pyc.reset()

        # Usamos dash=True para compatibilidad en web
        pyc.basis("CHNOS+", selected, dash=True)

        # Crear figura matplotlib
        fig = plt.figure(figsize=(6, 5))

        # Generar diagrama con dash=True para entorno Flask
        pyc.diagram("Eh-pH", fig=fig, dash=True)

    except Exception as exc:
        return f"Error generating diagram: {exc}", 500

    # Guardar figura en memoria y enviarla como imagen
    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
