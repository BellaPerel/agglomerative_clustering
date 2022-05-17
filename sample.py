
class Sample:
    def __init__(self, s_id, genes, label):
        """
        the class builder
        :param s_id: the sample id, his type is integer. the value in the column sample
        :param genes: list of gens for each sample
        :param label: the class which the record belongs to, its a string, the value of the record in column type
        """
        self.s_id = s_id
        self.genes = genes
        self.label = label

    def compute_euclidean_distance(self, other):
        """
        calculate the euclidean distance from one sample to another
        :param other: an object of the sample class, this is the other sample we calculate the euclidean distance to
        :return: the euclidean distance between the sample to the other sample
        """
        return sum([(my - his) ** 2 for my, his in zip(self.genes, other.genes)]) ** 0.5

