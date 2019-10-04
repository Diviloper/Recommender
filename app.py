import json
import os

from flask import Flask, Response
from flask import request
import copy

app = Flask(__name__)


def load_data():
    filename = os.path.join(app.static_folder, 'data.json')
    with open(filename) as blog_file:
        return json.load(blog_file)


class Dataset(object):
    def __init__(self) -> None:
        super().__init__()
        data = load_data()
        print(data)
        self.sectors_dataset = data['sectors']
        self.t_estudis_dataset = data['t_estudis']
        self.empresa_dataset = data['empresa']
        self.pasta_dataset = data['pasta']
        self.people = data['people']


class User:

    def __init__(self, dataset, sectors_si, sectors_no, t_estudis, empresa, pasta) -> None:
        super().__init__()
        self.dataset = dataset
        self.sectors_si = self.transform(sectors_si, self.dataset.sectors_dataset)
        self.sectors_no = self.transform(sectors_no, self.dataset.sectors_dataset)
        self.t_estudis = self.transform(t_estudis, self.dataset.t_estudis_dataset)
        self.empresa = self.transform(empresa, self.dataset.empresa_dataset)
        self.pasta = self.transform(pasta, self.dataset.pasta_dataset)

    @staticmethod
    def transform(data, dataset):
        data_t = copy.deepcopy(dataset)
        for d in data:
            data_t[d] = True
        return data_t.values()


def recommend(user, people):
    pass


@app.route('/recommendation', methods=['POST'])
def new_recommendation():
    data = request.json

    dataset = Dataset()

    sectors_si = data['sectorsSi']
    sectors_no = data['sectorsNo']
    t_estudis = data['tEstudis']
    empresa = data['empresa']
    pasta = data['pasta']

    user = User(dataset=dataset, sectors_si=sectors_si, sectors_no=sectors_no, t_estudis=t_estudis, empresa=empresa,
                pasta=pasta)
    return Response(response=recommend(user, dataset.people), status=200, content_type='application/json')


if __name__ == '__main__':
    app.run()
