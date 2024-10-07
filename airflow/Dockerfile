FROM apache/airflow:latest-python3.11

USER root
# mssql odbc
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN sudo apt-get update
RUN sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# other things
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install firefox-esr -y

USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

# USER root
# RUN chmod -R 777 /home/airflow
# RUN git clone https://world-headlines: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@github.com/rst0070/world-headlines.git
# RUN git clone https://world-headlines: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@github.com/world-headlines/world-headlines.github.io.git
