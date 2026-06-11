from flask import Flask, request

app = Flask(__name__)

def controlla_otp_esterno(otp):
    if otp == "payload":
        raise ConnectionError("Impossibile contattare il server OTP esterno (Timeout).")
    return otp == "123456"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    otp = request.form.get('otp')
    autenticato = False
    
    try:
        if controlla_otp_esterno(otp):
            autenticato = True
    except Exception as e:
        print(f"[LOG SERVER] Errore critico di rete: {e}")
        # GESTIONE ECCEZIONE FALLIMENTARE (Fail-Open):
        # Pur di non bloccare l'utente in caso di guasto del server, il sistema fa passare!
        autenticato = True 

    if autenticato:
        return f'''
        <script src="https://cdn.tailwindcss.com"></script>
        <div class="min-h-screen bg-slate-900 flex items-center justify-center p-6">
            <div class="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl p-8 border border-green-500/30 text-center">
                <div class="w-16 h-16 bg-green-500/10 text-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <h1 class="text-2xl font-bold text-white mb-2">ACCESSO CONCESSO</h1>
                <p class="text-slate-400 mb-6">Benvenuto nel pannello di controllo, <span class="text-green-400 font-semibold">{username}</span>.</p>
                <div class="bg-slate-900 p-4 rounded-lg border border-slate-700 text-left font-mono text-xs text-green-400 break-all">
                    <strong>FLAG:</strong> IS{{FAIL_OPEN_SUCCESS}}
                </div>
            </div>
        </div>
        '''
    else:
        return '''
        <script src="https://cdn.tailwindcss.com"></script>
        <div class="min-h-screen bg-slate-900 flex items-center justify-center p-6">
            <div class="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl p-8 border border-red-500/30 text-center">
                <div class="w-16 h-16 bg-red-500/10 text-red-400 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </div>
                <h1 class="text-2xl font-bold text-white mb-2">ACCESSO NEGATO</h1>
                <p class="text-slate-400 mb-6">Il codice OTP inserito non è corretto.</p>
                <a href="/" class="inline-block bg-slate-700 hover:bg-slate-600 text-white font-medium py-2 px-4 rounded-lg transition">Riprova</a>
            </div>
        </div>
        ''', 401

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="min-h-screen bg-slate-900 flex items-center justify-center p-6">
        <div class="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl p-8 border border-slate-700">
            <div class="mb-6 text-center">
                <span class="bg-red-500/10 text-red-400 text-xs font-medium px-2.5 py-1 rounded-full border border-red-500/20">Ambiente Vulnerabile (Port 5003)</span>
                <h1 class="text-2xl font-bold text-white mt-3">Gateway Critico di Rete</h1>
                <p class="text-slate-400 text-sm mt-1">Richiesta autenticazione a due fattori (2FA)</p>
            </div>
            <form action="/login" method="post" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-1">ID Operatore</label>
                    <input type="text" name="username" placeholder="es. admin" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition">
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-1">Codice OTP</label>
                    <input type="text" name="otp" placeholder="Inserisci 'payload' per bypass" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition">
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 px-4 rounded-lg transition shadow-lg shadow-indigo-600/20">
                    Verifica Identità
                </button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)