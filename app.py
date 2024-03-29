# Module Imports
import base64, flask, dash_mantine_components as dmc, sys
from dash import Dash, page_container, Output, Input, State, html
from dash_auth.auth import Auth
from datetime import datetime
from os import listdir, path, getcwd

# Logs
# log = logging.getLogger("werkzeug")
# log.setLevel(logging.WARNING)

# Auth
class MHALAuth(Auth):
    def __init__(self, app):
        Auth.__init__(self, app)

    def is_authorized(self):
        out = {}
        if path.exists(path.join("configuration", "users.cfg")):
            with open(path.join("configuration", "users.cfg"), "r", encoding="utf-8") as f:
                for raw in f.read().removesuffix("\n").strip().split("\n"):
                    user = raw.split(";")
                    out.update({user[0]: user[1].replace("<secret1>", str(int(float(datetime.now().month*datetime.now().day+3))))})
        else:
            with open(path.join("configuration", "users.cfg"), "w") as f: f.write("")

        self._users = (
            out
            if isinstance(out, dict)
            else {k: v for k, v in out}
        )

        header = flask.request.headers.get("Authorization", None)
        if not header:
            return False
        username_password = base64.b64decode(header.split("Basic ")[1])
        username_password_utf8 = username_password.decode("utf-8")
        username, password = username_password_utf8.split(":", 1)
        return self._users.get(username) == password

    def login_request(self):
        return flask.Response(
            "Login Required",
            headers={"WWW-Authenticate": 'Basic realm="User Visible Realm"'},
            status=401
        )

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()
        return wrap

# App
server = flask.Flask(__name__)
app = Dash(__name__, server=server, title="MHAL Panel", update_title="MHAL Panel", use_pages=True, pages_folder=path.join(getcwd(), "pages"), meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0,"}])
if sys.platform.startswith("win"): pass
else: auth = MHALAuth(app)
app._favicon = path.join(getcwd(), "assets", "favicon.png")

@server.errorhandler(500)
def internal_server_error(e):
    return """
    <div class="container">
    <a class="button" href="#" onClick='window.location.reload();' style="--color:#1971C2;">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        Oturumu Başlat
    </a>
    </div>

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;300;400;500;600;700;800;900&display=swap');

    * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
    }

    .container {
    width: 100%;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 120px;
    background: #1A1B1E;
    }

    .button {
    position: relative;
    padding: 16px 30px;
    font-size: 1.5rem;
    color: var(--color);
    border: 2px solid #25262B;
    border-radius: 4px;
    text-shadow: 0 0 15px var(--color);
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.1rem;
    transition: 0.5s;
    z-index: 99;
    background-color: #25262B;
    }

    .button:hover {
    color: #fff;
    border: 2px solid rgba(0, 0, 0, 0);
    box-shadow: 0 0 0px var(--color);
    }

    .button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--color);
    z-index: -1;
    transform: scale(0);
    transition: 0.5s;
    }

    .button:hover::before {
    transform: scale(1);
    transition-delay: 0.5s;
    box-shadow: 0 0 10px var(--color),
        0 0 30px var(--color),
        0 0 60px var(--color);
    }

    .button span {
    position: absolute;
    background: var(--color);
    pointer-events: none;
    border-radius: 2px;
    /*box-shadow: 0 0 10px var(--color),
        0 0 20px var(--color),
        0 0 30px var(--color),
        0 0 50px var(--color),
        0 0 100px var(--color);*/
    transition: 0.5s ease-in-out;
    transition-delay: 0.25s;
    }

    .button:hover span {
    opacity: 0;
    transition-delay: 0s;
    }

    .button span:nth-child(1),
    .button span:nth-child(3) {
    width: 40px;
    height: 4px;
    }

    .button:hover span:nth-child(1),
    .button:hover span:nth-child(3) {
    transform: translateX(0);
    }

    .button span:nth-child(2),
    .button span:nth-child(4) {
    width: 4px;
    height: 40px;
    }

    .button:hover span:nth-child(1),
    .button:hover span:nth-child(3) {
    transform: translateY(0);
    }

    .button span:nth-child(1) {
    top: calc(50% - 2px);
    left: -50px;
    transform-origin: left;
    }

    .button:hover span:nth-child(1) {
    left: 50%;
    }

    .button span:nth-child(3) {
    top: calc(50% - 2px);
    right: -50px;
    transform-origin: right;
    }

    .button:hover span:nth-child(3) {
    right: 50%;
    }

    .button span:nth-child(2) {
    left: calc(50% - 2px);
    top: -50px;
    transform-origin: top;
    }

    .button:hover span:nth-child(2) {
    top: 50%;
    }

    .button span:nth-child(4) {
    left: calc(50% - 2px);
    bottom: -50px;
    transform-origin: bottom;
    }

    .button:hover span:nth-child(4 ) {
    bottom: 50%;
    }
    </style>
    """

app.layout = dmc.MantineProvider(
    children=[
        page_container,
    ],
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    withCSSVariables=True
)

# Callbacks
@app.callback(
    Output("sorgu-sinav-indisi", "data"), Output("sorgu-sinav-indisi", "value"), 
    Input("sorgu-ogretim-yili", "value")
)
def indis_yenile(ogretim_yili):
    return [{"value": ind, "label": ind.removesuffix(".xlsx")} for ind in sorted(listdir(path.join("database", str(ogretim_yili))), key=lambda w: int(str(w[0])+str(w[1])))], listdir(path.join("database", str(ogretim_yili)))[-1] if len(listdir(path.join("database", str(ogretim_yili)))) > 0 else None

@app.callback(
    Output("sorgu-sinav-getir", "href"), 
    Input("sorgu-sinav-indisi", "value"),
    State("sorgu-ogretim-yili", "value")
)
def sinav_getir(indi, ogr_yili):
    try: return f"sinav/{ogr_yili}_{indi.split(' - ')[0]}"
    except: return "sinav/x_x"

@app.callback(
    Output("sorgu-ogrenci-table", "children"),
    Input("sorgu-ogrenci-filtrele", "n_clicks"),
    State("sorgu-ogrenci-adi", "value"), State("sorgu-ogrenci-numarasi", "value"), State("sorgu-ogrenci-sinifi", "value")
)
def ogrenci_filtrele(n_clicks, ograd, ogrno, ogrsn):
    import pandas as pd
    from unidecode import unidecode as ud
    from dash import html
    import dash_mantine_components as dmc
    out, readies, order = [], [], []
    for ogry in listdir(path.join("database")):
        for xlsx in listdir(path.join("database", ogry)):
            if xlsx.endswith(".xlsx"):
                table = pd.read_excel(path.join("database", ogry, xlsx))
                for numara, isim, sinif in zip(table["Numara"], table["İsim"], table["Sınıf"]):
                    if (ud(str(ograd).replace("None","").replace(" ","").upper()) in ud(str(isim).replace(" ","").upper()) or ud(str(ograd).replace("None","").replace(" ","").upper()) == "") \
                        and (ud(str(ogrno).replace("None","").replace(" ","").upper()) in ud(str(numara).replace(" ","").upper()) or ud(str(ogrno).replace("None","").replace(" ","").upper()) == "") \
                            and (ud(str(ogrsn).replace("None","").replace(" ","").upper()) in ud(str(sinif).replace(" ","").upper()) or ud(str(ogrsn).replace("None","").replace(" ","").upper()) == ""):
                        isim = str(isim).upper()
                        if str(isim).lower().split()[0].strip() == str(isim).lower().strip(): isim = str(isim) + " X"
                        elem = html.Tr([html.Td(str(numara)), html.Td(isim.upper()), html.Td(sinif), html.A(children=dmc.Button("Profil"), href=f"/ogrenci/{numara}_{ud(isim.lower().replace(' ',''))}")])
                        if not (numara, isim, sinif) in readies:
                            out.append(elem)
                            readies.append((numara, isim, sinif))
                            order.append(numara)
    rows = [x for _, x in sorted(zip(order, out), key=lambda pair: pair[0])]
    for i in range(len(rows)): rows[i].style={"background-color": "transparent" if i%2 else "#2C2E33"}
    return rows

@app.callback(
    Output("sonuc-ogrenci-table", "children"), Output("ogrenci-net-chart", "figure"), Output("ogrenci-puan-chart", "figure"),
    Input("sonuc-sorgu-getir", "n_clicks"),
    State("sonuc-ogretim-yili", "value"), State("ogrenci-bilgi-isim", "children"), State("ogrenci-bilgi-sinif", "children"), State("ogrenci-bilgi-numara", "children")
)
def sonuc_getir(n_clicks, ogr_yili, isim, sinif, numara):
    from unidecode import unidecode as ud
    import dash_mantine_components as dmc
    from dash import html

    def get_rows2(i, y):
        import pandas as pd
        from unidecode import unidecode as ud
        
        out = []
        for x in sorted(listdir(path.join("database", y)), key=lambda w: int(str(w[0])+str(w[1]))):
            if x.endswith(".xlsx"):
                df = pd.read_excel(path.join("database", y, x))
                r = None
                for id, di in enumerate(df["İsim"].tolist()):
                    if ud(str(di).lower().replace(" ","")) == ud(str(i).lower().replace(" ","")): r = id
                if r != None: out.append([str(x).removesuffix(".xlsx")+" "+y]+df.iloc[r].tolist())
        for o in range(len(out)):
            del out[o][2]
            del out[o][2]
            del out[o][2]
        for a in range(len(out)):
            for b in range(len(out[a])):
                if str(out[a][b]).replace("/","").replace(" ","").isdigit() and "/" in str(out[a][b]):
                    out[a][b] = int(float(str(out[a][b]).split("/")[0]))
        return out

    rows = get_rows2(isim, ogr_yili)

    table = [html.Tr([html.Td(str(i)) for i in row] + [html.A(dmc.Button("Tablo"), href=f"/sinav/{ogr_yili}_{str(row[0]).split(' - ')[0].strip()}")], style={"background-color": "transparent" if rows.index(row)%2 else "#2C2E33"}) for row in rows]

    net_fig = {
        "data": [
            {"x": [ud(str(row[0]).split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[4]) for row in rows], "text": [str(float(row[4])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Toplam"},
            {"x": [ud(str(row[0]).split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[7]) for row in rows], "text": [str(float(row[7])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Türkçe"},
            {"x": [ud(str(row[0]).split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[10]) for row in rows], "text": [str(float(row[10])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Sosyal"},
            {"x": [ud(str(row[0]).split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[13]) for row in rows], "text": [str(float(row[13])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Matematik"},
            {"x": [ud(str(row[0]).split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[16]) for row in rows], "text": [str(float(row[16])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Fen"},
        ],
        "layout": {
            "plot_bgcolor": "#25262B",
            "paper_bgcolor": "#25262B",
            "font": {"color": "#DFDFDF"},
            "margin": dict(l=0, r=0, t=0, b=50),
            "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            "xaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
            "yaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
        }
    }

    puan_fig = {
        "data": [
            {"x": [ud(str(row[0]).split("(")[-1].split(")")[0].strip()) for row in rows], "y": [round(float(row[7])*3.3 + float(row[10])*3.4 + float(row[13])*3.3 + float(row[16])*3.4 + 100, 3)  for row in rows], "text": [str(round(float(row[7])*3.3 + float(row[10])*3.4 + float(row[13])*3.3 + float(row[16])*3.4 + 100, 3))  for row in rows], "hovertext": [ud(str(row[0]).split("-")[1].split("(")[0].strip()) for row in rows], "type": "marker", "name": "Puan"},
        ],
        "layout": {
            "plot_bgcolor": "#25262B",
            "paper_bgcolor": "#25262B",
            "font": {"color": "#DFDFDF"},
            "margin": dict(l=0, r=0, t=0, b=50),
            "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            "xaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
            "yaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
        }
    }
    return table, net_fig, puan_fig

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)
