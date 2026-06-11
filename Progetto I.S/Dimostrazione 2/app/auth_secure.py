from flask import Flask, request

app = Flask(__name__)

def controlla_otp_esterno(otp):
    if otp == "scatena_errore":
        raise ConnectionError("Impossibile contattare il server OTP esterno (Timeout).")
    return otp == "123456"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    otp = request.form.get('otp')
    
    try:
        if controlla_otp_esterno(otp):
            return f'''
            <script src="https://cdn.tailwindcss.com"></script>
            <div class="min-h-screen bg-slate-900 flex items-center justify-center p-6">
                <div class="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl p-8 border border-green-500/30 text-center">
                    <div class="w-16 h-16 bg-green-500/10 text-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    </div>
                    <h1 class="text-2xl font-bold text-white mb-2">ACCESSO CONCESSO</h1>
                    <p class="text-slate-400 mb-6">Autenticazione riuscita per l'utente: <span class="text-green-400 font-semibold">{username}</span>.</p>
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
                    <p class="text-slate-400 mb-6">Codice OTP non valido.</p>
                    <a href="/" class="inline-block bg-slate-700 hover:bg-slate-600 text-white font-medium py-2 px-4 rounded-lg transition">Riprova</a>
                </div>
            </div>
            ''', 401
            
    except Exception as e:
        print(f"[LOG SERVER SICURO] Eccezione intercettata in sicurezza: {e}")
        # APPLICAZIONE DEL PRINCIPIO FAIL-SAFE:
        # In caso di errore imprevisto, l'accesso viene categoricamente negato.
        return '''
        <script src="https://cdn.tailwindcss.com"></script>
        <div class="min-h-screen bg-slate-900 flex items-center justify-center p-6">
            <div class="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl p-8 border border-amber-500/30 text-center">
                <div class="w-16 h-16 bg-amber-500/10 text-amber-400 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                </div>
                <h1 class="text-2xl font-bold text-white mb-2">ERRORE DI SISTEMA</h1>
                <p class="text-slate-400 mb-6">Servizio di autenticazione momentaneamente non disponibile. Riprova più tardi.</p>
                <a href="/" class="inline-block bg-amber-600 hover:bg-amber-500 text-white font-medium py-2 px-4 rounded-lg transition">Torna alla Home</a>
            </div>
        </div>
        ''', 500

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
                <span class="bg-green-500/10 text-green-400 text-xs font-medium px-2.5 py-1 rounded-full border border-green-500/20">Ambiente Protetto (Port 5004)</span>
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
                    <input type="text" name="otp" placeholder="Inserisci OTP" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition">
                </div>
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2 px-4 rounded-lg transition shadow-lg shadow-emerald-600/20">
                    Verifica Identità
                </button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)