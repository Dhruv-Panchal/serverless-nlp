FROM python:3.7
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=config/key.json
# For web server
# Don't use on Google run, use $PORT instead
EXPOSE 8080



# Default command to run app 
CMD streamlit run --browser.serverAddress='0.0.0.0' --server.port=8080 main.py