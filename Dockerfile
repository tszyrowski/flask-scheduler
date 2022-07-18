FROM python:3.7

# Create a directory named flask
RUN mkdir flask

# Copy everything to flask folder
COPY . /flask/

# Make flask as working directory
WORKDIR /flask

# Install the Python libraries
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the entrypoint script
CMD ["bash", "entrypoint.sh"]