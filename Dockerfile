# Start with the official Python image
FROM python:3.11

# Create a user and set up permissions
RUN useradd -m -u 1000 user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Create the app directory and set permissions before switching to the non-root user
WORKDIR $HOME/app
RUN mkdir -p $HOME/app/.files && chown -R user:user $HOME/app

# Copy files as root and set ownership
COPY --chown=user . $HOME/app

# Switch to the non-root user
USER user

# Copy the requirements file and install dependencies
COPY --chown=user requirements.txt $HOME/app/requirements.txt
RUN pip install --user -r requirements.txt

# Copy the rest of the application files
COPY --chown=user . .

# Define the command to run the application
CMD ["chainlit", "run", "app.py", "--port", "7860"]
