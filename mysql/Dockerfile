FROM mysql:latest
ADD my.cnf /etc/mysql/my.cnf
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 3306
CMD ["mysqld"]
