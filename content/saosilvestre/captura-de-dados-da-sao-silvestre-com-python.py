import pandas as pd
import matplotlib.pyplot as plt
# ['fivethirtyeight', 'ggplot', 'dark_background', 'grayscale', 'bmh']
plt.style.use('ggplot')

ss = pd.read_csv("https://raw.githubusercontent.com/wilsonfreitas/saosilvestre/master/saosilvestre.csv")
ss.head()
ss_pais = ss.groupby('pais')
ss_pais.corrida.count()
ss_pais.corrida.count().sort(inplace=False).plot(kind='bar', figsize=(14,7))
plt.savefig('../figure/ss-pais-campeoes.png', bbox_inches='tight')