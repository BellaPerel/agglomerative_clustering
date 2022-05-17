class Link:
    def compute(self, cluster, other, distances):
        """
        abstract function with no implementation
        :param cluster: first cluster
        :param other: second cluster
        :param distances: the distance dictionary
        """
        pass


class SingleLink(Link):
    def compute(self, cluster, other, distances):
        """
        computes the distance between two clusters according to single link measure
        :param cluster: first cluster
        :param other: second cluster
        :param distances: the distance dictionary
        :return: the minimum distance between clusters
        """
        min_dist = float('inf')
        for i in cluster.samples:
            for j in other.samples:
                if (distances[(i.s_id, j.s_id)]) < min_dist:
                    min_dist = distances[(i.s_id, j.s_id)]
        return min_dist


class CompleteLink(Link):
    def compute(self, cluster, other, distances):
        """
        computes the distance between two clusters according to complete link measure
        :param cluster: first cluster
        :param other: second cluster
        :param distances: the distance dictionary
        :return: the maximum distance between clusters
        """
        max_dist = float('-inf')
        for i in cluster.samples:
            for j in other.samples:
                if (distances[(i.s_id, j.s_id)]) > max_dist:
                    max_dist = distances[(i.s_id, j.s_id)]
        return max_dist
