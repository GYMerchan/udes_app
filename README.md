# udes_app
Aplicación de gestión de espacios fisicos

Inicialmente se debe configurar la base de datos en postgresql con el nombre 'UDES'
Se inicia como un proyecto normal en virtual enviroment de python
Ya con la base datos creada, se realizan las migraciones-- python manage.py makemigrations
Luego se migran-- python manage.py migrate

Inicialmente en el entorno de pruebas, la aplicación se ejecutó con superuser de django, creado con comando-- python manage.py createsuperuser, llamado Administrador
Desde allí se manejaron los usuarios, con dos grupos, un grupo llamado Estudiante, con sus respectivas caracteristicas, y permisos y el otro grupo llamado Usuario_Control
Desde el panel de administración de django se crearon los usuarios y se agregaron a sus respectivos grupos
En el Home <localhost:8000> esta la pagina base que redirecciona a los dos clientes, cada cliente <Genesis> y <Galileo> son totalmente independientes
La creación de Sitios para reservar, y las reservas, tienen diferentes tags de navegación y según los permisos especificos dados a cada usuario, permiten su manejo, 
a nivel de crud
Las validaciones se encuentran en el views.py y las reglas junto a los modelos.

