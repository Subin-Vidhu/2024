# Docker Basics Unleashed

- 📦 Ever wished software was as easy as playing with Lego blocks? Slotting them together and voila, you've built something cool. Docker is here to grant that wish!

- 🐳 What's Docker? Think of it as your personal software toolbox. Inside this box, every software, app, or tool comes packed in its own little bubble, called a 'container'. Everything the software needs to run perfectly is right there with it!

- 🔄 No More 'It Works On My Machine'! We've all been there, right? An app works perfectly on one computer but throws a tantrum on another. With Docker, if it works in a container on your laptop, it'll work in the same container anywhere else!

- 🎨 Mix & Match! Like a paint palette, Docker lets you use multiple containers together. Need a specific database for your app? There’s a container for that. A special environment for coding? There's a container for that too.

- 🚀 Ready, Set, Deploy! With Docker, sending your software to a big server or sharing it with the world is as easy as handing over your container. It's like sharing a recipe where you provide every single ingredient in a perfect little box.

- Time to dive in and play with these magic boxes. By the end of this, Docker won't just be a tool; it'll be your favorite sidekick on every tech adventure! 🌟🛠

---

- Some common Docker commands:
  - `docker run <image>`: Run a container from an image.
  - `docker ps`: List all running containers.
  - `docker ps -a`: List all containers.
  - `docker stop <container>`: Stop a running container.
  - `docker rm <container>`: Remove a container.
  - `docker images`: List all images.
  - `docker rmi <image>`|`docker image rm <image>`: Remove an image.
  - `docker pull <image>`: Pull an image from Docker Hub.
  - `docker push <image>`: Push an image to Docker Hub.
  - `docker exec -it <container> <command>`: Run a command in a running container.
  - `docker build -t <image> .`: Build an image from a Dockerfile.
  - `docker-compose up`: Start services defined in a `docker-compose.yml` file.
  - `docker-compose down`: Stop services defined in a `docker-compose.yml` file.

---

- 📚 **Resources**:
  - [Docker Documentation](https://docs.docker.com/)
  - [Docker Hub](https://hub.docker.com/)
  - [Docker Compose Documentation](https://docs.docker.com/compose/)
  - [Docker Compose File Reference](https://docs.docker.com/compose/compose-file/)

---

- Dockerfile:

    - A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image.
    - Docker can build images automatically by reading the instructions from a Dockerfile.
    - A Dockerfile adheres to a specific format and set of instructions which you can find at the [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).

        ```Docker
        # Use an official Python runtime as a parent image
        FROM python:2.7-slim

        # Set the working directory to /app
        WORKDIR /app

        # Copy the current directory contents into the container at /app
        ADD . /app

        # Install any needed packages specified in requirements.txt
        RUN pip install --trusted-host pypi.python.org -r requirements.txt

        # Make port 80 available to the world outside this container
        EXPOSE 80

        # Define environment variable
        ENV NAME World

        # Run app.py when the container launches
        CMD ["python", "app.py"]
        ```

    - To build an image from a Dockerfile, use the `docker build` command:

        ```bash
        docker build -t friendlyhello . # Replace friendlyhello with your desired image name
        ```

    - To run a container from the image you just built, use the `docker run` command:

        ```bash
        docker run -p 4000:80 friendlyhello # Replace friendlyhello with the image name you used, here 4000 and 80 are the host and container ports respectively, meaning you can access the app at http://localhost:4000
        ```

---

- WebServer Container:

    - To run a simple web server in a container, use the following command:

        ```bash
        docker run -d -p 80:80 --name webserver nginx # This command runs the nginx web server in a container, -d flag runs the container in detached mode, -p flag maps port 80 of the host to port 80 of the container, --name flag assigns a name to the container, you can access the web server at http://localhost or http://localhost:80, where you'll see the default nginx welcome page
        ```

    - To stop the container, use the following command:

        ```bash
        docker stop webserver # Replace webserver with the name of your container
        ```

    - To remove the container, use the following command:

        ```bash
        docker rm webserver # Replace webserver with the name of your container
        ```