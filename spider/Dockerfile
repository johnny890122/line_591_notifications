FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ./
RUN python3.11 -m pip install -r requirements.txt -t .

COPY app.py utils.py CONST.py ./

CMD ["app.lambda_handler"]
