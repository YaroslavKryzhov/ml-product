from hyperopt import hp
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models

# Определяем search_space
CLUSTERING_SEARCH_SPACE_CONFIG = {
    Models.KMEANS: {
        'n_clusters': hp.quniform('n_clusters', 2, 20, 1),
        'init': hp.choice('init', ['k-means++', 'random']),
    },

    Models.MINI_BATCH_KMEANS: {
        'n_clusters': hp.quniform('n_clusters', 2, 20, 1),
        'init': hp.choice('init', ['k-means++', 'random']),
        'batch_size': hp.quniform('batch_size', 50, 200, 1),
    },

    Models.AFFINITY_PROPAGATION: {
        'damping': hp.uniform('damping', 0.5, 1),
    },

    Models.MEAN_SHIFT: {
        'bandwidth': hp.uniform('bandwidth', 0.5, 2),
    },

    Models.SPECTRAL_CLUSTERING: {
        'n_clusters': hp.quniform('n_clusters', 2, 20, 1),
        'eigen_solver': hp.choice('eigen_solver', [None, 'arpack', 'lobpcg']),
    },

    Models.WARD: {
        'n_clusters': hp.quniform('n_clusters', 2, 20, 1),
    },

    Models.AGGLOMERATIVE_CLUSTERING: {
        'n_clusters': hp.quniform('n_clusters', 2, 20, 1),
        'linkage': hp.choice('linkage',
                             ['ward', 'complete', 'average', 'single']),
    },

    Models.DBSCAN: {
        'eps': hp.uniform('eps', 0.1, 1),
        'min_samples': hp.quniform('min_samples', 2, 10, 1),
    },

    Models.OPTICS: {
        'min_samples': hp.quniform('min_samples', 2, 10, 1),
        'xi': hp.uniform('xi', 0.01, 0.1),
    },

    Models.BIRCH: {
        'n_clusters': hp.quniform('n_clusters', 2, 20, 1),
        'threshold': hp.uniform('threshold', 0.1, 1),
    },

    Models.GAUSSIAN_MIXTURE: {
        'n_components': hp.quniform('n_components', 2, 20, 1),
        'covariance_type': hp.choice('covariance_type',
                                     ['full', 'tied', 'diag', 'spherical']),
    },
}
