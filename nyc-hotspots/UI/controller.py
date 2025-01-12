import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        provider = self._view._ddProvider.value
        if provider is None:
            print("Seleziona un provider")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Seleziona un provider"))
            self._view.update_page()

            return
        self._view.txt_result.controls.clear()

        soglia = self._view._txtInDistanza.value
        if soglia == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Distanza non inserita"))
            self._view.update_page()
            return

        try:
            sogliaFloat = float(soglia)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"ATTENZIONE, soglia inserita non numerica"))
            self._view.update_page()
            return

        self._model.buildGrafo(provider, sogliaFloat)

        self._view.txt_result.controls.append(ft.Text(f"Il grafo è stato correttamente creato "))
        nNodes, nEdges = self._model.getGrafoDettagli()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi e {nEdges} archi"))

        self._view.update_page()

    def handleAnalizzaGrafo(self, e):
        nNodes, nEdges = self._model.getGrafoDettagli()
        if nNodes == 0 and nEdges==0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"ATTENZIONE, il grafo non è stato craeto correttamente, è vuoto"))
            self._view.update_page()
            return
        lista = self._model.getNodesMostVicini()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Nodi con più vicini"))
        for l in lista:
            self._view.txt_result.controls.append(
                ft.Text(f"{l[0]} -- {l[1]}"))
        self._view.update_page()

    def handleCalcolaPercorso(self, e):
        pass

    def fillDDProvider(self):
        providers = self._model.getAllProviders()
        providers.sort() #sono delle stringhe allora automaticamente sono in ordine alfabetico
        for p in providers:
            self._view._ddProvider.options.append(ft.dropdown.Option(p)) #Option(data=p, text=p, onclick=...)
            # ma qui non è necessario perchè p non è un oggetto ma una stringa
        self._view.update_page()

    def fillDDTarget(self):
        locations = self._model.getAllLocations()
        locationsDD = map(lambda x: ft.dropdown.Option(data=x, text=x.Location, on_click=self.readChoiceLocation), locations)
        self._view._ddTarget.options.extend(locationsDD)

    def readChoiceLocation(self, e):
        if e.control.data is None:
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data