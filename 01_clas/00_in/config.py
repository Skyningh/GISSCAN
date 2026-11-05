all_configs = []

# all possible model combinations
possible_models = {
    'cnn': {'type': 'image', 'columns': ['images'], 'features': 512},
    'gnn0': {
        'type': 'graph0',
        'columns': ['nx_list'],
        'input_feature_size': 8,
        'output_feature_size': 256,
        'params': {
            'model_embedding_size': 128,
            'model_attention_heads': 1,
            'model_layers': 2,
            'model_dropout_rate': 0.2,
            'model_top_k_ratio': 0.5,
            'model_top_k_every_n': 1,
            'model_dense_neurons': 256,
            'model_edge_dim': 2
        }
    },
    'gnn1': {
        'type': 'graph1',
        'columns': ['dual_graph_nx_list'],
        'input_feature_size': 4,
        'output_feature_size': 256,
        'params': {
            'model_embedding_size': 128,
            'model_attention_heads': 1,
            'model_layers': 2,
            'model_dropout_rate': 0.2,
            'model_top_k_ratio': 0.5,
            'model_top_k_every_n': 1,
            'model_dense_neurons': 256,
            'model_edge_dim': 1
        }
    },
    'gnn2': {
        'type': 'graph2',
        'columns': ['primal_graph_nx_list'],
        'input_feature_size': 5,
        'output_feature_size': 256,
        'params': {
            'model_embedding_size': 128,
            'model_attention_heads': 1,
            'model_layers': 2,
            'model_dropout_rate': 0.2,
            'model_top_k_ratio': 0.5,
            'model_top_k_every_n': 1,
            'model_dense_neurons': 256,
            'model_edge_dim': 1
        }
    },
    'global0': {'type': 'global', 'columns': ['global_handcrafted_features'], 'input_features': 23, 'features': 256},
    'label': {'type': 'label', 'columns': ['label0']}
}