FROM odoo:18.0

USER root
SHELL ["/bin/bash", "-c"]

# update & install pip
RUN apt-get update \
    && apt-get install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip and install required Python packages in one layer
RUN pip3 install --upgrade pip \
    && pip3 install ipdb html2text python3-linkedin python-docx docx-mailmerge \
    hijri_converter WooCommerce moodlepy MechanicalSoup debugpy asn1crypto num2words paramiko
