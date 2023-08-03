from flask import Flask, render_template, request
import pandas as pd
from ConnDB import DB


#dt = DB(request.form['nome'])
#df = dt.vol_car()
#print(df)
dt = pd.read_csv(r"C:\Users\pcp03\Desktop\exportar.csv")
df = pd.DataFrame(dt, columns=['CARREGAMENTO', 'CODIGO_VOLUME', 'COD_ITEM', 'DESC_TECNICA', 'QTDE'])

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not df.empty:
        result = None
        if request.method == 'POST':
            car = request.form['car']
            item = request.form['item']
            #dt = DB(car)
            #df = dt.vol_car()
            if car and item:
                result = df[(df['CARREGAMENTO'] == int(car)) & (df['COD_ITEM'] == int(item))]
            elif car:
                result = df[df['CARREGAMENTO'] == int(car)]
            elif item:
                result = df[df['COD_ITEM'] == int(item)]
            else:
                df.copy()
        else:
            result = df.head(0)
    else:
        return render_template(r"simple.html")
    return render_template(r"simple.html", result=result)


if __name__ == '__main__':
    app.run(host='10.40.3.48', port=8000)
