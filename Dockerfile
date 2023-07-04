# Use an official Python runtime as the base image
FROM fleetproatgmail/requirements_archimedes

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# Copy the rest of the project code
COPY . .

RUN pyarmor gen utils/tools_m1.py

RUN rm utils/tools_m1.py
# COPY .dist .

RUN cp -r -f ./dist/* ./
# RUN chmod 644 dist/pyarmor_runtime_000000/pyarmor_runtime.so

# Expose the port on which your FastAPI application runs
EXPOSE 8000

# Define the command to run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
