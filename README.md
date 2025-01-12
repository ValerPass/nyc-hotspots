a. Si permetta all’utente di inserire una distanza x espressa in km (anche con la virgola) e di selezionare, dall’apposito menu a tendina, un provider p tra quelli presenti nella colonna Provider 
(ordinati alfabeticamente).
b. Alla pressione del bottone “Crea Grafo” si costruisca un grafo semplice, pesato, e non orientato, i cui vertici
corrispondano alle località l distinte (colonna Location) in cui opera il provider p.
c. Due località l1 e l2 sono collegate da un arco se la distanza tra le due località è minore o uguale alla soglia x 
inserita dall’utente. Per calcolare tale distanza, si utilizzi la libreria simplelatlng1 (già inclusa nel progetto base), 
considerando, per ogni località, la media delle latitudini e longitudini degli hotspot installati dal provider p in tale 
località. Il peso dell’arco, sempre positivo, rappresenta la distanza tra le due località.
d. Alla pressione del bottone “Analisi Grafo”, trovare e stampare i vertici del grafo che hanno il maggior numero di vicini. Per ogni vertice, stampare il nome della località e il numero (massimo) di vicini.
