from datetime import datetime
from app.database.config_database import Config
from app.config import settings
import psycopg2
import os
import json


def get_connection():
    print(f"→ Estableciendo conexión a {Config.DB_HOST}, base: {Config.DB_NAME}")
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        connect_timeout=5
    )
    
    return conn


def db_get_videos_by_status(status):
    print(f"→ Consultando videos pendientes de descarga...")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT *
                        FROM
                        "youtube".get_data_videos(
                        p_status := %s::text
                        )""", (status,))
            pending_videos = cur.fetchall()
        print(f"✅ Se encontraron {len(pending_videos)} videos pendientes.")
        return pending_videos
    except Exception as e:
        print(f"❌ Error al obtener videos pendientes: {e}")
        return []
    finally:
        conn.close()


def get_video_content(video_id):
    """
    Obtiene el contenido de un video desde la base de datos.
    
    Returns:
        dict con keys: video_id, transcription, summary
        [] si no se encuentra o hay un error
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT *
                        FROM
                        "youtube".get_video_content(
                        p_video_id := %s::text
                        )""", (video_id,))
            video_content = cur.fetchone()
        print(f"✅ Contenido obtenido para {video_id}")
        return { 'video_id': video_content[0], 'transcription': video_content[2] , 'summary': video_content[1] }
    except Exception as e:
        print(f"❌ Error al obtener contenido para {video_id}: {e}")
        return []
    finally:
        conn.close()


def update_status_to_vector(video_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        CALL
                        "youtube".update_status_to_vector(
                        p_video_id := %s::text
                        )""", (video_id,))
            conn.commit()
        print(f"✅ Status actualizado a 'vector' para {video_id}")
    except Exception as e:
        print(f"❌ Error al actualizar status a 'vector' para {video_id}: {e}")
    finally:
        conn.close()


def update_embedding_error(video_id, error_message):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        CALL
                        "youtube".update_embedding_error(
                        p_video_id := %s::text,
                        p_error_message := %s::text
                        )""", (video_id, error_message))
            conn.commit()
        print(f"✅ Status actualizado a 'error' para {video_id}")
    except Exception as e:
        print(f"❌ Error al actualizar status a 'error' para {video_id}: {e}")
    finally:
        conn.close()