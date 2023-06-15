# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10

# Create and activate virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000

# Runs the migrations and creates a superuser
RUN python auth_user/manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('sujata', 'sujata.goudar@infovision.com', 'admin')" | python auth_user/manage.py shell
RUN python auth_user/manage.py collectstatic --noinput

# Runs the production server
ENTRYPOINT ["python", "auth_user/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

