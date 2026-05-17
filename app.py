from flask import Flask, render_template, request
import requests, json, os

app = Flask(__name__)
CACHE_FILE = 'pokemon_cache.json'

def fetch_from_api(limit=151):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    pokemon_list = []
    for item in data['results']:
        detail = requests.get(item['url'], timeout=10).json()
        try:
            species = requests.get(detail['species']['url'], timeout=10).json()
            deskripsi = ''
            for entry in species.get('flavor_text_entries', []):
                if entry['language']['name'] == 'en':
                    deskripsi = entry['flavor_text'].replace('\n',' ').replace('\f',' ')
                    break
        except Exception:
            deskripsi = ''
        artwork = detail['sprites']['other']['official-artwork']
        pokemon_list.append({
            'id':           detail['id'],
            'nama':         detail['name'].capitalize(),
            'gambar':       artwork.get('front_default') or detail['sprites'].get('front_default',''),
            'gambar_shiny': artwork.get('front_shiny',''),
            'tipe':         [t['type']['name'].capitalize() for t in detail['types']],
            'tinggi':       round(detail['height']/10, 1),
            'berat':        round(detail['weight']/10, 1),
            'hp':           detail['stats'][0]['base_stat'],
            'attack':       detail['stats'][1]['base_stat'],
            'defense':      detail['stats'][2]['base_stat'],
            'sp_atk':       detail['stats'][3]['base_stat'],
            'sp_def':       detail['stats'][4]['base_stat'],
            'speed':        detail['stats'][5]['base_stat'],
            'total':        sum(s['base_stat'] for s in detail['stats']),
            'abilities':    [a['ability']['name'].replace('-',' ').title() for a in detail['abilities']],
            'deskripsi':    deskripsi,
        })
    return pokemon_list

def ambil_semua_pokemon():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE,'r') as f:
                data = json.load(f)
            if len(data) >= 50:
                return data, None
        except Exception:
            pass
    try:
        data = fetch_from_api(151)
        with open(CACHE_FILE,'w') as f:
            json.dump(data, f)
        return data, None
    except Exception:
        return DATA_LOKAL, None

@app.route('/')
def halaman_utama():
    pokemon_list, error = ambil_semua_pokemon()
    q           = request.args.get('q','').strip().lower()
    tipe_filter = request.args.get('tipe','').strip().lower()
    sort_by     = request.args.get('sort','id')
    filtered = pokemon_list
    if q:
        filtered = [p for p in filtered if q in p['nama'].lower() or q in str(p['id'])]
    if tipe_filter:
        filtered = [p for p in filtered if tipe_filter in [t.lower() for t in p['tipe']]]
    sort_map = {
        'id':      lambda p: p['id'],
        'nama':    lambda p: p['nama'],
        'hp':      lambda p: -p['hp'],
        'attack':  lambda p: -p['attack'],
        'defense': lambda p: -p['defense'],
        'speed':   lambda p: -p['speed'],
        'total':   lambda p: -p['total'],
    }
    filtered.sort(key=sort_map.get(sort_by, sort_map['id']))
    semua_tipe = sorted(set(t for p in pokemon_list for t in p['tipe']))
    return render_template('index.html',
        pokemon_list=filtered, semua_tipe=semua_tipe,
        total_all=len(pokemon_list), total=len(filtered),
        q=q, tipe_filter=tipe_filter, sort_by=sort_by, error=error)

@app.route('/detail/<int:pokemon_id>')
def detail(pokemon_id):
    pokemon_list, _ = ambil_semua_pokemon()
    pokemon = next((p for p in pokemon_list if p['id'] == pokemon_id), None)
    if not pokemon:
        return "<h1>404</h1>", 404
    prev_p = next((p for p in pokemon_list if p['id'] == pokemon_id-1), None)
    next_p = next((p for p in pokemon_list if p['id'] == pokemon_id+1), None)
    return render_template('detail.html', p=pokemon, prev_p=prev_p, next_p=next_p)

@app.route('/ranking')
def ranking():
    pokemon_list, error = ambil_semua_pokemon()
    sort_by = request.args.get('sort','total')
    sort_map = {
        'total':   lambda p: -p['total'],
        'hp':      lambda p: -p['hp'],
        'attack':  lambda p: -p['attack'],
        'defense': lambda p: -p['defense'],
        'sp_atk':  lambda p: -p['sp_atk'],
        'sp_def':  lambda p: -p['sp_def'],
        'speed':   lambda p: -p['speed'],
    }
    ranked = sorted(pokemon_list, key=sort_map.get(sort_by, sort_map['total']))
    return render_template('ranking.html', ranked=ranked, sort_by=sort_by, error=error)

@app.route('/compare')
def compare():
    pokemon_list, _ = ambil_semua_pokemon()
    id1 = request.args.get('p1', type=int)
    id2 = request.args.get('p2', type=int)
    p1 = next((p for p in pokemon_list if p['id'] == id1), None) if id1 else None
    p2 = next((p for p in pokemon_list if p['id'] == id2), None) if id2 else None
    return render_template('compare.html', pokemon_list=pokemon_list, p1=p1, p2=p2)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

DATA_LOKAL = [
    {'id':1,  'nama':'Bulbasaur', 'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/1.png','tipe':['Grass','Poison'],'tinggi':0.7,'berat':6.9,'hp':45,'attack':49,'defense':49,'sp_atk':65,'sp_def':65,'speed':45,'total':318,'abilities':['Overgrow'],'deskripsi':'A strange seed was planted on its back at birth.'},
    {'id':4,  'nama':'Charmander','gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/4.png','tipe':['Fire'],'tinggi':0.6,'berat':8.5,'hp':39,'attack':52,'defense':43,'sp_atk':60,'sp_def':50,'speed':65,'total':309,'abilities':['Blaze'],'deskripsi':'The flame on its tail indicates Charmanders life force.'},
    {'id':6,  'nama':'Charizard', 'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/6.png','tipe':['Fire','Flying'],'tinggi':1.7,'berat':90.5,'hp':78,'attack':84,'defense':78,'sp_atk':109,'sp_def':85,'speed':100,'total':534,'abilities':['Blaze'],'deskripsi':'It spits fire hot enough to melt boulders.'},
    {'id':7,  'nama':'Squirtle',  'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/7.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/7.png','tipe':['Water'],'tinggi':0.5,'berat':9.0,'hp':44,'attack':48,'defense':65,'sp_atk':50,'sp_def':64,'speed':43,'total':314,'abilities':['Torrent'],'deskripsi':'Shoots water at high velocity using its mouth.'},
    {'id':25, 'nama':'Pikachu',   'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/25.png','tipe':['Electric'],'tinggi':0.4,'berat':6.0,'hp':35,'attack':55,'defense':40,'sp_atk':50,'sp_def':50,'speed':90,'total':320,'abilities':['Static'],'deskripsi':'When several gather their electricity can cause lightning storms.'},
    {'id':94, 'nama':'Gengar',    'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/94.png','tipe':['Ghost','Poison'],'tinggi':1.5,'berat':40.5,'hp':60,'attack':65,'defense':60,'sp_atk':130,'sp_def':75,'speed':110,'total':500,'abilities':['Cursed Body'],'deskripsi':'It is said to emerge from darkness to steal the lives of those who become lost in mountains.'},
    {'id':130,'nama':'Gyarados',  'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/130.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/130.png','tipe':['Water','Flying'],'tinggi':6.5,'berat':235.0,'hp':95,'attack':125,'defense':79,'sp_atk':60,'sp_def':100,'speed':81,'total':540,'abilities':['Intimidate'],'deskripsi':'It is virtually impossible to stop once it has been enraged.'},
    {'id':143,'nama':'Snorlax',   'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/143.png','tipe':['Normal'],'tinggi':2.1,'berat':460.0,'hp':160,'attack':110,'defense':65,'sp_atk':65,'sp_def':110,'speed':30,'total':540,'abilities':['Immunity'],'deskripsi':'Very lazy. Just eats and sleeps.'},
    {'id':149,'nama':'Dragonite', 'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/149.png','tipe':['Dragon','Flying'],'tinggi':2.2,'berat':210.0,'hp':91,'attack':134,'defense':95,'sp_atk':100,'sp_def':100,'speed':80,'total':600,'abilities':['Inner Focus'],'deskripsi':'An extremely rarely seen marine pokemon.'},
    {'id':150,'nama':'Mewtwo',    'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/150.png','tipe':['Psychic'],'tinggi':2.0,'berat':122.0,'hp':106,'attack':110,'defense':90,'sp_atk':154,'sp_def':90,'speed':130,'total':680,'abilities':['Pressure'],'deskripsi':'A pokemon created by genetic manipulation.'},
    {'id':151,'nama':'Mew',       'gambar':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/151.png','gambar_shiny':'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/151.png','tipe':['Psychic'],'tinggi':0.4,'berat':4.0,'hp':100,'attack':100,'defense':100,'sp_atk':100,'sp_def':100,'speed':100,'total':600,'abilities':['Synchronize'],'deskripsi':'So rare that it is still said to be a mirage by many experts.'},
]

if __name__ == '__main__':
    app.run(debug=True)
