from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash_messages'

EXCEL_FILE = 'users.xlsx'
LOG_FILE = 'password_log.txt'

def cargar_usuarios():
    try:
        df = pd.read_excel(EXCEL_FILE)
        return df
    except Exception as e:
        print(f"Error al cargar el archivo Excel: {e}")
        return pd.DataFrame(columns=['numero_usuario', 'contraseña'])

def guardar_usuarios(df):
    df.to_excel(EXCEL_FILE, index=False)

def registrar_log(numero_usuario, old_password, new_password, cambio_exitoso):
    with open(LOG_FILE, 'a') as log_file:
        if cambio_exitoso:
            # Registro de log en una sola línea en caso de éxito
            log_file.write(f"{datetime.now()} - Usuario {numero_usuario}: cambio de contraseña - éxito | "
                           f"Contraseña antigua: {old_password} -> Nueva contraseña: {new_password}\n")
        else:
            # Registro de log en una sola línea en caso de fallo
            log_file.write(f"{datetime.now()} - Usuario {numero_usuario}: cambio de contraseña - fallo | "
                           f"Contraseña antigua proporcionada: {old_password}\n")



@app.route('/cambiar_contraseña', methods=['GET', 'POST'])
def cambiar_contraseña():
    if request.method == 'POST':
        numero_usuario = request.form['numero_usuario']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        df = cargar_usuarios()
        usuario = df[(df['numero_usuario'] == int(numero_usuario)) & (df['contraseña'] == old_password)]

        if not usuario.empty:
            df.loc[df['numero_usuario'] == int(numero_usuario), 'contraseña'] = new_password
            guardar_usuarios(df)
            registrar_log(numero_usuario, old_password, new_password, True)
            flash('Contraseña cambiada con éxito.', 'success')
        else:
            registrar_log(numero_usuario, old_password, new_password, False)
            flash('Número de usuario o contraseña incorrecta.', 'danger')
        return redirect(url_for('cambiar_contraseña'))

    return render_template('cambiar_contraseña.html')


if __name__ == '__main__':
    app.run(debug=True)
