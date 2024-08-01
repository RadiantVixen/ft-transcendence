FROM python:3

RUN apt-get update && apt-get install -y

# RUN apt-get update && apt-get install -y \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# COPY ./conf/script.sh /script.sh

# RUN chmod +x /script.sh

# CMD ["./script.sh"]

CMD ["tail", "-t"]
