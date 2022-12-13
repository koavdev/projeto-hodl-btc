import mysql.connector
import azure_credentials as azure

connection = mysql.connector.connect(
    host=azure.host,
    user=azure.user,
    password=azure.password,
    port=azure.port,
    database=azure.database
)

cursor = connection.cursor()

# Retorna o usuário que está logado
def get_user(email,password):
    cursor.execute('SELECT * FROM usuarios WHERE email=%s AND password=%s',(email,password,))
    record = cursor.fetchone()
    return record

# Cadastra um novo usuário no banco
def insert_user(email,password):
    cursor.execute('INSERT INTO usuarios (email, password) VALUES (%s, %s)',(email,password))
    connection.commit()

# Insere uma nova transação no banco
def insert_transaction(data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,email_user):
    cursor.execute('INSERT INTO transacoes (data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,email_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,email_user))
    connection.commit()

# Retorna uma lista das transações do usuário filtradas por E-mail (que será utilizado para o RLS do PowerBI)
def get_transaction(email_user):
    cursor.execute('SELECT id_transacao,data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet FROM transacoes WHERE email_user=%s',(email_user,))
    record = cursor.fetchall()
    return record

# Atualiza uma transação
def update_transaction(data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,id_transacao):
    cursor.execute('UPDATE transacoes SET data=%s,tipo=%s,valor_brl=%s,valor_usd=%s,quantidade=%s,preco_brl=%s,preco_usd=%s,wallet=%s WHERE id_transacao=%s',(data,tipo,valor_brl,valor_usd,quantidade,preco_brl,preco_usd,wallet,id_transacao,))
    connection.commit()

# Deleta uma transação
def delete_transaction(id_transacao,email_user):
    cursor.execute('DELETE FROM transacoes WHERE id_transacao=%s AND email_user=%s',(id_transacao,email_user))
    connection.commit()