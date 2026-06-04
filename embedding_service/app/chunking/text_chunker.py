from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings
import re

def split_into_chunks(text:str, chunk_size:int=1000, chunk_overlap:int=200) -> list[str]:
    """
    Splits text into overlapping chunks using recursive character splitting.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]

    )
    return text_splitter.split_text(text)


def calculate_chunk_size(text:str,model_name:str) -> tuple[int,int]:
    """
    Defines the Chunk size based on the lenght of the text
    """
    model_info = settings.MODELS_EMBEDDINGS_REGISTRY.get(model_name)
    if not model_info:
        raise ValueError(f"Model '{model_name}' not found in registry.")

    max_tokens = model_info["max_tokens"]
    chars_per_token = model_info["chars_per_token"]

    max_chars = max_tokens * chars_per_token
    chunk_size = min(int(len(text) * 0.15), max_chars)
    chunk_size = max(chunk_size, 200)
    overlap = int(chunk_size * 0.2)
    return chunk_size,overlap

def clean_text(text,source="generic"):
    """
    Clean text based on the source, removing unwanted characters and formatting.
    """
    
    if source == "youtube":
        # Remueve timestamps: 12:34 o 1:23:45
        text = re.sub(r'\b(?:\d{1,2}:)?\d{1,2}:\d{2}\b', '', text)
        # Remueve URLs
        text = re.sub(r'http[s]?://\S+', '', text)
    elif source == "docs":
       # Remueve referencias numéricas tipo [1], [40]
        text = re.sub(r'\[\d+\]', '', text)
        # Remueve referencias de letras tipo [a], [nota]
        text = re.sub(r'\[[a-zA-Z]+\]', '', text)
        # Remueve URLs
        text = re.sub(r'http[s]?://\S+', '', text)
    
    # --- REGLAS GLOBALES (Para todo texto) ---
    
    # 1. Eliminar caracteres invisibles (Zero-width spaces, etc.)
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)   
    
    # (OMITIDO INTENCIONALMENTE: No borrar [^\w\s] para conservar puntos y comas)
    
    # 2. Reemplazar múltiples espacios o tabs con un solo espacio
    text = re.sub(r'[ \t]+', ' ', text) 
    
    # 3. Limitar saltos de línea a un máximo de dos (vital para el Chunker)
    text = re.sub(r'\n{3,}', '\n\n', text) 
    
    # 4. Quitar espacios basura al inicio y al final
    return text.strip()

def optimize_chunks(chunks: list[str]) -> list[str]:
	"""
	Optimiza los chunks uniendo chunks pequeños con el siguiente chunk disponible.
	Si el chunk pequeño es el último, lo une con el chunk anterior.
	"""
	optimized_chunks: list[str] = []
	index = 0
	min_size = 100
	separator = "\n\n"

	while index < len(chunks):
		current_chunk = chunks[index]

		if len(current_chunk) < min_size and index + 1 < len(chunks):
			next_chunk = chunks[index + 1]

			print(f"Warning: Chunk of length {len(current_chunk)} is too short")

			optimized_chunks.append(
				current_chunk.rstrip() + separator + next_chunk.lstrip()
			)
			index += 2

		elif len(current_chunk) < min_size and index + 1 == len(chunks):
			print(
				f"Warning: Last chunk of length {len(current_chunk)} is too short. "
				"Merging with previous chunk."
			)

			if optimized_chunks:
				optimized_chunks[-1] = (
					optimized_chunks[-1].rstrip()
					+ separator
					+ current_chunk.lstrip()
				)
			else:
				optimized_chunks.append(current_chunk)

			index += 1

		else:
			optimized_chunks.append(current_chunk)
			index += 1

	return optimized_chunks



if __name__ == "__main__":

    sample_text = """
El mar de la supervivencia: Saga de los Supernovatos
Saga del East Blue[40]
La serie comienza con la ejecución de Gold Roger, un hombre conocido como el «Rey de los Piratas» (海賊王 Kaizoku-Ō?), quien justo antes de su muerte, hace mención de su gran tesoro legendario, el «One Piece» (ワンピース Wan Pīsu?), y que puede ser tomado por quien lo encuentre. Esto marca el inicio de una era conocida como la «Gran Era de los Piratas» (大海賊時代 Daikaizokujidai?). Como resultado, un sinnúmero de piratas zarparon hacia Grand Line, el mar donde se encuentra dicho tesoro, con el objetivo de encontrarlo. Más de veinte años después de la muerte de Roger, el One Piece sigue sin ser encontrado. Un joven llamado Monkey D. Luffy, quien comió la Fruta Goma Goma, una Fruta del Diablo la cual le otorgó elasticidad, inspirado por la admiración que desde su infancia le tiene al pirata legendario Shanks «el Pelirrojo», comienza su aventura desde su hogar en el mar East Blue para encontrar el One Piece y convertirse en el próximo Rey de los Piratas, llevando consigo el sombrero de paja que se Shanks le cedió. Con el fin de crear y convertirse en el capitán de una tripulación pirata propia reclutando varios miembros para superar a la tripulación de los Piratas del Pelirrojo, recluta durante su viaje en el East Blue a Roronoa Zoro, un infame espadachín y ex-cazarrecompensas, Nami, una navegante experta en robos, Usopp, un francotirador mentiroso, y Sanji, un cocinero enamoradizo pero caballeroso, además de conseguir un barco llamado el Going Merry. Tras viajar por varias islas en las que se enfrenta a varios enemigos como la Marina u otros piratas infames, la tripulación llega a la entrada de Grand Line.

Saga de Arabasta[40]
Después de llegar finalmente a la Grand Line, el grupo conoce en la entrada a Crocus, el guardián del faro y cuidador de Laboon, una gigantesca ballena. Él les da información para navegar por el mar y sobre Laugh Tale, la última isla donde Roger dejó el One Piece. También conocen a Nefertari Vivi, una princesa que desea salvar a su país, el Reino de Arabasta, de manos de una peligrosa organización criminal llamada Baroque Works, viajando ella y su super pato mascota Karoo con la tripulación durante un tiempo. Durante su trayecto hacia Arabasta, los piratas pasan por Little Garden, una isla donde entablan amistad con Dorry y Brogy, dos gigantes del lugar, y la Isla de Drum, una isla invernal donde invitan a un reno antropomórfico llamado Tony Tony Chopper a unirse a la tripulación, ejerciendo como el médico de a bordo. Kureha, la mentora de Chopper, también hace mención a que el verdadero nombre de Roger realmente era Gol D. Roger. Una vez que la tripulación llega hasta de Arabasta, comienzan una serie de batallas contra la organización Baroque Works y su líder, el Guerrero del Mar Sir Crocodile. Tras derrotarles y liberar al reino, la tripulación se despide de Vivi. Inmediatamente después, Nico Robin, una arqueóloga que antes pertenecía a Baroque Works como vicepresidenta, se une a la tripulación.

Saga de Skypiea[40]
Poco después, queriendo buscar una ruta a la legendaria «Isla del Cielo», llegan a Jaya, una isla, donde conocen Marshal D. Teach, alias «Barbanegra», quien también aspira a convertirse en el Rey de los Piratas, comenzando también una rivalidad entre él y Luffy. La tripulación viaja hasta una isla del cielo llamada Skypiea, donde sin querer, se unen a una guerra incipiente entre dos tribus habitantes de dicho lugar, lo que los lleva a enfrentarse al líder de la isla, Enel, quien posee el poder de la Fruta del Diablo de crear relámpagos y electricidad. Luffy logra derrotarlo y, con ello, terminar la guerra. También al abandonar la isla obtienen gran cantidad de oro, el cual deciden usarlo para reparar el Going Merry, y de paso encontrar un carpintero para arreglar futuros daños en el barco.

Saga de Water Seven[41]
Tras un encuentro con los Piratas de Foxy, quienes les retan a una serie de juegos pirata llamada Davy Back Fight, la tripulación llega a Water 7, donde los carpinteros del lugar les informan que el Going Merry está demasiado dañado y no es posible repararlo, lo que causa que Usopp renuncie a seguir en la tripulación. Después tienen un encuentro con un cíborg llamado Franky, el líder de la Familia Franky, así como el pupilo de Tom, quien construyó el barco del Rey de los Piratas. El CP9, una agencia de inteligencia del Gobierno Mundial, captura a Robin y a Franky, por lo que sus amigos van en su rescate a Enies Lobby, la Isla Judicial. Tras una lucha contra los agentes del CP9, la tripulación logra rescatar a Robin. De vuelta en Water 7, los Piratas de Sombrero de Paja, Franky construye una nueva embarcación llamada el Thousand Sunny, con el fin de reemplazar al perdido Going Merry, y con ello él se une a la tripulación como su carpintero. Tras ello, Usopp pide disculpas a sus compañeros por marcharse, volviendo de nuevo a reconciliarse con ellos.

Saga de Thriller Bark[41]
Navegando en su nuevo barco, los Piratas de Sombrero de Paja se encuentran con un barco fantasma, donde conocen a Brook, un esqueleto viviente que fue revivido por la Fruta Revive Revive, y además, a quien Gecko Moria, otro miembro de los Siete Guerreros del Mar y capitán del gigantesco barco pirata Thriller Bark, le robó su sombra. Una vez que los piratas derrotan a Moria y liberan las sombras de sus víctimas, Brook se une a la tripulación como su músico.

Saga de Marine Ford[41]
Después de llegar al Archipiélago Sabaody, la tripulación se prepara para ingresar al Nuevo Mundo, la segunda mitad del Grand Line. Ahí, se hacen amigos de Silvers Rayleigh, el antiguo primer oficial de la tripulación de los Piratas de Roger, y le piden que recubra su barco para que puedan atravesar la Red Line por medio del subsuelo oceánico. Pero tras verse involucrados en una revuelta causada por un Noble Mundial, llega al lugar uno de los Siete Guerreros del Mar, Bartholomew Kuma, quien los separa enviándolos a diferentes lugares mediante sus poderes de la Fruta del Diablo.
Luffy llega a una isla afrodisíaca llamada Amazon Lily, donde únicamente la habitan mujeres, y gobernada por Boa Hancock, una de los Siete Guerreros del Mar, la cual acaba enamorandose de él. Una vez que el muchacho se entera de que su hermano mayor, Portgas D. Ace, se encuentra prisionero en Impel Down, Luffy emprende un viaje para liberarlo. Luffy logra soltar a otros prisioneros, como al hombre-pez y miembro de los Siete Guerreros del Mar Jinbe, a quien encerraron tras negarse a colaborar con el Gobierno. Sin embargo, descubre que su hermano mayor ya ha sido llevado a Marine Ford para ser ejecutado. Tras fugarse de prisión para rescatarle, se revela que Ace es el hijo biológico de Roger, siendo el hermano adoptivo de Luffy. En Marine Ford, una guerra estalla entre las fuerzas de la Marina y la tripulación del renombrado Edward Newgate, alias «Barbablanca», asistidos por Luffy y resto de fugitivos de Impel Down. Al clímax de la guerra, Ace y Barbablanca son asesinados. Luffy lamenta la pérdida de Ace y se quiebra emocionalmente, al igual que la pérdida que vivió de pequeño con su otro hermano adoptivo, Sabo. Con la ayuda de Jinbe y a petición de Rayleigh, Luffy decide enviar a sus amigos el mensaje de esperar dos años hasta volver a encontrarse, pasando todos ellos por un intenso régimen de entrenamiento.


"""
    sample_text = clean_text(sample_text,source="docs")
    chunk_size, chunk_overlap = calculate_chunk_size(sample_text, "all-MiniLM-L6-v2")
    print(f"Calculated chunk size: {chunk_size} characters")
    chunks = split_into_chunks(sample_text, chunk_size, chunk_overlap)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
        print(f"Chunk {i+1} length: {len(chunk)} characters\n")
    
    optimized_chunks = optimize_chunks(chunks)
    for i, chunk in enumerate(optimized_chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
        print(f"Chunk {i+1} length: {len(chunk)} characters\n")