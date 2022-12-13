from flask import Flask, render_template, request, session, redirect, url_for
import azure_db as db

app = Flask(__name__)

app.secret_key = 'super secret key123'


# /
@app.route('/')
def index():
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        email_user = session['email']        
        transactions = db.get_transaction(email_user)
        return render_template('transactions.html',transactions=transactions,email=session['email'])
    

# Home
@app.route('/home')
def home():
    try:
        if request.method == 'GET' and session.get('email'):
            # Carregar com as transações do usuário recém logado       
            return render_template('home.html', email=session['email'])
    except:
        return "<h1>Você não tem acesso a essa página!</h1>"

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if not session.get('email'):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = db.get_user(email,password)

            if user:
                session['email'] = user[1]
                return redirect(url_for('home'))
            else:  
                msg = 'ERRO: E-mail ou senha incorreto.'

        return render_template('login.html', msg=msg)
    else:
        return redirect('/home')

# Logout
@app.route('/logout')
def logout():
    #for key in list(session.keys()):
     #   session.pop(key)
    session['email'] = None
    return render_template('login.html')
    
# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('email'):
        if request.method == 'GET':
            return render_template('register.html')
        else:
            email = request.form['email']
            password = request.form['password']
            db.insert_user(email,password)

            session['email'] = email
            return redirect('/home')
    else:
        return redirect('/home')

# Transactions
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    msg = ''
    if session.get('email'):
        if request.method == 'GET':
            email_user = session['email']

            # Coleta as transações do usuário logado
            transactions = db.get_transaction(email_user)

            # Print no console para ver Output
            for x in transactions:
                print(x)
        else:
            data = request.form['data']
            tipo = request.form['tipo']
            if request.form['valor_brl'] == '':
                valor_brl = 0
            else:
                valor_brl = float(request.form['valor_brl'].replace(',','.'))

            if  request.form['valor_usd'] == '':            
                valor_usd = 0
            else:
                valor_usd = float(request.form['valor_usd'].replace(',','.'))

            if  request.form['quantidade'] == '':            
                quantidade = 0
            else:
                quantidade = float(request.form['quantidade'].replace(',','.'))
            
            if request.form['preco_brl'] == '':
                preco_brl = 0
            else: preco_brl = float(request.form['preco_brl'].replace(',','.'))

            if request.form['preco_usd'] == '':
                preco_usd = 0
            else:
                preco_usd = float(request.form['preco_usd'].replace(',','.'))
                
            wallet = request.form['wallet']
            email_user = session['email']

            # Envia a transação para o banco
            db.insert_transaction(data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,email_user)

            # Coleta as transações do usuário logado
            transactions = db.get_transaction(email_user)

            # Msg que aparece ao lado do submit na pagina transactions.html
            msg = 'Transaction registered.'

            return render_template('transactions.html', transactions=transactions, msg=msg, email=session['email'])
                
        return render_template('transactions.html', transactions=transactions, email=session['email'])

@app.route('/update', methods=['POST'])
def update():
    id_transacao = request.form['id_transacao']
    data = request.form['data']
    tipo = request.form['tipo']
    if request.form['valor_brl'] == '':
            valor_brl = 0
    else:
        valor_brl = float(request.form['valor_brl'].replace(',','.'))

        if  request.form['valor_usd'] == '':            
            valor_usd = 0
        else:
            valor_usd = float(request.form['valor_usd'].replace(',','.'))

        quantidade = float(request.form['quantidade'].replace(',','.'))
        
        if request.form['preco_brl'] == '':
            preco_brl = 0
        else: preco_brl = float(request.form['preco_brl'].replace(',','.'))

        if request.form['preco_usd'] == '':
            preco_usd = 0
        else:
            preco_usd = float(request.form['preco_usd'].replace(',','.'))
    wallet = request.form['wallet']
    #email_user = session['email']

    db.update_transaction(data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,id_transacao)

    return redirect(url_for('transactions'))

@app.route('/delete/<string:id_transacao>',methods=['GET'])
def delete(id_transacao):
    email_user = session['email']
    db.delete_transaction(id_transacao,email_user)
    return redirect(url_for('transactions'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session.get('email'):
        return render_template('dashboard.html',email=session['email'])

@app.errorhandler(404)
def page_not_found(e):
    if session.get('email'):
        return render_template('404.html',email=session['email']), 404
    else:
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    if session.get('email'):
        return render_template('500.html', email=session['email'])
    else:
        return render_template('500.html')


if __name__ == '__main__':
    app.run(debug=True)
