FROM docker.io/jupyter/base-notebook

RUN mamba install --yes 'jupyterhub==4.0.1' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
