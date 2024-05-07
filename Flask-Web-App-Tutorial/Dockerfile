FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

# Perbarui pip terlebih dahulu
RUN pip install --upgrade pip

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install library OpenGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
#CMD ["python", "-m", "flask", "run", "--host=188.166.239.153"]