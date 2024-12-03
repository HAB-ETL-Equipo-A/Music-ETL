import streamlit as st

analysises = [
    """ Aunque la elección de la tonalidad se distribuye de una forma ligeramente más homogénea 
 entre las canciones aleatorias que en los éxitos mundiales, se puede observar 
 en ambos gráficos un orden de preferencia claro entre las tonalidades existentes en la música actual. 

 Destacan entre las canciones exitosas, las que tienen una tonalidad alegre, fácil 
 de comprender y de tocar instrumentos populares como piano y guitarra. Se sabe que C Maj es la 
 escala preferida tanto para la música en ámbitos de enseñanza como para la composición entre géneros populares
 por no tener notas alteradas. 
 Son populares también G Maj y D Maj, probablemente por la facilidad de componer canciones desde la guitarra sobre estas tonalidades. 

 Entre las primeras posiciones de ambas listas se encuentran las 
 tonalidades mayores entre las que se puede alcanzar una amplia tesitura de voz y ofrecen facilidad al ser interpretadas. 
 Es lógico pensar que es preferible elegir tonalidades que no presenten dificultades por el número de alteraciones que tengan, para 
 que el proceso de composición pueda ser fluido y sin factores técnicos que descentren la atención del artista. 

 Destacan las tonalidades de A min y E min entre las menores en la lista de canciones aleaorias por su facilidad 
 a la hora de tocarlas y componer sobre ellas. A min es relativa menor de C Maj y no tiene alteraciones. E min solo tiene una alteración
 y es la tonalidad con la que la guitarra se puede tocar de forma más abierta (pulsando menos cuerdas con la mano izquierda). 

 Personalmente me resulta anómalo que C Maj/Db Maj se encuentre entre las tonalidades maás frecuentes en ambas listas.
 Esta tonalidad tiende a tener una sonoridad brillante, luminosa y un poco "grande", pero escrita como C Maj,
 es muy complicada de tocar en instrumentos como piano, guitarra, instrumentos de viento de llaves o de metal. 
 La única explicación que se me ocurre para que sea tan popular, es que se toque desde la guitarra usando una cejilla en el primer traste
 (lugar donde la cejilla se utiliza con más frecuencia), mientras se articula la tonalidad de C, obteniendo 
 así un sonido similar pero más brillante que en la tonalidad más frecuente de la música popular. 

 En todos los gráficos mostrados se observa una frecuencia de canciones en las tonalidades de D Maj y D min mucho menor al resto
 de tonalidades.
 Esto podría explicarse atendiendo a motivos técnicos, prácticos y culturales:

 - Al igual que CMaj, estas tonalidades son incómodas de tocar, tanto a nivel de técnica y 
 articulación como por la lectura de partituras,  por sus múltiples alteraciones, por lo que se  
 suele transponer a tonalidades más simples. 
 - Re sostenido no se popularizó en géneros comunes y tiene menor asociación 
 emocional o "color tonal" en la música popular, (según ciertas teorías, como
 la de "colores de tonalidades").
 - Aunque la tecnología permite cualquier tonalidad, los productores prefieren 
 tonalidades comunes para facilitar colaboración y compatibilidad."""
]

for a in analysises:
    st.write(a)