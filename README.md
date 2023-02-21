# Como-se-crea-una-blockchain

Script detallado de como se crea una blockchain en Python 

Para visualizar la idea de blockchain, tenemos que imaginar un libro contable en donde se registran todas las entradas y salidas de dinero. Este libro está formado por una cadena de bloques, los cuales contienen información de una transacción en la red. Al estar enlazados, permiten las transferencias de datos donde no hace falta un tercero que certifique la información. Una vez que se introduce la información, en el registro global de transacciones aparecen los elementos que han sido modificados o añadidos de manera inmutable, sin posibilidad de borrar esos registros.

Para llegar a una cadena a prueba de ataques y eficaz, se divide en varias fases:

Cada vez que se hace una transacción, se queda en el «pool de transacciones», y cuando hay suficientes transacciones en dicho pool, se conforma un bloque de datos. Este, a su vez, puede registrar la información que se seleccione, como qué, cuándo, etc.
Cada bloque está conectado con el precedente y el posterior. El conjunto forma una cadena de datos que se va  uniendo de forma segura confirmando el tiempo exacto y la secuencia de transacciones.
Estas transacciones conforman bloques que se unen y forman una cadena irreversible (un cambio en cualquier bloque alteraría la validación de todos los bloques sucesivos), lo que denominamos blockchain. Llegados a este punto, cada bloque adicional, refuerza la verificación del anterior, y continúa, reforzando también toda la cadena de bloques. Así se consigue que dicha cadena sea a prueba de manipulaciones, asegurando un espacio confiable.

Por otro lado hemos de entender que es un hash. Podriamos decir que se trata de una función criptográfica que genera identificadores únicos e irrepetibles a partir de una información dada. Estas funciones tienen como objetivo primordial codificar datos para formar una cadena de caracteres única. Todo ello sin importar la cantidad de datos introducidos inicialmente en la función. Estas funciones sirven para asegurar la autenticidad de datos, almacenar de forma segura contraseñas, y la firma de documento electrónicos.


Debido a que hay 16 caracteres posibles en un valor hexadecimal, cada vez que incrementaamos la dificultad en un hash, hacemos que el rompecabezas sea 16 veces más 
difícil, aumentando con ello el tiempo de resolución.

En la tabla inferior se puede visualizar el tiempo estimado:


![tiempo estimado hash](https://user-images.githubusercontent.com/113166854/217254862-bb32e671-e86b-45dc-b47f-ce473f26857b.png)



Links de interés:


https://www.youtube.com/watch?v=bBC-nXj3Ng4

https://www.youtube.com/watch?v=Us_Og3JeXiI

https://www.youtube.com/watch?v=qOVAbKKSH10


* para la creación de este repositorio, he tomado como referencia el contenido didáctico de varios libros y diversos canales de youtube.
