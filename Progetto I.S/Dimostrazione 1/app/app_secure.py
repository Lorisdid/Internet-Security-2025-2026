from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/calcola-quota', methods=['GET'])
def calcola_quota():
    totale_fattura = 1000.0
    partecipanti_raw = request.args.get('partecipanti')

    if not partecipanti_raw:
        return '''
        <script src="https://cdn.tailwindcss.com"></script>
        <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
            <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-6 border-l-4 border-amber-500">
                <div class="flex items-start">
                    <div class="ml-3">
                        <h3 class="text-sm font-semibold text-slate-900">Parametro Mancante</h3>
                        <p class="text-xs text-slate-500 mt-1">Specificare il parametro 'partecipanti' nell'interfaccia di calcolo.</p>
                        <a href="/" class="inline-block text-xs font-medium text-amber-600 hover:text-amber-500 mt-3">Torna alla Home</a>
                    </div>
                </div>
            </div>
        </body>
        ''', 400

    try:
        partecipanti = float(partecipanti_raw)
        if partecipanti == 0:
            return '''
            <script src="https://cdn.tailwindcss.com"></script>
            <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
                <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-6 border-l-4 border-amber-500">
                    <div class="flex items-start">
                        <div class="ml-3">
                            <h3 class="text-sm font-semibold text-slate-900">Operazione non valida</h3>
                            <p class="text-xs text-slate-500 mt-1">Il numero di partecipanti non può essere pari a zero.</p>
                            <a href="/" class="inline-block text-xs font-medium text-amber-600 hover:text-amber-500 mt-3">Torna alla Home</a>
                        </div>
                    </div>
                </div>
            </body>
            ''', 400
            
        quota = totale_fattura / partecipanti
        return f'''
        <script src="https://cdn.tailwindcss.com"></script>
        <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-sans">
            <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center border border-slate-100">
                <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                </div>
                <span class="bg-green-500/10 text-green-600 text-xs font-medium px-2.5 py-1 rounded-full border border-green-500/20">Ambiente Protetto (Port 5002)</span>
                <h2 class="text-sm font-semibold text-slate-400 uppercase tracking-wider mt-4">Divisione Spese Ultimata</h2>
                <p class="text-4xl font-extrabold text-slate-900 mt-2">{quota:.2f} <span class="text-xl font-medium text-slate-500">EUR</span></p>
                <p class="text-sm text-slate-500 mt-2">Quota individuale calcolata su un totale di 1000.00 EUR</p>
                <div class="mt-6 pt-6 border-t border-slate-100">
                    <a href="/" class="text-sm font-medium text-emerald-600 hover:text-emerald-500">← Torna alla Home</a>
                </div>
            </div>
        </body>
        '''

    except ValueError:
        return '''
        <script src="https://cdn.tailwindcss.com"></script>
        <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
            <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-6 border-l-4 border-amber-500">
                <div class="flex items-start">
                    <div class="ml-3">
                        <h3 class="text-sm font-semibold text-slate-900">Errore Input</h3>
                        <p class="text-xs text-slate-500 mt-1">Il valore inserito non corrisponde a un formato numerico valido.</p>
                        <a href="/" class="inline-block text-xs font-medium text-amber-600 hover:text-amber-500 mt-3">Torna alla Home</a>
                    </div>
                </div>
            </div>
        </body>
        ''', 400

# MITIGAZIONE GENERALE (CWE-209): Cattura qualunque eccezione imprevista senza mostrare lo stack trace
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.error(f"Eccezione non gestita intercettata in produzione: {error}", exc_info=True)
    return '''
    <script src="https://cdn.tailwindcss.com"></script>
    <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
        <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-6 border-l-4 border-red-500">
            <div class="flex items-start">
                <div class="ml-3">
                    <h3 class="text-sm font-semibold text-red-600">500 Internal Server Error</h3>
                    <p class="text-xs text-slate-500 mt-1">Si è verificato un errore interno di sistema. La richiesta non può essere evasa.</p>
                    <a href="/" class="inline-block text-xs font-medium text-red-600 hover:text-red-500 mt-3">Torna alla Home</a>
                </div>
            </div>
        </div>
    </body>
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
    <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
        <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
            <div class="mb-6 text-center">
                <span class="bg-green-500/10 text-green-600 text-xs font-medium px-2.5 py-1 rounded-full border border-green-500/20">Ambiente Protetto (Port 5002)</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-3">Ripartizione Spese Spedizioni</h1>
                <p class="text-slate-500 text-sm mt-1">Inserisci il numero di dipendenti per dividere la fattura da 1000 EUR</p>
            </div>
            <form action="/calcola-quota" method="get" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Numero Partecipanti</label>
                    <input type="text" name="partecipanti" placeholder="Inserisci un valore numerico" required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition">
                </div>
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2 px-4 rounded-lg transition shadow-lg shadow-emerald-600/20">
                    Calcola Quota Spesa
                </button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # In produzione debug=False impedisce la fuga di dati sensibili
    app.run(host='0.0.0.0', port=5000, debug=False)