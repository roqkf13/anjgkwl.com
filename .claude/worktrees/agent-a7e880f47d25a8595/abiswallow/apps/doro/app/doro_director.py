from fastapi import FastAPI

from doro.app.doro_reader import DoroReader


class DoroDirector:
    def __init__(self):
        pass
        

    def get_data(self):
        doro_reader = DoroReader()
        return doro_reader.get_data()


app = FastAPI(title="Doro DoroDirector API")



