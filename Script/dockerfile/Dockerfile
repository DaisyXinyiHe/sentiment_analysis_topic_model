FROM puckel/docker-airflow:1.10.9
RUN apt-get update
RUN cd $HOME
RUN git clone https://github.com/DaisyXinyiHe/sentiment_analysis_topic_model.git
RUN cd sentiment_analysis_topioc_model/Scripts
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

