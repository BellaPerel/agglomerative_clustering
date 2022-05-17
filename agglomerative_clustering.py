import cluster as clustering
import link as link


class AgglomerativeClustering:
    def __init__(self, linker, samples, distances):
        """
        :param linker: indicates the type of linkage we want to use for the clustering
        :param samples: list of samples
        :param distances:  matrix of distances
        """
        if linker == "CompleteLink":
            self.linker = link.CompleteLink()
        else:
            self.linker = link.SingleLink()
        self.samples = samples
        self.clusters = []
        self.distances = distances
        for sample in samples:
            new_cluster = clustering.Cluster(sample.s_id, sample)
            self.clusters.append(new_cluster)

    def run(self, max_clusters):
        """
        runs the clustering algorithm
        :param max_clusters: the amount of clusters we want on the end of the algorithm run
        :return:
        """
        index1 = -1
        index2 = -1
        min_dist = float('inf')
        while len(self.clusters) > max_clusters:
            min_dist = float('inf')
            for i, j in zip(self.clusters, range(len(self.clusters))):
                for n, k in zip(self.clusters, range(len(self.clusters))):
                    if j == k:
                        pass
                    else:
                        dist_between_clusters = self.linker.compute(self.clusters[j], self.clusters[k], self.distances)
                        if dist_between_clusters < min_dist:
                            min_dist = dist_between_clusters
                            cluster1 = self.clusters[j]
                            cluster2 = self.clusters[k]
                            index1 = j
                            index2 = k
            cluster1.merge(cluster2)
            if cluster1.c_id < cluster2.c_id:
                del self.clusters[index2]
            else:
                del self.clusters[index1]

        for i, j in zip(self.clusters, range(len(self.clusters))):
            self.clusters[j].print_details(self.compute_summery_silhoeutte())
        print("Whole data: silhouette = ", float("{0:.3f}".format(self.compute_summery_silhoeutte().get(0))), ", RI = ",
              float("{0:.3f}".format(self.compute_rand_index())), sep='')

    def compute_summery_silhoeutte(self):
        """
        computes the silhoeutte values of the clusters and the whole data silhoeutte value and puts it in a dictionary
        :return: dictionary of silhoeutte values of the clusters. in key 0 there is the whole data silhoeutte value
        """
        sample_silhoeutte_dict = self.compute_silhoeutte()
        cluster_silhoeutte_dict = dict()
        cluster_silhoeutte_dict[0] = 0
        sum_total_sx = 0
        for cluster in self.clusters:
            sum_sx = 0
            for sample in cluster.samples:
                sum_sx += sample_silhoeutte_dict.get(sample.s_id)
            sum_total_sx += sum_sx
            cluster_silhoeutte = sum_sx / len(cluster.samples)
            cluster_silhoeutte_dict[cluster.c_id] = cluster_silhoeutte
        cluster_silhoeutte_dict[0] = sum_total_sx / len(sample_silhoeutte_dict)
        return cluster_silhoeutte_dict

    def compute_silhoeutte(self):
        """
        computes the silhoeutte value of each point in the dataset
        :return: a dictionary with all the samples' silhoeutte in all the data set.
        """
        silhoeutte_dict = {}
        in_compute = 0
        out_compute = 0
        for cluster in self.clusters:
            for sample in cluster.samples:
                in_compute = self.in_compute_silhoeutte(sample, cluster)
                out_compute = (self.out_compute_silhoeutte(sample, cluster))
                if len(cluster.samples) <= 1:
                    silhoeutte = 0
                    silhoeutte_dict[sample.s_id] = silhoeutte
                else:
                    in_x = in_compute / (len(cluster.samples) - 1)
                    out_x = out_compute
                    if max(in_x, out_x) != 0:
                        silhoeutte = (out_x - in_x) / (max(in_x, out_x))
                        silhoeutte_dict[sample.s_id] = silhoeutte
        return silhoeutte_dict

    def in_compute_silhoeutte(self, sample, cluster):
        """
        calculates the average distance of the sample from the other points in the same cluster
        :param sample: the current sample
        :param cluster: the current cluster of the points we check the sample distance from
        :return:the sum of all the distances from all the other points in the cluster
        """
        total_in = 0
        for sample2 in cluster.samples:
            if sample.s_id == sample2.s_id:
                pass
            else:
                total_in += self.distances[(sample.s_id, sample2.s_id)]
        return total_in

    def out_compute_silhoeutte(self, sample, cluster):
        """
        calculates the minimum distance of the point Xi from the other clusters(not including the cluster she belongs to
        :param sample: the current sample
        :param cluster: the current cluster of the points we check the sample distance from
        :return:the minimum distance of the point Xi from the other clusters(not including the cluster she belongs to.
        """
        distance_list = []
        for cluster2 in self.clusters:
            total_out = 0
            for sample2 in cluster2.samples:
                if cluster.c_id == cluster2.c_id:
                    pass
                else:
                    total_out += self.distances[(sample.s_id, sample2.s_id)]
            if total_out != 0:
                distance_list.append(total_out/len(cluster2.samples))
        return min(distance_list)

    def compute_rand_index(self):
        """
        measures in how much decisions the algorithm was right based on all of his decisions
        :return: the result of in how much decisions the algorithm was right based on all of his decisions
        """
        n = 0
        for cluster in self.clusters:
            n += len(cluster.samples)
        TP = 0
        for cluster in self.clusters:
            for sample in cluster.samples:
                for sample2 in cluster.samples:
                    if sample.s_id == sample2.s_id:
                        pass
                    elif sample.label == sample2.label:
                        TP = TP + 1
        TN = 0
        for cluster in self.clusters:
            for sample in cluster.samples:
                for cluster2 in self.clusters:
                    if cluster2.c_id == cluster.c_id:
                        pass
                    else:
                        for sample2 in cluster2.samples:
                            if sample2.label != sample.label:
                                TN = TN + 1
        RI = (TP + TN) / ((n * (n - 1) / 2)*2)
        return RI
