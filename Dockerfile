FROM postgres:15

# Set environment variables
ENV POSTGRES_DB=bank_db
ENV POSTGRES_USER=bank_user
ENV POSTGRES_PASSWORD=bank_password

# Expose port
EXPOSE 5432

# Set the default command
CMD ["postgres"] 

# Set environment variables
ENV POSTGRES_DB=bank_db
ENV POSTGRES_USER=bank_user
ENV POSTGRES_PASSWORD=bank_password

# Expose port
EXPOSE 5432

# Set the default command
CMD ["postgres"] 