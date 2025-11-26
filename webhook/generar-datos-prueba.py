#!/usr/bin/env python3
"""
Script para generar y enviar datos ficticios de llamadas al webhook de Google Apps Script.
Esto permite poblar Google Sheets con datos de prueba para análisis en Looker Studio.
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List

# URL del webhook
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwo0m3C-2oeDErTAO9pzLp40B1407SbH3rZPsD9BN1ogQ9X11WT70GgG9iVuWbDaXfv/exec"

# Número de origen (from)
FROM_NUMBER = "22833301"

# Contactos de prueba
CONTACTOS = [
    {"telefono": "60012345", "nombre": "Alex Martínez", "problema": "software"},
    {"telefono": "60025678", "nombre": "Karla Gómez", "problema": "hardware"},
    {"telefono": "60039012", "nombre": "José Pérez", "problema": "rendimiento lento"},
    {"telefono": "60043456", "nombre": "María Díaz", "problema": "sobrecalentamiento del equipo"},
    {"telefono": "60057890", "nombre": "Diego Hernández", "problema": "pantalla azul"},
    {"telefono": "70011122", "nombre": "Andrea López", "problema": "arranque del sistema"},
    {"telefono": "70023344", "nombre": "Carlos Rivera", "problema": "virus y malware"},
    {"telefono": "70035566", "nombre": "Sofía Morales", "problema": "conexión a internet"},
    {"telefono": "70047788", "nombre": "Luis Castillo", "problema": "sistema operativo"},
    {"telefono": "70059900", "nombre": "Gabriela Sánchez", "problema": "batería de la laptop"},
    {"telefono": "61234567", "nombre": "Fernando Rivas", "problema": "almacenamiento lleno"},
    {"telefono": "62345678", "nombre": "Valeria Campos", "problema": "fallas de audio"},
    {"telefono": "63456789", "nombre": "Ernesto López", "problema": "puertos USB"},
    {"telefono": "74567890", "nombre": "Daniela Molina", "problema": "teclado"},
    {"telefono": "75678901", "nombre": "Ricardo Aguilar", "problema": "actualización de Windows"},
]

# Respuestas predefinidas para generar datos realistas
CALIFICACIONES = [1, 2, 3, 4, 5]
NPS_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
TIEMPO_ATENCION = ["bueno", "regular", "malo"]
AMABILIDAD_TECNICO = ["buena", "regular", "mala"]
ESTADOS_LLAMADA = ["completada", "rechazada", "reprogramada", "errónea"]

COMENTARIOS_POSITIVOS = [
    "Excelente servicio, muy profesional.",
    "Muy contento con la atención recibida.",
    "El técnico fue muy amable y resolvió mi problema rápido.",
    "Muy buena experiencia, lo recomiendo.",
    "Servicio de calidad, quedé satisfecho.",
    "Muy profesional y eficiente.",
]

COMENTARIOS_REGULARES = [
    "Estuvo bien, pero podría mejorar.",
    "El servicio fue aceptable.",
    "Regular, esperaba más rapidez.",
    "Bien, pero el técnico podría ser más amable.",
    "Funcional, pero no destacable.",
]

COMENTARIOS_NEGATIVOS = [
    "El técnico tardó mucho en llegar.",
    "No quedé satisfecho con la solución.",
    "El servicio fue lento y poco eficiente.",
    "Esperaba mejor atención.",
    "No resolvieron mi problema completamente.",
]

MENSAJES_BOT = [
    "Hola, {nombre}, le saluda Karla desde TecniFix Solutions. Le contacto brevemente para validar la calidad del servicio técnico que recibió recientemente sobre un problema de {problema}, no nos tomará más de dos minutos. ¿Me permite comenzar con la primera pregunta?",
    "Excelente. En una escala del uno al cinco, donde uno es pésimo y cinco es excelente, ¿cómo calificaría el servicio técnico recibido?",
    "Entiendo, en nuestra escala eso corresponde a un {calificacion} sobre cinco, ¿está de acuerdo?",
    "Calificación del servicio: {calificacion}. ¿Cómo consideraría el tiempo de espera para ser atendido: bueno, regular o malo?",
    "Tiempo de atención: {tiempo_atencion}. ¿Y la amabilidad del técnico fue buena, regular o mala?",
    "Amabilidad del técnico: {amabilidad_tecnico}. En una escala del cero al diez, ¿qué probabilidad hay de que recomiende TecniFix a un amigo?",
    "Registro su valor como {nps}. Por último, ¿tiene algún comentario o sugerencia adicional?",
    "Comentario registrado, gracias. Muchas gracias por su tiempo, sus comentarios nos ayudan mucho. Doy por completada esta llamada. Que pase una feliz jornada.",
]

MENSAJES_USUARIO = [
    "Ok, está bien.",
    "Sí, puedo.",
    "Claro, adelante.",
    "{calificacion_texto}",
    "Sí, estoy de acuerdo.",
    "{tiempo_atencion_texto}",
    "{amabilidad_texto}",
    "{nps_texto}",
    "{comentario}",
    "Gracias a usted.",
]


def generar_calificacion_texto(calificacion: int) -> str:
    """Genera una respuesta de texto para la calificación."""
    opciones = {
        1: ["Pésimo", "Muy malo", "Terrible"],
        2: ["Malo", "Regular", "No muy bueno"],
        3: ["Regular", "Aceptable", "Ni bueno ni malo"],
        4: ["Bueno", "Muy bueno", "Satisfactorio"],
        5: ["Excelente", "Muy bueno", "Perfecto", "Muy contento, le pondría 5"],
    }
    return random.choice(opciones[calificacion])


def generar_tiempo_texto(tiempo: str) -> str:
    """Genera una respuesta de texto para el tiempo de atención."""
    opciones = {
        "bueno": ["Bueno, la verdad", "Sí, bueno", "Está bueno", "Fue rápido"],
        "regular": ["Regular", "Más o menos", "Ni rápido ni lento"],
        "malo": ["Tardó mucho", "Fue lento", "Demasiado tiempo"],
    }
    return random.choice(opciones[tiempo])


def generar_amabilidad_texto(amabilidad: str) -> str:
    """Genera una respuesta de texto para la amabilidad."""
    opciones = {
        "buena": ["Buena", "Muy amable", "Sí, fue amable"],
        "regular": ["Regular", "Más o menos", "Ni tan buena ni tan mala", "Vamos a ir a regular"],
        "mala": ["No fue muy amable", "Podría mejorar", "Regular"],
    }
    return random.choice(opciones[amabilidad])


def generar_nps_texto(nps: int) -> str:
    """Genera una respuesta de texto para el NPS."""
    if nps >= 8:
        return f"La verdad es que sería muy alta, póngale {nps}."
    elif nps >= 5:
        return f"Sería {nps}, está bien."
    else:
        return f"Probablemente {nps}."


def generar_comentario(calificacion: int, nps: int) -> str:
    """Genera un comentario basado en la calificación y NPS."""
    if calificacion >= 4 and nps >= 8:
        return random.choice(COMENTARIOS_POSITIVOS)
    elif calificacion >= 3 and nps >= 5:
        return random.choice(COMENTARIOS_REGULARES)
    else:
        return random.choice(COMENTARIOS_NEGATIVOS)


def generar_transcripcion(contacto: Dict, calificacion: int, nps: int, tiempo_atencion: str, 
                          amabilidad_tecnico: str, comentario: str) -> List[Dict]:
    """Genera una transcripción ficticia pero realista de la llamada."""
    transcript = []
    base_time = datetime.now() - timedelta(minutes=random.randint(1, 5))
    
    # Mensaje inicial del bot
    mensaje_bot_1 = MENSAJES_BOT[0].format(
        nombre=contacto["nombre"],
        problema=contacto["problema"]
    )
    transcript.append({
        "id": "m1",
        "created_at": base_time.isoformat() + "Z",
        "text": mensaje_bot_1,
        "user": "bot"
    })
    
    # Respuesta del usuario
    transcript.append({
        "id": "m2",
        "created_at": (base_time + timedelta(seconds=2)).isoformat() + "Z",
        "text": random.choice(MENSAJES_USUARIO[:4]),
        "user": "user"
    })
    
    # Pregunta de calificación
    transcript.append({
        "id": "m3",
        "created_at": (base_time + timedelta(seconds=4)).isoformat() + "Z",
        "text": MENSAJES_BOT[1],
        "user": "bot"
    })
    
    # Respuesta de calificación
    calificacion_texto = generar_calificacion_texto(calificacion)
    transcript.append({
        "id": "m4",
        "created_at": (base_time + timedelta(seconds=6)).isoformat() + "Z",
        "text": calificacion_texto,
        "user": "user"
    })
    
    # Confirmación del bot
    transcript.append({
        "id": "m5",
        "created_at": (base_time + timedelta(seconds=8)).isoformat() + "Z",
        "text": MENSAJES_BOT[2].format(calificacion=calificacion),
        "user": "bot"
    })
    
    # Confirmación del usuario
    transcript.append({
        "id": "m6",
        "created_at": (base_time + timedelta(seconds=10)).isoformat() + "Z",
        "text": "Sí, estoy de acuerdo.",
        "user": "user"
    })
    
    # Pregunta de tiempo de atención
    transcript.append({
        "id": "m7",
        "created_at": (base_time + timedelta(seconds=12)).isoformat() + "Z",
        "text": MENSAJES_BOT[3].format(calificacion=calificacion),
        "user": "bot"
    })
    
    # Respuesta de tiempo
    tiempo_texto = generar_tiempo_texto(tiempo_atencion)
    transcript.append({
        "id": "m8",
        "created_at": (base_time + timedelta(seconds=14)).isoformat() + "Z",
        "text": tiempo_texto,
        "user": "user"
    })
    
    # Pregunta de amabilidad
    transcript.append({
        "id": "m9",
        "created_at": (base_time + timedelta(seconds=16)).isoformat() + "Z",
        "text": MENSAJES_BOT[4].format(tiempo_atencion=tiempo_atencion),
        "user": "bot"
    })
    
    # Respuesta de amabilidad
    amabilidad_texto = generar_amabilidad_texto(amabilidad_tecnico)
    transcript.append({
        "id": "m10",
        "created_at": (base_time + timedelta(seconds=18)).isoformat() + "Z",
        "text": amabilidad_texto,
        "user": "user"
    })
    
    # Pregunta de NPS
    transcript.append({
        "id": "m11",
        "created_at": (base_time + timedelta(seconds=20)).isoformat() + "Z",
        "text": MENSAJES_BOT[5].format(amabilidad_tecnico=amabilidad_tecnico),
        "user": "bot"
    })
    
    # Respuesta de NPS
    nps_texto = generar_nps_texto(nps)
    transcript.append({
        "id": "m12",
        "created_at": (base_time + timedelta(seconds=22)).isoformat() + "Z",
        "text": nps_texto,
        "user": "user"
    })
    
    # Confirmación del bot sobre NPS
    transcript.append({
        "id": "m13",
        "created_at": (base_time + timedelta(seconds=24)).isoformat() + "Z",
        "text": MENSAJES_BOT[6].format(nps=nps),
        "user": "bot"
    })
    
    # Pregunta de comentario
    transcript.append({
        "id": "m14",
        "created_at": (base_time + timedelta(seconds=26)).isoformat() + "Z",
        "text": MENSAJES_BOT[6].format(nps=nps).replace(f"Registro su valor como {nps}.", "").strip() or MENSAJES_BOT[7],
        "user": "bot"
    })
    
    # Respuesta de comentario
    transcript.append({
        "id": "m15",
        "created_at": (base_time + timedelta(seconds=28)).isoformat() + "Z",
        "text": comentario if comentario else "No, todo bien.",
        "user": "user"
    })
    
    # Cierre del bot
    transcript.append({
        "id": "m16",
        "created_at": (base_time + timedelta(seconds=30)).isoformat() + "Z",
        "text": MENSAJES_BOT[7],
        "user": "bot"
    })
    
    return transcript


def generar_resumen(contacto: Dict, calificacion: int, nps: int, tiempo_atencion: str, 
                    amabilidad_tecnico: str, comentario: str) -> str:
    """Genera un resumen de la llamada."""
    return (
        f"Karla de TecniFix Solutions contactó a {contacto['nombre']} para evaluar la calidad del "
        f"servicio técnico recibido por un problema de {contacto['problema']}. "
        f"{contacto['nombre']} calificó el servicio con un {calificacion} sobre cinco y consideró "
        f"el tiempo de espera como {tiempo_atencion}. La amabilidad del técnico fue calificada como "
        f"{amabilidad_tecnico}. {contacto['nombre']} expresó una probabilidad de {nps} sobre diez "
        f"de recomendar TecniFix a un amigo. Como comentario adicional, mencionó: '{comentario}'. "
        f"Karla agradeció a {contacto['nombre']} por su tiempo y completó la llamada."
    )


def generar_payload(contacto: Dict, call_id: int) -> Dict:
    """Genera un payload completo para una llamada."""
    # Generar datos aleatorios pero coherentes
    calificacion = random.choice(CALIFICACIONES)
    nps = random.choice(NPS_VALUES)
    tiempo_atencion = random.choice(TIEMPO_ATENCION)
    amabilidad_tecnico = random.choice(AMABILIDAD_TECNICO)
    estado_llamada = random.choice(ESTADOS_LLAMADA)
    comentario = generar_comentario(calificacion, nps)
    
    # Ajustar coherencia: si la calificación es alta, NPS debería ser alto también
    if calificacion >= 4:
        nps = random.choice([7, 8, 9, 10])
    elif calificacion <= 2:
        nps = random.choice([0, 1, 2, 3, 4, 5])
    
    # Generar transcripción
    transcript = generar_transcripcion(
        contacto, calificacion, nps, tiempo_atencion, amabilidad_tecnico, comentario
    )
    
    # Generar resumen
    summary = generar_resumen(
        contacto, calificacion, nps, tiempo_atencion, amabilidad_tecnico, comentario
    )
    
    # Calcular créditos (aleatorio entre 200 y 800)
    credits = random.randint(200, 800)
    
    payload = {
        "successful": True,
        "call": {
            "id": call_id,
            "from": FROM_NUMBER,
            "to": contacto["telefono"],
            "credits": credits,
            "transcript": transcript,
            "summary": summary,
            "is_completed": estado_llamada == "completada",
            "analysis_schema": {
                "calificacion_servicio": "number",
                "nps": "number",
                "opinion_cliente": "string",
                "tiempo_atencion": "string",
                "amabilidad_tecnico": "string",
                "estado_llamada_completada_rechazada_reprogramada_o_erronea": "string"
            },
            "analysis": {
                "calificacion_servicio": calificacion,
                "nps": nps,
                "opinion_cliente": comentario,
                "tiempo_atencion": tiempo_atencion,
                "amabilidad_tecnico": amabilidad_tecnico,
                "estado_llamada_completada_rechazada_reprogramada_o_erronea": estado_llamada
            }
        }
    }
    
    return payload


def enviar_webhook(payload: Dict) -> bool:
    """Envía el payload al webhook."""
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Error: {e}")
        return False


def main():
    """Función principal."""
    print("=" * 60)
    print("Generador de Datos de Prueba para Webhook TecniFix")
    print("=" * 60)
    print(f"\nURL del webhook: {WEBHOOK_URL}")
    print(f"Total de contactos: {len(CONTACTOS)}")
    print(f"\nIniciando envío de datos...\n")
    
    exitosos = 0
    fallidos = 0
    
    for i, contacto in enumerate(CONTACTOS, 1):
        call_id = 900000000 + i  # IDs únicos empezando desde 900000001
        
        print(f"[{i}/{len(CONTACTOS)}] Enviando datos para {contacto['nombre']} ({contacto['telefono']})...", end=" ")
        
        payload = generar_payload(contacto, call_id)
        
        if enviar_webhook(payload):
            print("✅ Enviado correctamente")
            exitosos += 1
        else:
            print("❌ Falló")
            fallidos += 1
        
        # Pequeño delay para no saturar el servidor
        if i < len(CONTACTOS):
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("Resumen:")
    print(f"  ✅ Exitosos: {exitosos}")
    print(f"  ❌ Fallidos: {fallidos}")
    print(f"  📊 Total: {len(CONTACTOS)}")
    print("=" * 60)
    print("\n¡Datos enviados! Revisa tu Google Sheets para ver los resultados.")
    print("Los datos estarán disponibles en Looker Studio después de unos minutos.")


if __name__ == "__main__":
    main()



