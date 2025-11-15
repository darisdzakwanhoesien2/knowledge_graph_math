subject/introduction_to_optimization/narrative/01_intro_to_matrix_computation.md

subject/introduction_to_optimization/derivations/1. Derivation_p_Norm_Properties.md

subject/introduction_to_optimization/nodes/Vector_Norms.md

streamlit_app/utils/graph_builder.py

subjects/
└── numerical_matrix_analysis/
    ├── relationships/
    ├── index.json
    └── narrative/


streamlit_app/
│
├── streamlit_app.py
├── app_config.py
├── utils/
│   ├── load_data.py
│   ├── graph_builder.py
│   ├── file_reader.py
│   └── search_engine.py
│
├── components/
│   ├── node_viewer.py
│   ├── derivation_viewer.py
│   ├── graph_viewer.py
│   ├── narrative_viewer.py
│   └── sidebar_navigation.py
│
└── subjects/     # You place your subjects here
    └── numerical_matrix_analysis/


knowledge_graph/
│
├── subjects/
│   ├── machine_learning/
│   │   ├── nodes/
│   │   │   ├── Attention_Mechanism.md
│   │   │   ├── KL_Divergence.md
│   │   │   ├── Covariance_Matrix.md
│   │   │   ├── Spectral_Clustering.md
│   │   │   └── ... (more ML concepts)
│   │   │
│   │   ├── derivations/
│   │   │   ├── KL_Divergence_Derivation.md
│   │   │   ├── Covariance_Matrix_Proof.md
│   │   │   ├── Spectral_Clustering_Laplacian_Derivation.md
│   │   │   └── ... (any detailed math)
│   │   │
│   │   ├── relationships/
│   │   │   ├── ml_edges.json        # edge list linking nodes
│   │   │   └── ml_subgraphs/        # optional modular subgraphs
│   │   │
│   │   ├── narrative/
│   │   │   ├── 01_introduction.md
│   │   │   ├── 02_regularization.md
│   │   │   ├── 03_spectral_methods.md
│   │   │   └── 04_probabilistic_models.md
│   │   │
│   │   └── index.json               # subject metadata, node list, summary
│   │
│   ├── data_science/
│   │   ├── nodes/
│   │   ├── derivations/
│   │   ├── relationships/
│   │   ├── narrative/
│   │   └── index.json
│   │
│   ├── signal_processing/
│   │   ├── nodes/
│   │   ├── derivations/
│   │   ├── relationships/
│   │   ├── narrative/
│   │   └── index.json
│   │
│   └── ... more subjects
│
│
├── global_kg/
│   ├── merged_graph.json           # all subjects merged into global KG
│   ├── merge_logs/
│   │   └── merge_2025-11-15.txt
│   ├── ontology_schema.json        # unified schema for all subjects
│   └── similarity_edges.json       # cross-subject connections (optional)
│
│
├── datasets/
│   ├── pdf_topics/                 # topics extracted from user PDFs
│   ├── complete_nodes.json
│   ├── incomplete_nodes.json
│   └── raw_pdfs/
│
│
├── scripts/
│   ├── extract_topics.py           # PDF → topic list
│   ├── generate_nodes_from_topics.py
│   ├── enrich_kg.py                # fill missing nodes
│   ├── merge_subject_kg.py
│   ├── render_streamlit/           # optional UI utilities
│   └── utils/
│
│
├── streamlit_app/
│   ├── pages/
│   │   ├── 01_View_KG.py
│   │   ├── 02_Search_Node.py
│   │   ├── 03_Subject_Browser.py
│   │   ├── 04_Derivation_Explorer.py
│   │   ├── 05_Narrative_Reader.py
│   │   └── 06_Upload_PDF_Topic_Extractor.py
│   ├── assets/
│   └── streamlit_app.py
│
└── README.md
