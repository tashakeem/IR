class Clustering:

    def get_cluster(self,documents):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        from collections import defaultdict

        cluster = defaultdict(list)
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(documents.values())
        true_k = 8

        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)

        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()

        for i in range(true_k):
            for ind in order_centroids[i, :50]:
                cluster[i].append(terms[ind])
        return cluster

