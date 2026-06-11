from flask import Flask, request

app = Flask(__name__)

@app.route('/calcola-quota', methods=['GET'])
def calcola_quota():
    totale_fattura = 1000.0
    partecipanti = request.args.get('partecipanti')

    # COMPORTAMENTO VULNERABILE: Nessun controllo sul tipo di input o sullo zero.
    # L'esecuzione di operazioni aritmetiche su input non validi scatena un'eccezione a basso livello.
    quota = totale_fattura / float(partecipanti)
    
    return f'''
    <script src="https://cdn.tailwindcss.com"></script>
    <body class="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-sans">
        <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center border border-slate-100">
            <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            </div>
            <span class="bg-red-500/10 text-red-600 text-xs font-medium px-2.5 py-1 rounded-full border border-red-500/20">Ambiente Vulnerabile (Port 5001)</span>
            <h2 class="text-sm font-semibold text-slate-400 uppercase tracking-wider mt-4">Divisione Spese Ultimata</h2>
            <p class="text-4xl font-extrabold text-slate-900 mt-2">{quota:.2f} <span class="text-xl font-medium text-slate-500">EUR</span></p>
            <p class="text-sm text-slate-500 mt-2">Quota individuale calcolata su un totale di 1000.00 EUR</p>
            <div class="mt-6 pt-6 border-t border-slate-100">
                <a href="/" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">← Torna alla Home</a>
            </div>
        </div>
    </body>
    '''

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
                <span class="bg-red-500/10 text-red-600 text-xs font-medium px-2.5 py-1 rounded-full border border-red-500/20">Ambiente Vulnerabile (Port 5001)</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-3">Ripartizione Spese Spedizioni</h1>
                <p class="text-slate-500 text-sm mt-1">Inserisci il numero di dipendenti per dividere la fattura da 1000 EUR</p>
            </div>
            <form action="/calcola-quota" method="get" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Numero Partecipanti</label>
                    <input type="text" name="partecipanti" placeholder="Prova con '0' o una qualsiasi stringa" required class="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-indigo-500 transition">
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 px-4 rounded-lg transition shadow-lg shadow-indigo-600/20">
                    Calcola Quota Spesa
                </button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # ATTENZIONE: debug=True in produzione scatena l'interfaccia interattiva ed espone il codice sorgente
    app.run(host='0.0.0.0', port=5000, debug=True)