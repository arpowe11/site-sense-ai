# Use Python v3.12 base
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy everything into the container, excluding via .dockerignore
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Start the app using Gunicorn and wsgi.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
