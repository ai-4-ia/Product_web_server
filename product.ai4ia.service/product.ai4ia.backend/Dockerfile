FROM python:3.10

# create working directory in container 
WORKDIR /app
# Copy the requirements file to the container
COPY ./requirements.txt /app

# Install project dependencies
RUN pip install -r requirements.txt

# COPY all source to the container
COPY . /app

# Start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

