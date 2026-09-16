
import os
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import CSRFProtect

from database import SessionLocal
from repositories import (
    CarreraRepository,
    EstudianteRepository,
    CandidatoRepository,
)
from votacion_repository import (
    CandidatoConsultaRepository,
    VotoAuditoriaRepository,
    ConteoResultadosRepository,
)

app = Flask(__name__)
# La clave se toma de una variable de entorno (FLASK_SECRET_KEY en el .env).
# Si no existe, se genera una aleatoria en cada arranque: nunca queda un
# secreto fijo escrito en el código fuente.
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

# Protección CSRF para todos los formularios (POST) de la aplicación.
csrf = CSRFProtect(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/carreras", methods=["GET", "POST"])
def carreras():
    db = SessionLocal()
    try:
        if request.method == "POST":
            try:
                CarreraRepository(db).crear(
                    nombre=request.form["nombre"],
                    costo=float(request.form["costo"]),
                    semestres=int(request.form["semestres"]),
                    modalidad=request.form["modalidad"],
                    facultad=request.form["facultad"],
                )
                flash("Carrera agregada correctamente.", "exito")
            except ValueError:
                flash("Costo debe ser numérico y semestres un entero.", "error")
            except Exception as e:
                db.rollback()
                flash(f"Error: {e}", "error")
            return redirect(url_for("carreras"))

        lista_carreras = CarreraRepository(db).obtener_todos()
        return render_template("carreras.html", carreras=lista_carreras)
    finally:
        db.close()


@app.route("/estudiantes", methods=["GET", "POST"])
def estudiantes():
    db = SessionLocal()
    try:
        if request.method == "POST":
            try:
                EstudianteRepository(db).crear(
                    documento=request.form["documento"],
                    nombres=request.form["nombres"],
                    apellidos=request.form["apellidos"],
                    correo=request.form["correo"],
                    semestre=int(request.form["semestre"]),
                    id_carrera=int(request.form["id_carrera"]),
                )
                flash("Estudiante agregado correctamente.", "exito")
            except ValueError:
                flash("Semestre debe ser un número entero.", "error")
            except Exception as e:
                db.rollback()
                flash(f"Error: {e}", "error")
            return redirect(url_for("estudiantes"))

        lista_estudiantes = EstudianteRepository(db).obtener_estudiantes_con_carrera_join()
        lista_carreras = CarreraRepository(db).obtener_todos()
        return render_template("estudiantes.html", estudiantes=lista_estudiantes, carreras=lista_carreras)
    finally:
        db.close()


@app.route("/candidatos", methods=["GET", "POST"])
def candidatos():
    db = SessionLocal()
    try:
        if request.method == "POST":
            try:
                CandidatoRepository(db).crear(
                    nombre_planeta=request.form["nombre_planeta"],
                    propuestas=request.form["propuestas"],
                    numero_tarjeton=int(request.form["numero_tarjeton"]),
                    id_estudiante=int(request.form["id_estudiante"]),
                )
                flash("Candidato agregado correctamente.", "exito")
            except ValueError:
                flash("El número de tarjetón debe ser un entero.", "error")
            except Exception as e:
                db.rollback()
                flash(f"Error: {e}", "error")
            return redirect(url_for("candidatos"))

        lista_candidatos = CandidatoConsultaRepository(db).obtener_todos_con_estudiante()
        lista_estudiantes = EstudianteRepository(db).obtener_todos()
        return render_template("candidatos.html", candidatos=lista_candidatos, estudiantes=lista_estudiantes)
    finally:
        db.close()


@app.route("/votacion", methods=["GET", "POST"])
def votacion():
    db = SessionLocal()
    try:
        if request.method == "POST":
            try:
                id_estudiante = int(request.form["id_estudiante"])
                id_candidato = int(request.form["id_candidato"])
                VotoAuditoriaRepository(db).registrar_voto(id_estudiante, id_candidato)
                flash("¡Voto registrado correctamente!", "exito")
            except ValueError as e:
                flash(str(e), "advertencia")
            except Exception as e:
                db.rollback()
                flash(f"Error: {e}", "error")
            return redirect(url_for("votacion"))

        lista_estudiantes = EstudianteRepository(db).obtener_todos()
        lista_candidatos = CandidatoRepository(db).obtener_todos()
        return render_template("votacion.html", estudiantes=lista_estudiantes, candidatos=lista_candidatos)
    finally:
        db.close()


@app.route("/resultados", methods=["GET"])
def resultados():
    db = SessionLocal()
    try:
        lista_resultados = ConteoResultadosRepository(db).obtener_resultados()
        return render_template("resultados.html", resultados=lista_resultados)
    finally:
        db.close()


if __name__ == "__main__":
    # El modo debug solo se activa si defines FLASK_DEBUG=1 en tu .env.
    # Por defecto queda apagado, como corresponde para producción.
    modo_debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=modo_debug)
    