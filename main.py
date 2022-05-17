import sys
from data import *
import agglomerative_clustering as agg


def main(argv):
    data = Data(argv[1])
    list_of_samples = data.create_samples()
    distances = data.distances_matrix()

    print("single link:")
    new_run = agg.AgglomerativeClustering("SingleLink", list_of_samples, distances)
    new_run.run(7)
    print("")

    print("complete link:")
    new_run2 = agg.AgglomerativeClustering("CompleteLink", list_of_samples, distances)
    new_run2.run(7)


if __name__ == '__main__':
    main(sys.argv)
