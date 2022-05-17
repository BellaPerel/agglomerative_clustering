class Cluster:
    def __init__(self, c_id, samples):
        """
        the class builder
        :param c_id: the cluster id number
        :param samples: a list of sample objects
        """
        self.c_id = c_id
        self.samples = []
        self.samples.append(samples)

    def merge(self, other):
        """
        in each step of the algorithm this method merges 2 clusters into one. we add the other coordinates into self
        coordinates. the new cluster id will be the minimum between the 2 clusters ids'.
        :param other: sample from the data
        :return: list of samples
        """
        self.samples = self.samples+other.samples
        self.c_id = min(self.c_id, other.c_id)
        del other
        self.samples.sort(key=lambda x: x.s_id)
        return self.samples

    def print_details(self, silhoeutte):
        """
        prints the cluster details
        :param silhoeutte: the silhoeutte measure if the cluster
        :return: nothing
        """
        print("Cluster ", self.c_id, ": ", self.get_samples(), ", dominant label = ", self.dominant_label(),
              ", silhouette = ", float("{0:.3f}".format(silhoeutte.get(self.c_id))), sep='')

    def dominant_label(self):
        """
        finds the dominant label for the cluster
        :return: the dominant label in the cluster
        """
        dominant_dict = {}
        for sample in self.samples:
            dominant_dict[sample.label] = 0
        for sample in self.samples:
            dominant_dict[sample.label] += 1
        dominant_label = max(dominant_dict, key=dominant_dict.get)
        return dominant_label

    def get_samples(self):
        """
        organize the cluster samples as a list
        :return: the cluster samples as a list
        """
        samples_list = []
        for sample in self.samples:
            samples_list.append(sample.s_id)
        return samples_list
