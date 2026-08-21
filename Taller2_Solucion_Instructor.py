"""
Taller 2 — Reglas de Validación y Control de Versiones con Git
Solución de referencia para el instructor
Caso: TiendaNova · Datasets: clientes.csv, pedidos.csv

Este script programa 6 reglas de negocio como funciones reutilizables,
genera un resumen de cumplimiento, y al final incluye los comandos Git
que los alumnos deben ejecutar para versionar este mismo archivo.
"""
import pandas as pd

clientes = pd.read_csv("clientes.csv")
pedidos = pd.read_csv("pedidos.csv")


# ---------------------------------------------------------------------
# Exploración inicial de los datasets
# ---------------------------------------------------------------------

def explorar_datasets(clientes_df, pedidos_df):
    """Muestra una vista general de ambos datasets antes de aplicar las reglas:
    dimensiones, tipos de dato, nulos, duplicados y valores categóricos."""
    print("=== Dimensiones ===")
    print(f"Clientes: {clientes_df.shape[0]} filas x {clientes_df.shape[1]} columnas")
    print(f"Pedidos:  {pedidos_df.shape[0]} filas x {pedidos_df.shape[1]} columnas\n")

    print("=== Vista previa de clientes ===")
    print(clientes_df.head(), "\n")

    print("=== Vista previa de pedidos ===")
    print(pedidos_df.head(), "\n")

    print("=== Tipos de dato y nulos (clientes) ===")
    clientes_df.info()
    print()

    print("=== Tipos de dato y nulos (pedidos) ===")
    pedidos_df.info()
    print()

    print("=== Estadísticas descriptivas (clientes) ===")
    print(clientes_df.describe(include="all"), "\n")

    print("=== Estadísticas descriptivas (pedidos) ===")
    print(pedidos_df.describe(include="all"), "\n")

    print("=== Filas duplicadas ===")
    print(f"Clientes: {clientes_df.duplicated().sum()} duplicados")
    print(f"Pedidos:  {pedidos_df.duplicated().sum()} duplicados\n")

    print("=== Valores únicos en columnas categóricas ===")
    print("Ciudades (clientes):", sorted(clientes_df["ciudad"].dropna().unique()))
    print("Canales de registro (clientes):", sorted(clientes_df["canal_registro"].dropna().unique()))
    print("Estados de pedido (pedidos):", sorted(pedidos_df["estado"].dropna().unique()))


# ---------------------------------------------------------------------
# Catálogo de reglas de negocio 
# ---------------------------------------------------------------------

def regla_email_valido(df):
    """R001 — Todo email debe contener '@' y no estar vacío."""
    return df[df["email"].isnull() | ~df["email"].astype(str).str.contains("@", na=False)]


def regla_cantidad_positiva(df):
    """R002 — La cantidad de un pedido debe ser mayor a cero."""
    return df[df["cantidad"] <= 0]


def regla_fecha_entrega_posterior(df):
    """R003 — La fecha de entrega no puede ser anterior a la fecha de pedido (consistencia)."""
    d = df.copy()
    d["fecha_pedido"] = pd.to_datetime(d["fecha_pedido"])
    d["fecha_entrega"] = pd.to_datetime(d["fecha_entrega"])
    return d[d["fecha_entrega"] < d["fecha_pedido"]]


def regla_integridad_cliente(pedidos_df, clientes_df):
    """R004 — Todo id_cliente en pedidos debe existir en clientes (integridad referencial)."""
    ids_validos = set(clientes_df["id_cliente"])
    return pedidos_df[~pedidos_df["id_cliente"].isin(ids_validos)]


def regla_no_duplicados_pedido(df):
    """R005 — No deben existir pedidos exactamente duplicados."""
    return df[df.duplicated()]


def regla_ciudad_normalizada(df):
    """R006 — El nombre de la ciudad no debe tener espacios extra ni variar en
    mayúsculas/minúsculas; debe estar en formato Título (ej. 'Lima')."""
    ciudad_normalizada = df["ciudad"].astype(str).str.strip().str.title()
    return df[df["ciudad"].notna() & (df["ciudad"].astype(str) != ciudad_normalizada)]


def ejecutar_todas_las_reglas(clientes_df, pedidos_df):
    """Corre las 6 reglas y devuelve un resumen de cumplimiento."""
    resultados = {
        "R001 Email válido (clientes)": regla_email_valido(clientes_df),
        "R002 Cantidad positiva (pedidos)": regla_cantidad_positiva(pedidos_df),
        "R003 Fecha entrega >= fecha pedido (pedidos)": regla_fecha_entrega_posterior(pedidos_df),
        "R004 Integridad referencial id_cliente (pedidos -> clientes)": regla_integridad_cliente(pedidos_df, clientes_df),
        "R005 Pedidos sin duplicados exactos": regla_no_duplicados_pedido(pedidos_df),
        "R006 Ciudad normalizada (clientes)": regla_ciudad_normalizada(clientes_df),
    }
    resumen = {nombre: len(df_errores) for nombre, df_errores in resultados.items()}
    return resultados, resumen


if __name__ == "__main__":
    explorar_datasets(clientes, pedidos)

    resultados, resumen = ejecutar_todas_las_reglas(clientes, pedidos)

    print("=== Resumen de cumplimiento de reglas ===")
    for nombre, n_errores in resumen.items():
        print(f"{nombre}: {n_errores} incumplimientos")

    # Guardar el detalle de errores de integridad referencial como evidencia
    resultados["R004 Integridad referencial id_cliente (pedidos -> clientes)"].to_csv(
        "errores_integridad_referencial.csv", index=False
    )
    print("\nDetalle de errores de integridad referencial guardado en "
          "errores_integridad_referencial.csv")


# ---------------------------------------------------------------------
# GUÍA RÁPIDA DE GIT — pasos a ejecutar en la terminal (no en Python)
# ---------------------------------------------------------------------
#
# 1) Inicializar el repositorio (una sola vez, dentro de la carpeta del proyecto):
#      git init
#
# 2) Ver el estado de los archivos:
#      git status
#
# 3) Agregar este script al área de preparación (staging):
#      git add Taller2_Solucion_Instructor.py
#
# 4) Confirmar el cambio con un mensaje descriptivo:
#      git commit -m "Agrega reglas de validacion R001-R005 para clientes y pedidos"
#
# 5) Ver el historial de commits:
#      git log --oneline
#
# 6) (Opcional) Conectar con un repositorio remoto en GitHub y subir el historial:
#      git remote add origin https://github.com/<usuario>/<repositorio>.git
#      git push -u origin main
#
# Entregable del Taller 2: este script + un repositorio Git local con al
# menos 2 commits + una captura de pantalla de "git log --oneline".
