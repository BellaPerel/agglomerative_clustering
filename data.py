import pandas
from sample import *


class Data:
    def __init__(self, path):
        """
        the class builder
        :param path: the path of the data set csv
        """
        df = pandas.read_csv(path)
        self.data = df.to_dict(orient="list")
        self.list_of_samples = []

    def create_samples(self):
        """
        creates list of samples derived from the given data set
        :param: none
        :return: list of all samples derived from the given data set
        """
        j = 0
        self.list_of_samples = []
        for i in range(len(self.data["samples"])):
            genes = []
            s_id = self.data["samples"][i]
            label = self.data["type"][i]
            for key in self.data:
                if key == "samples" or key == "type":
                    pass
                else:
                    genes.append(self.data[key][j])
            new_sample = Sample(s_id, genes, label)
            self.list_of_samples.append(new_sample)
            j = j+1
        return self.list_of_samples

    def distances_matrix(self):
        """
        calculate the distance between 2 points and saves it in a matrix
        :return: returns distance matrix between all of the genes vectors ("points")
        """
        length = len(self.list_of_samples)
        distances_matrix = [[-1]*length for i in range(length)]
        distances_dict = dict()
        for i in range(len(self.list_of_samples)):
            for j in range(len(self.list_of_samples)):
                if distances_matrix[i][j] == -1:
                    distances_matrix[i][j] = self.list_of_samples[i].compute_euclidean_distance(self.list_of_samples[j])
                    distances_matrix[j][i] = distances_matrix[i][j]
                else:
                    pass
        for i, sample1 in zip(range(len(self.list_of_samples)), self.list_of_samples):
            for j, sample2 in zip(range(len(self.list_of_samples)), self.list_of_samples):
                if sample1.s_id == sample2.s_id:
                    pass
                else:
                    distances_dict[(sample1.s_id, sample2.s_id)] = distances_matrix[i][j]
        return distances_dict
