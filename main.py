
from flask import Flask, render_template, url_for, request,send_from_directory
import Calcula
import db
#===================================================================

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route("/teladados")
def teladados():
  return render_template('teladados.html')

@app.route('/userarea', methods = ['POST', 'GET'])
def userarea():
  if request.method == 'POST':
    resultuserarea = request.form
    email = resultuserarea['email']
    password = resultuserarea['password']

    convert_ = db.query_email_confere(email, password)

    email_ = convert_[0]['EMAIL']
    password_ = convert_[0]['PASSWORD']
    name_user = convert_[0]['FIRST_NAME']

    status = True
    
    if email == '' or password == '':
      return f"""
        <p>Atenção, Todos os campos precisam ser preenchidos... :( </p>
        <br>
        <br>
        <br>
        <p><a href="/cotation"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

     """

    if email == email_.lower() and password == password_:
      return render_template("userarea.html", title='Python_Flask', status=status, name_user=name_user.lower().capitalize())
    else:
      return render_template("message.html", email=email)

@app.route('/result', methods = ['POST', 'GET'])
def result():

  if request.method == 'POST':
    resultcep = request.form
    print(resultcep)
    consultCEP = resultcep['cep']
    print(consultCEP)

    dados = Calcula.calculogeral(consultCEP)
    tal_log = Calcula.consultlog_lat(consultCEP)

    print(dados)
    print(tal_log)

    lat = tal_log[0]
    log = tal_log[1]

    return render_template("result.html", consultCEP=consultCEP,  lat=lat, log=log, tables=[dados.to_html(classes='data')], titles=dados.columns.values)
   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)

